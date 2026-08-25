#!/bin/sh
set -eu

report=/var/lib/mission-control-install/self-test.json
install -d -m 0700 /var/lib/mission-control-install

python3 - "$report" <<'PY'
import json
import os
import pwd
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

report_path = Path(sys.argv[1])
checks = []

def run(name, command, predicate=lambda rc, out, err: rc == 0):
    completed = subprocess.run(command, text=True, capture_output=True)
    output = (completed.stdout or completed.stderr).strip()
    ok = predicate(completed.returncode, completed.stdout, completed.stderr)
    checks.append({"name": name, "ok": bool(ok), "detail": output[:500]})
    return ok

def record(name, ok, detail=""):
    checks.append({"name": name, "ok": bool(ok), "detail": str(detail)[:500]})
    return bool(ok)

hostname = subprocess.run(["hostname"], text=True, capture_output=True, check=True).stdout.strip()
record("hostname", bool(re.fullmatch(r"vincent-worker-\d{6}", hostname)), hostname)

run("network_route", ["ip", "route", "get", "1.1.1.1"])
run("network_dns", ["getent", "ahosts", "github.com"])
run("ssh_service", ["systemctl", "is-active", "--quiet", "ssh"])
run("git", ["git", "--version"])
run("github_cli", ["gh", "--version"])
run("docker", ["docker", "info"])
run("ddev", ["ddev", "version"])
run("codex", ["codex", "--version"])
run("python_packaging", ["python3", "-c", "import pip, setuptools.build_meta"])

source_root = Path("/opt/mission-control/source")
expected_path = Path("/opt/mission-control-media/expected-commit")
installed_path = Path("/var/lib/mission-control-install/installed-commit")
try:
    expected = expected_path.read_text().strip()
    installed = installed_path.read_text().strip()
    head = subprocess.run(["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True, capture_output=True, check=True).stdout.strip()
    remote = subprocess.run(["git", "-C", str(source_root), "remote", "get-url", "origin"], text=True, capture_output=True, check=True).stdout.strip()
    record("git_exact_commit", bool(expected and expected == installed == head), f"expected={expected} installed={installed} head={head}")
    record("git_public_remote", remote == "https://github.com/Gordonfive/vincent.git", remote)
except Exception as exc:
    record("git_exact_commit", False, repr(exc))
    record("git_public_remote", False, repr(exc))

try:
    account = pwd.getpwnam("mission-control")
    record("service_account", account.pw_shell.endswith("nologin"), account.pw_shell)
except KeyError:
    record("service_account", False, "mission-control account missing")

human_accounts = [entry.pw_name for entry in pwd.getpwall() if 1000 <= entry.pw_uid < 60000]
record("no_human_login_accounts", not human_accounts, ",".join(human_accounts) or "none")

request_path = Path("/var/lib/mission-control/identity/enrollment-request.json")
try:
    request = json.loads(request_path.read_text())
    required = {"worker_id", "fingerprint", "public_key"}
    record("enrollment_request", required.issubset(request), request.get("worker_id", "missing worker_id"))
except Exception as exc:
    record("enrollment_request", False, repr(exc))

archive = Path("/opt/mission-control-media/platform.tar.gz")
run("embedded_recovery_payload", ["tar", "-tzf", str(archive)]) if archive.is_file() else record("embedded_recovery_payload", False, "archive missing")

private_key_marker = re.compile(br"BEGIN (?:OPENSSH|RSA|EC) PRIVATE KEY")
try:
    data = archive.read_bytes()
    found = private_key_marker.search(data)
    record("embedded_private_key_scan", found is None, "no private-key marker" if found is None else "private-key marker found")
except Exception as exc:
    record("embedded_private_key_scan", False, repr(exc))

completed = subprocess.run(["systemctl", "is-enabled", "mission-control-worker.service"], text=True, capture_output=True)
record("worker_authority_disabled", completed.returncode != 0, (completed.stdout or completed.stderr).strip())

passed = all(item["ok"] for item in checks)
payload = {
    "schema_version": 1,
    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "hostname": hostname,
    "overall": "PASS" if passed else "FAIL",
    "checks": checks,
}
report_path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
os.chmod(report_path, 0o600)

for item in checks:
    print(f"{item['name']}: {'PASS' if item['ok'] else 'FAIL'} {item['detail']}")
print(f"VINCENT_SELF_TEST={'PASS' if passed else 'FAIL'}")
sys.exit(0 if passed else 1)
PY
