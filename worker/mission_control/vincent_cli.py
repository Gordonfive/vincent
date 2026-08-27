"""Safe single-command bootstrap for a freshly installed Vincent worker."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request

INSTRUCTIONS_URL = "https://raw.githubusercontent.com/Gordonfive/vincent/main/bootstrap/instructions.json"
EXPECTED_BOOTSTRAP_REPOSITORY = "Gordonfive/vincent"
ENROLLMENT_REQUEST = Path("/var/lib/vincent/identity/enrollment-request.json")
AUTHORIZATION = Path("/etc/vincent/authorization.json")

def run(command: list[str], *, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, cwd=cwd, text=True)

def load_instructions() -> dict:
    request = urllib.request.Request(INSTRUCTIONS_URL, headers={"User-Agent": "Vincent/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("schema_version") != 1:
        raise RuntimeError("unsupported public bootstrap schema")
    if payload.get("product") != "Vincent":
        raise RuntimeError("bootstrap product mismatch")
    if payload.get("bootstrap_repository") != EXPECTED_BOOTSTRAP_REPOSITORY:
        raise RuntimeError("bootstrap repository mismatch")
    if payload.get("platform_repository") != EXPECTED_BOOTSTRAP_REPOSITORY:
        raise RuntimeError("platform repository mismatch")
    return payload

def load_enrollment_request() -> dict:
    if not ENROLLMENT_REQUEST.is_file():
        raise RuntimeError("local enrollment request is missing; reinstall or use documented identity recovery")
    payload = json.loads(ENROLLMENT_REQUEST.read_text(encoding="utf-8"))
    for field in ("worker_id", "hostname", "public_key", "fingerprint"):
        if not payload.get(field):
            raise RuntimeError(f"invalid enrollment request: missing {field}")
    return payload

def load_authorization(worker_id: str) -> dict | None:
    if not AUTHORIZATION.is_file():
        return None
    payload = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or payload.get("worker_id") != worker_id:
        raise RuntimeError("authorization does not match this worker identity")
    if not isinstance(payload.get("repository_scopes"), list):
        raise RuntimeError("authorization repository scopes are invalid")
    return payload

def write_local_report(instructions: dict, enrollment: dict, authorization: dict | None) -> Path:
    report_root = Path.home() / ".local" / "state" / "vincent"
    report_root.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": 1,
        "product": "Vincent",
        "worker_id": enrollment["worker_id"],
        "hostname": os.uname().nodename,
        "fingerprint": enrollment["fingerprint"],
        "platform_repository": instructions["platform_repository"],
        "git_available": shutil.which("git") is not None,
        "codex_available": shutil.which("codex") is not None,
        "authorized": authorization is not None,
        "repository_scopes": [] if authorization is None else authorization["repository_scopes"],
        "status": "ENROLLMENT_REQUIRED" if authorization is None else "AUTHORIZED",
    }
    path = report_root / "enrollment-report.json"
    path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path

def main() -> int:
    try:
        print("Vincent: reading public bootstrap instructions...")
        instructions = load_instructions()
        enrollment = load_enrollment_request()
        authorization = load_authorization(enrollment["worker_id"])
        report = write_local_report(instructions, enrollment, authorization)
        print(f"Vincent worker: {enrollment['worker_id']}")
        print(f"Hostname: {enrollment['hostname']}")
        print(f"Enrollment fingerprint: {enrollment['fingerprint']}")
        print(f"Local report: {report}")
        if authorization is None:
            print("Enrollment is awaiting explicit owner approval; no private repository access was attempted.")
            return 10
        if shutil.which("codex") is None:
            raise RuntimeError("Codex is missing; first-boot provisioning did not complete")
        workspace = Path.home() / ".local" / "share" / "vincent" / "workspace"
        workspace.mkdir(parents=True, exist_ok=True)
        print("Vincent: authorization verified; starting Codex.")
        return run(["codex"], check=False, cwd=workspace).returncode
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Vincent bootstrap failed: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
