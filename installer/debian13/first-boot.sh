#!/bin/sh
set -eu

log_file=/var/log/mission-control/bootstrap.log
status_file=/var/lib/mission-control-install/status.json
source_archive=/opt/mission-control-media/platform.tar.gz
source_root=/opt/mission-control/source
self_test=/usr/local/sbin/vincent-self-test

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
    detail=$2
    python3 - "$status_file" "$state" "$detail" <<'PY'
import json, socket, sys
from datetime import datetime, timezone
from pathlib import Path

path, state, detail = sys.argv[1:]
payload = {
    "schema_version": 1,
    "state": state,
    "detail": detail,
    "hostname": socket.gethostname(),
    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
}
Path(path).write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
PY
    chmod 0600 "$status_file"
}

trap 'code=$?; if [ "$code" -ne 0 ]; then write_status FAILED "bootstrap or self-test failed; see self-test report and bootstrap log"; fi' EXIT
write_status BOOTSTRAPPING "installing platform from verified USB payload"

if [ ! -f "$source_archive" ]; then
    write_status FAILED "platform archive is missing"
    exit 1
fi
if [ -e "$source_root" ]; then
    write_status FAILED "source directory already exists; refusing implicit reuse"
    exit 1
fi
if [ ! -x "$self_test" ]; then
    write_status FAILED "Vincent self-test executable is missing"
    exit 1
fi

install -d -m 0755 "$source_root"
tar -xzf "$source_archive" -C "$source_root"
sh "$source_root/installer/install.sh" "$source_root"
install -d -m 0755 /var/lib/vincent
install -m 0644 /var/lib/mission-control/identity/enrollment-request.json \
    /var/lib/vincent/enrollment-request.json
sh "$source_root/bootstrap/provision-worker-baseline.sh"

write_status SELF_TESTING "running unattended Vincent appliance validation"
"$self_test"
write_status ENROLLMENT_REQUIRED "self-test passed; approve scoped enrollment remotely"
systemctl disable mission-control-first-boot.service
