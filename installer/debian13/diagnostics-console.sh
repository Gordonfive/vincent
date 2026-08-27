#!/bin/sh
set -eu

report=/var/lib/vincent-install/diagnostics.json

while :; do
    clear || true
    echo "VINCENT DIAGNOSTICS"
    echo "Alt+F1 status | Alt+F2 Codex | Alt+F3 network | Alt+F4 diagnostics"
    echo
    if [ ! -s "$report" ]; then
        echo "No diagnostics report yet. Scheduled diagnostics will populate this screen."
    else
        python3 - "$report" <<'PY'
import json, sys
from pathlib import Path
try:
    data=json.loads(Path(sys.argv[1]).read_text())
except Exception as exc:
    print(f"REPORT ERROR: {exc!r}")
    raise SystemExit
print(f"LAST RUN: {data.get('timestamp','unknown')}")
print(f"OVERALL: {data.get('overall','unknown')}")
print()
for item in data.get('checks', []):
    state='PASS' if item.get('ok') else 'FAIL'
    detail=str(item.get('detail','')).replace('\n',' ')[:140]
    print(f"{state:4}  {item.get('name','unknown'):28} {detail}")
PY
    fi
    echo
    echo "Diagnostics are noninteractive and refresh automatically."
    sleep 5
done
