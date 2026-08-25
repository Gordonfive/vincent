#!/bin/sh
set -eu

status_file=/var/lib/mission-control-install/status.json
report_file=/var/lib/mission-control-install/self-test.json

render() {
    python3 - "$status_file" "$report_file" <<'PY'
import json, sys
from pathlib import Path

status_path, report_path = map(Path, sys.argv[1:])
status = {}
report = {}
try:
    status = json.loads(status_path.read_text())
except Exception:
    pass
try:
    report = json.loads(report_path.read_text())
except Exception:
    pass

state = status.get("state", "BOOTSTRAPPING")
hostname = status.get("hostname", report.get("hostname", "vincent-worker-unenrolled"))
overall = report.get("overall", "PENDING")

print("\033[2J\033[H", end="")
print("VINCENT WORKER SELF-TEST")
print("========================")
print()
for item in report.get("checks", []):
    result = "PASS" if item.get("ok") else "FAIL"
    print(f"{item.get('name', 'unknown'):<28} {result}")
print()
print(f"OVERALL: {overall}")
print(f"STATE:   {state}")
print(f"WORKER:  {hostname}")
if status.get("detail"):
    print(f"DETAIL:  {status['detail']}")
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
