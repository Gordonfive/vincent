"""Execution outcomes richer than a process boolean."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ExecutionStatus(StrEnum):
    SUCCESS = "SUCCESS"
    TASK_FAILURE = "TASK_FAILURE"
    BLOCKED = "BLOCKED"
    WAITING_FOR_HUMAN = "WAITING_FOR_HUMAN"
    USAGE_LIMITED = "USAGE_LIMITED"


@dataclass(frozen=True, slots=True)
class ExecutionOutcome:
    status: ExecutionStatus
    reason: str = ""
