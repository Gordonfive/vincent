#!/bin/sh
set -eu

status_file=/var/lib/mission-control-install/status.json
report_file=/var/lib/mission-control-install/self-test.json
enrollment_file=/var/lib/mission-control/identity/enrollment-request.json
log_file=/var/log/mission-control/bootstrap.log
expected_commit_file=/opt/mission-control-media/expected-commit

render() {
    python3 - "$status_file" "$report_file" "$enrollment_file" "$log_file" "$expected_commit_file" <<'PY'
import json, shutil, sys
from pathlib import Path

status_path, report_path, enrollment_path, log_path, expected_path = map(Path, sys.argv[1:])
status = {}
report = {}
enrollment = {}
for path, target in ((status_path, status), (report_path, report), (enrollment_path, enrollment)):
    try:
        target.update(json.loads(path.read_text()))
    except Exception:
        pass
try:
    expected_commit = expected_path.read_text().strip()
except Exception:
    expected_commit = "unknown"

state = status.get("state", "BOOTSTRAPPING")
step = status.get("step", "starting")
hostname = status.get("hostname", report.get("hostname", "vincent-worker"))
overall = report.get("overall", "PENDING")
if state == "FAILED":
    overall = "FAIL"
fingerprint = enrollment.get("fingerprint", "pending")
worker_id = enrollment.get("worker_id", "pending")
checks = report.get("checks", [])
failed = [item for item in checks if not item.get("ok")]
attempt = status.get("attempt", 0)
maximum = status.get("max_attempts", 0)
width = max(80, shutil.get_terminal_size((120, 40)).columns)
height = max(24, shutil.get_terminal_size((120, 40)).lines)
try:
    lines = log_path.read_text(errors="replace").splitlines()
except Exception:
    lines = []
nonempty = [line for line in lines if line.strip()]
last_error = nonempty[-1] if nonempty else status.get("detail", "pending")

print("\033[2J\033[H", end="")
print("VINCENT WORKER")
print("=" * min(width, 100))
print(f"STATE: {state:<20} OVERALL: {overall:<8} STEP: {step}")
print(f"HOSTNAME: {hostname:<28} WORKER ID: {worker_id}")
print(f"FINGERPRINT: {fingerprint}")
print(f"EXPECTED GIT: {expected_commit}")
print(f"IP: {status.get('ip_addresses') or 'pending'}")
print(f"ROUTE: {status.get('default_route') or 'pending'}")
print(f"GITHUB DNS: {status.get('github_dns', 'pending')}")
if maximum:
    print(f"RETRY: {attempt}/{maximum}")
print("-" * min(width, 100))
print(f"CURRENT TASK: {status.get('detail') or step}")
if state == "FAILED" or overall == "FAIL":
    print(f"LAST ERROR:   {last_error[:max(0, width-14)]}")
print("-" * min(width, 100))

if checks:
    print("SELF-TEST STATUS")
    for item in checks[:10]:
        result = "PASS" if item.get("ok") else "FAIL"
        detail = str(item.get("detail", "")).replace("\n", " ")
        print(f"{item.get('name', 'unknown'):<28} {result:<4} {detail[:max(0, width-40)]}")
    print("-" * min(width, 100))

if state == "ENROLLMENT_REQUIRED" and overall == "PASS":
    print("READY FOR REMOTE ENROLLMENT")
elif state == "FAILED" or overall == "FAIL":
    print("INSTALLATION / SELF-TEST FAILURE")
    if failed:
        print("FAILED CHECKS:")
        for item in failed[:6]:
            print(f"- {item.get('name', 'unknown')}: {str(item.get('detail', ''))[:max(0, width-6)]}")
    print("Photograph this screen; no local login is required.")
else:
    print("Vincent is provisioning and testing itself.")

print("Alt+F2: interactive Codex console (available after Codex installation)")
print("Alt+F1: return to this dashboard")
print("-" * min(width, 100))
print("LIVE WORK OUTPUT")

reserved = 20 + min(len(checks), 10)
log_lines = max(8, height - reserved)
for line in lines[-log_lines:]:
    print(line[:width])
PY
}

while :; do
    render
    sleep 2
done
