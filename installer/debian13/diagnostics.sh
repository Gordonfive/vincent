#!/bin/sh
set -eu

report=/var/lib/vincent-install/diagnostics.json
install -d -m 0700 /var/lib/vincent-install

python3 - "$report" <<'PY'
import json, os, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

report_path = Path(sys.argv[1])
checks = []

def run(name, command, timeout=30, predicate=lambda rc, out, err: rc == 0):
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
        out = completed.stdout or ""
        err = completed.stderr or ""
        ok = bool(predicate(completed.returncode, out, err))
        detail = (out or err).strip().replace("\x00", "")[:1000]
    except Exception as exc:
        ok = False
        detail = repr(exc)
    checks.append({"name": name, "ok": ok, "detail": detail})
    return ok

def record(name, ok, detail=""):
    checks.append({"name": name, "ok": bool(ok), "detail": str(detail)[:1000]})

run("default_route", ["ip", "route", "show", "default"])
run("dns_debian", ["getent", "ahosts", "deb.debian.org"])
run("dns_github", ["getent", "ahosts", "github.com"])
run("debian_index", ["curl", "--fail", "--silent", "--show-error", "--location", "--connect-timeout", "5", "--max-time", "20", "https://deb.debian.org/debian/dists/trixie/InRelease", "-o", "/dev/null"])
run("codex_installer_endpoint", ["curl", "--fail", "--silent", "--show-error", "--location", "--connect-timeout", "5", "--max-time", "20", "https://chatgpt.com/codex/install.sh", "-o", "/dev/null"])
run("docker_index", ["curl", "--fail", "--silent", "--show-error", "--location", "--connect-timeout", "5", "--max-time", "20", "https://download.docker.com/linux/debian/dists/trixie/InRelease", "-o", "/dev/null"])
run("vincent_git", ["git", "ls-remote", "https://github.com/Gordonfive/vincent.git", "HEAD"])
run("network_manager", ["systemctl", "is-active", "--quiet", "NetworkManager"])
run("ssh", ["systemctl", "is-active", "--quiet", "ssh"])
run("docker", ["docker", "info"])
run("codex", ["codex", "--version"])
run("bubblewrap", ["bwrap", "--version"])
run("time_sync", ["timedatectl", "show", "-p", "NTPSynchronized", "--value"], predicate=lambda rc, out, err: rc == 0 and out.strip().lower() == "yes")

host = shutil.which("codex-code-mode-host")
record("codex_code_mode_host", bool(host and os.access(host, os.X_OK)), host or "missing")

build = Path("/etc/vincent/build-number")
record("build_metadata", build.is_file() and bool(build.read_text().strip()), build.read_text().strip() if build.is_file() else "missing")

identity = Path("/var/lib/vincent/identity/identity.json")
request = Path("/var/lib/vincent/identity/enrollment-request.json")
record("identity_state", identity.is_file() and request.is_file(), f"identity={identity.is_file()} enrollment_request={request.is_file()}")

usage = shutil.disk_usage("/")
free_pct = round((usage.free / usage.total) * 100, 1) if usage.total else 0
record("root_free_space", free_pct >= 10.0, f"free_percent={free_pct}")

passed = all(item["ok"] for item in checks)
payload = {
    "schema_version": 1,
    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "overall": "PASS" if passed else "FAIL",
    "checks": checks,
}
report_path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
os.chmod(report_path, 0o600)
for item in checks:
    print(f"{item['name']}: {'PASS' if item['ok'] else 'FAIL'} {item['detail']}")
print(f"VINCENT_DIAGNOSTICS={'PASS' if passed else 'FAIL'}")
sys.exit(0 if passed else 1)
PY
