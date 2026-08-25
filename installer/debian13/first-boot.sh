#!/bin/sh
set -eu

log_file=/var/log/mission-control/bootstrap.log
status_file=/var/lib/mission-control-install/status.json
expected_commit_file=/opt/mission-control-media/expected-commit
source_root=/opt/mission-control/source
self_test=/usr/local/sbin/vincent-self-test
repository_url=https://github.com/Gordonfive/vincent.git
network_attempts=20
network_delay=15

machine_identity=$(cat /sys/class/dmi/id/product_uuid 2>/dev/null || cat /etc/machine-id)
vincent_hostname=$(python3 - "$machine_identity" <<'PY'
import hashlib, sys
value = int.from_bytes(hashlib.sha256(sys.argv[1].strip().encode()).digest()[:8], "big") % 1_000_000
print(f"vincent-worker-{value:06d}")
PY
)
hostnamectl set-hostname "$vincent_hostname"
python3 - "$vincent_hostname" <<'PY'
import re, sys
from pathlib import Path
hostname = sys.argv[1]
path = Path("/etc/hosts")
text = path.read_text()
line = f"127.0.1.1\t{hostname}"
if re.search(r"^127\.0\.1\.1\s+.*$", text, flags=re.MULTILINE):
    text = re.sub(r"^127\.0\.1\.1\s+.*$", line, text, flags=re.MULTILINE)
else:
    text += ("" if text.endswith("\n") else "\n") + line + "\n"
path.write_text(text)
PY

install -d -m 0750 /var/log/mission-control
install -d -m 0700 /var/lib/mission-control-install
exec >>"$log_file" 2>&1

write_status() {
    state=$1
    step=$2
    detail=$3
    attempt=${4:-0}
    maximum=${5:-0}
    route=$(ip route show default 2>/dev/null | head -n1 || true)
    addresses=$(hostname -I 2>/dev/null | xargs || true)
    dns=fail
    getent ahosts github.com >/dev/null 2>&1 && dns=pass
    python3 - "$status_file" "$state" "$step" "$detail" "$attempt" "$maximum" "$route" "$addresses" "$dns" <<'PY'
import json, socket, sys
from datetime import datetime, timezone
from pathlib import Path
path, state, step, detail, attempt, maximum, route, addresses, dns = sys.argv[1:]
payload = {
    "schema_version": 1,
    "state": state,
    "step": step,
    "detail": detail,
    "hostname": socket.gethostname(),
    "attempt": int(attempt),
    "max_attempts": int(maximum),
    "default_route": route,
    "ip_addresses": addresses,
    "github_dns": dns,
    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
}
Path(path).write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
PY
    chmod 0600 "$status_file"
}

trap 'code=$?; if [ "$code" -ne 0 ]; then write_status FAILED bootstrap "bootstrap or self-test failed; see console diagnostics"; fi' EXIT

if [ ! -s "$expected_commit_file" ]; then
    write_status FAILED metadata "expected Vincent commit is missing from installer metadata"
    exit 1
fi
expected_commit=$(tr -d '\r\n' <"$expected_commit_file")
case "$expected_commit" in
    [0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]*) ;;
    *) write_status FAILED metadata "expected Vincent commit is invalid"; exit 1 ;;
esac

if [ ! -x "$self_test" ]; then
    write_status FAILED metadata "Vincent self-test executable is missing"
    exit 1
fi

# Network-online.target is not sufficient on every Debian/network stack. Wait
# explicitly for route, DNS and HTTPS before declaring bootstrap failure.
attempt=1
while [ "$attempt" -le "$network_attempts" ]; do
    write_status BOOTSTRAPPING network "waiting for route, DNS and HTTPS to GitHub" "$attempt" "$network_attempts"
    route_ok=false
    dns_ok=false
    https_ok=false
    ip route show default >/dev/null 2>&1 && route_ok=true
    getent ahosts github.com >/dev/null 2>&1 && dns_ok=true
    curl --fail --silent --show-error --head --connect-timeout 5 --max-time 10 https://github.com/ >/dev/null 2>&1 && https_ok=true
    echo "network attempt $attempt/$network_attempts route=$route_ok dns=$dns_ok https=$https_ok"
    if [ "$route_ok" = true ] && [ "$dns_ok" = true ] && [ "$https_ok" = true ]; then
        write_status BOOTSTRAPPING network "network ready; GitHub reachable" "$attempt" "$network_attempts"
        break
    fi
    if [ "$attempt" -eq "$network_attempts" ]; then
        write_status FAILED network "network did not become ready after $network_attempts attempts" "$attempt" "$network_attempts"
        exit 1
    fi
    sleep "$network_delay"
    attempt=$((attempt + 1))
done

# A failed pre-fetch attempt may leave only an empty Git work area. It is safe
# to recreate that area before installation has produced an installed marker.
if [ -e "$source_root" ] && [ ! -f /var/lib/mission-control-install/installed-commit ]; then
    rm -rf "$source_root"
fi
if [ -e "$source_root" ]; then
    write_status FAILED source "source directory already exists after installation began; refusing implicit reuse"
    exit 1
fi

write_status BOOTSTRAPPING git "fetching exact Vincent commit $expected_commit from public Git"
install -d -m 0755 "$source_root"
git -C "$source_root" init -q
git -C "$source_root" remote add origin "$repository_url"

attempt=1
while [ "$attempt" -le 5 ]; do
    write_status BOOTSTRAPPING git "fetching exact commit from GitHub" "$attempt" 5
    if git -C "$source_root" fetch --no-tags --depth=1 origin "$expected_commit"; then
        break
    fi
    [ "$attempt" -lt 5 ] || {
        write_status FAILED git "Git fetch failed after 5 attempts" "$attempt" 5
        exit 1
    }
    sleep 15
    attempt=$((attempt + 1))
done

fetched_commit=$(git -C "$source_root" rev-parse FETCH_HEAD)
if [ "$fetched_commit" != "$expected_commit" ]; then
    write_status FAILED git "Git fetched $fetched_commit but installer requires $expected_commit"
    exit 1
fi
git -C "$source_root" checkout -q --detach "$expected_commit"
installed_commit=$(git -C "$source_root" rev-parse HEAD)
[ "$installed_commit" = "$expected_commit" ] || {
    write_status FAILED git "checked out commit does not match installer requirement"
    exit 1
}
printf '%s\n' "$installed_commit" >/var/lib/mission-control-install/installed-commit
chmod 0600 /var/lib/mission-control-install/installed-commit

write_status BOOTSTRAPPING platform "installing verified Vincent Git commit $expected_commit"
sh "$source_root/installer/install.sh" "$source_root"
install -d -m 0755 /var/lib/vincent
install -m 0644 /var/lib/mission-control/identity/enrollment-request.json \
    /var/lib/vincent/enrollment-request.json

write_status BOOTSTRAPPING toolchain "installing and validating worker toolchain"
sh "$source_root/bootstrap/provision-worker-baseline.sh"

write_status SELF_TESTING self-test "running unattended Vincent appliance validation"
"$self_test"
write_status ENROLLMENT_REQUIRED ready "self-test passed; approve scoped enrollment remotely"
systemctl disable mission-control-first-boot.service
