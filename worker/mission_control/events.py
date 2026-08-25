"""Ephemeral event and heartbeat interfaces; neither is authoritative state."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Protocol


class EventType(StrEnum):
    WORKER_ONLINE = "WORKER_ONLINE"
    WORKER_OFFLINE = "WORKER_OFFLINE"
    TASK_STARTED = "TASK_STARTED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_FAILED = "TASK_FAILED"
    TASK_BLOCKED = "TASK_BLOCKED"
    HUMAN_DECISION_REQUIRED = "HUMAN_DECISION_REQUIRED"
    USAGE_LIMITED = "USAGE_LIMITED"
    TASK_RESUMED = "TASK_RESUMED"
    SUPERVISOR_ERROR = "SUPERVISOR_ERROR"


@dataclass(frozen=True, slots=True)
class Event:
    event: EventType
    timestamp: str
    worker_id: str
    task_id: str | None = None
    details: dict | None = None

    @classmethod
    def create(cls, event: EventType, worker_id: str, task_id: str | None = None, details: dict | None = None):
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        return cls(event, timestamp, worker_id, task_id, details)

    def to_json(self) -> str:
        data = asdict(self)
        data["event"] = self.event.value
        return json.dumps(data, sort_keys=True)


class EventSink(Protocol):
    def emit(self, event: Event) -> None: ...


@dataclass(frozen=True, slots=True)
class Heartbeat:
    worker_id: str
    timestamp: str
    supervisor_version: str
    state: str
    current_task: str | None
    resource_summary: dict


class HeartbeatFile:
    """Low-frequency, machine-local presence signal under /run or equivalent."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, heartbeat: Heartbeat) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(asdict(heartbeat), sort_keys=True, indent=2) + "\n"
        with NamedTemporaryFile("w", dir=self.path.parent, prefix=f".{self.path.name}.", delete=False) as temporary:
            temporary.write(payload)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_path = Path(temporary.name)
        try:
            os.chmod(temporary_path, 0o600)
            os.replace(temporary_path, self.path)
        finally:
            temporary_path.unlink(missing_ok=True)
