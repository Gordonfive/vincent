#!/bin/sh
set -eu

status_file=/var/lib/mission-control-install/status.json
report_file=/var/lib/mission-control-install/self-test.json
enrollment_file=/var/lib/mission-control/identity/enrollment-request.json

render() {
    python3 - "$status_file" "$report_file" "$enrollment_file" <<'PY'
import json, sys
from pathlib import Path

status_path, report_path, enrollment_path = map(Path, sys.argv[1:])
status = {}
report = {}
enrollment = {}
for path, target in ((status_path, status), (report_path, report), (enrollment_path, enrollment)):
    try:
        target.update(json.loads(path.read_text()))
    except Exception:
        pass

state = status.get("state", "BOOTSTRAPPING")
hostname = status.get("hostname", report.get("hostname", "vincent-worker-unenrolled"))
overall = report.get("overall", "PENDING")
fingerprint = enrollment.get("fingerprint", "pending")
worker_id = enrollment.get("worker_id", "pending")

print("\033[2J\033[H", end="")
print("VINCENT WORKER SELF-TEST")
print("========================")
print()
for item in report.get("checks", []):
    result = "PASS" if item.get("ok") else "FAIL"
    print(f"{item.get('name', 'unknown'):<28} {result}")
print()
print(f"OVERALL:     {overall}")
print(f"STATE:       {state}")
print(f"HOSTNAME:    {hostname}")
print(f"WORKER ID:   {worker_id}")
print(f"FINGERPRINT: {fingerprint}")
if status.get("detail"):
    print(f"DETAIL:      {status['detail']}")
print()
if state == "ENROLLMENT_REQUIRED" and overall == "PASS":
    print("READY FOR REMOTE ENROLLMENT")
    print("No local login or diagnostic commands are required.")
elif state == "FAILED" or overall == "FAIL":
    print("INSTALLATION FAILED SELF-TEST")
    print("Photograph this screen; detailed logs are stored locally.")
else:
    print("Vincent is provisioning and testing itself. No login is required.")
PY
}

while :; do
    render
    sleep 15
done
