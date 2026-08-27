"""Crash-safe local operational state and deterministic recovery decisions."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from .models import ProtocolError, TaskState


class RecoveryAction(StrEnum):
    IDLE = "IDLE"
    RECONCILE_REMOTE = "RECONCILE_REMOTE"
    INSPECT_WORKSPACE = "INSPECT_WORKSPACE"
    WAIT = "WAIT"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True, slots=True)
class OperationalState:
    schema_version: int = 1
    worker_id: str = ""
    task_id: str | None = None
    task_revision: int | None = None
    task_state: str | None = None
    claim_nonce: str | None = None
    claim_phase: str | None = None
    source_commit: str | None = None
    branch: str | None = None
    last_checkpoint: str | None = None
    codex_pid: int | None = None
    report_pending: bool = False

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "OperationalState":
        if data.get("schema_version") != 1:
            raise ProtocolError("unsupported operational-state schema")
        worker_id = data.get("worker_id")
        if not isinstance(worker_id, str) or not worker_id:
            raise ProtocolError("operational state requires worker_id")
        task_state = data.get("task_state")
        if task_state is not None:
            try:
                TaskState(task_state)
            except ValueError as exc:
                raise ProtocolError("invalid operational task_state") from exc
        claim_phase = data.get("claim_phase")
        if claim_phase not in {None, "INTENT", "REMOTE_CREATED"}:
            raise ProtocolError("invalid claim_phase")
        if claim_phase is not None and not all(
            isinstance(data.get(field), value_type)
            for field, value_type in (
                ("task_id", str),
                ("task_revision", int),
                ("claim_nonce", str),
                ("source_commit", str),
            )
        ):
            raise ProtocolError("claim intent requires task/revision/nonce/source_commit")
        return cls(**data)


class DurableStateStore:
    """One-record JSON store using write, fsync, rename, and directory fsync."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> OperationalState | None:
        try:
            content = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        try:
            raw = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ProtocolError("operational state is corrupt") from exc
        if not isinstance(raw, Mapping):
            raise ProtocolError("operational state must be an object")
        return OperationalState.from_mapping(raw)

    def save(self, state: OperationalState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        payload = json.dumps(asdict(state), sort_keys=True, indent=2) + "\n"
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self.path.parent,
            prefix=f".{self.path.name}.",
            delete=False,
        ) as temporary:
            temp_path = Path(temporary.name)
            os.chmod(temp_path, 0o600)
            temporary.write(payload)
            temporary.flush()
            os.fsync(temporary.fileno())
        try:
            os.replace(temp_path, self.path)
            self._fsync_parent()
        finally:
            temp_path.unlink(missing_ok=True)

    def clear(self) -> None:
        try:
            self.path.unlink()
        except FileNotFoundError:
            return
        self._fsync_parent()

    def _fsync_parent(self) -> None:
        directory_fd = os.open(self.path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)


def recovery_action(state: OperationalState | None) -> RecoveryAction:
    """Choose only the next safe local action; remote verification happens later."""
    if state is None or state.task_id is None:
        return RecoveryAction.IDLE
    if state.claim_phase is not None:
        return RecoveryAction.RECONCILE_REMOTE
    if state.report_pending:
        return RecoveryAction.ESCALATE
    task_state = TaskState(state.task_state)
    if task_state in {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED, TaskState.SUPERSEDED}:
        return RecoveryAction.IDLE
    if task_state in {TaskState.BLOCKED, TaskState.WAITING_FOR_HUMAN, TaskState.USAGE_LIMITED}:
        return RecoveryAction.WAIT
    if task_state in {TaskState.CLAIMING, TaskState.ACTIVE}:
        return RecoveryAction.RECONCILE_REMOTE
    return RecoveryAction.ESCALATE
