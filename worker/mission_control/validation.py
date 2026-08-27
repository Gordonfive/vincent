"""Supervisor-owned validation execution and bounded evidence capture."""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ValidationCommand:
    name: str
    argv: tuple[str, ...]
    timeout_seconds: int = 600


@dataclass(frozen=True, slots=True)
class ValidationResult:
    name: str
    argv: tuple[str, ...]
    started_at: str
    completed_at: str
    exit_status: int | None
    timed_out: bool
    output_sha256: str
    output_excerpt: str

    @property
    def passed(self) -> bool:
        return self.exit_status == 0 and not self.timed_out

    def public_mapping(self) -> dict:
        """Return validation evidence safe for durable coordination reports.

        Captured output remains local/in-memory evidence. It is deliberately not
        serialized into Git-backed task reports because arbitrary validation
        commands may print credentials or other sensitive values.
        """
        return {
            "name": self.name,
            "argv": list(self.argv),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "exit_status": self.exit_status,
            "timed_out": self.timed_out,
            "output_sha256": self.output_sha256,
        }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_validation(command: ValidationCommand, workspace: Path, *, excerpt_limit: int = 4000) -> ValidationResult:
    if not command.argv:
        raise ValueError("validation argv must not be empty")
    started = _now()
    timed_out = False
    status: int | None
    try:
        completed = subprocess.run(
            command.argv,
            cwd=workspace,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=command.timeout_seconds,
            check=False,
        )
        output = completed.stdout
        status = completed.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        status = None
        raw = exc.stdout or ""
        output = raw.decode(errors="replace") if isinstance(raw, bytes) else raw
    completed_at = _now()
    return ValidationResult(
        name=command.name,
        argv=command.argv,
        started_at=started,
        completed_at=completed_at,
        exit_status=status,
        timed_out=timed_out,
        output_sha256=hashlib.sha256(output.encode()).hexdigest(),
        output_excerpt=output[-excerpt_limit:],
    )


def validation_passed(results: tuple[ValidationResult, ...]) -> bool:
    return bool(results) and all(result.passed for result in results)
