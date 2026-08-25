"""Bounded continuous polling loop suitable for systemd supervision."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Event
from typing import Callable

from .engine import WorkerEngine


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(slots=True)
class WorkerService:
    engine: WorkerEngine
    poll_seconds: int
    stop: Event
    maximum_consecutive_errors: int = 5
    sleeper: Callable[[float], None] = time.sleep
    emit: Callable[[str], None] = print

    def run(self) -> int:
        errors = 0
        self.emit(json.dumps({"event": "WORKER_ONLINE", "timestamp": _timestamp()}))
        while not self.stop.is_set():
            try:
                result = self.engine.run_once()
                errors = 0
                if result is not None:
                    self.emit(json.dumps({"event": "TASK_STATE_CHANGED", "task_id": result.task.task_id, "state": result.task.state.value, "commit": result.coordination_commit, "timestamp": _timestamp()}))
            except Exception as exc:
                errors += 1
                self.emit(json.dumps({"event": "SUPERVISOR_ERROR", "error": type(exc).__name__, "consecutive_errors": errors, "timestamp": _timestamp()}))
                if errors >= self.maximum_consecutive_errors:
                    self.emit(json.dumps({"event": "WORKER_OFFLINE", "reason": "bounded error threshold", "timestamp": _timestamp()}))
                    return 1
            if not self.stop.is_set():
                self.sleeper(self.poll_seconds)
        self.emit(json.dumps({"event": "WORKER_OFFLINE", "reason": "shutdown requested", "timestamp": _timestamp()}))
        return 0
