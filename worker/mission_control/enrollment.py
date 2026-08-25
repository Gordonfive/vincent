"""Local identity generation and owner-reviewable enrollment requests."""

from __future__ import annotations

import json
import os
import socket
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


class EnrollmentError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class EnrollmentRequest:
    schema_version: int
    worker_id: str
    hostname: str
    public_key: str
    fingerprint: str
    requested_at: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, indent=2) + "\n"


def generate_enrollment(identity_root: Path, *, hostname: str | None = None) -> EnrollmentRequest:
    """Generate a new identity once; never overwrite or silently restore one."""
    identity_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    identity_file = identity_root / "identity.json"
    private_key = identity_root / "worker_ed25519"
    request_file = identity_root / "enrollment-request.json"
    if any(path.exists() for path in (identity_file, private_key, private_key.with_suffix(".pub"), request_file)):
        raise EnrollmentError("identity material already exists; explicit recovery is required")
    worker_id = f"worker-{uuid4().hex}"
    generated = subprocess.run(
        ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", worker_id, "-f", str(private_key)],
        text=True,
        capture_output=True,
        check=False,
    )
    if generated.returncode:
        raise EnrollmentError(generated.stderr.strip() or "worker key generation failed")
    os.chmod(private_key, 0o600)
    public_path = Path(f"{private_key}.pub")
    public_key = public_path.read_text(encoding="utf-8").strip()
    fingerprint_result = subprocess.run(
        ["ssh-keygen", "-lf", str(public_path)], text=True, capture_output=True, check=False
    )
    if fingerprint_result.returncode:
        raise EnrollmentError("worker key fingerprint failed")
    fields = fingerprint_result.stdout.split()
    if len(fields) < 2:
        raise EnrollmentError("worker key fingerprint output is invalid")
    request = EnrollmentRequest(
        schema_version=1,
        worker_id=worker_id,
        hostname=hostname or socket.gethostname(),
        public_key=public_key,
        fingerprint=fields[1],
        requested_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )
    identity_file.write_text(json.dumps({"schema_version": 1, "worker_id": worker_id}, indent=2) + "\n")
    request_file.write_text(request.to_json(), encoding="utf-8")
    os.chmod(identity_file, 0o600)
    os.chmod(request_file, 0o600)
    return request
