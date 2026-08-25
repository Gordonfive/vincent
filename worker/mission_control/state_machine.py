"""Authorized task-state transitions for worker protocol v1."""

from __future__ import annotations

from enum import StrEnum

from .models import Task, TaskState


class Actor(StrEnum):
    CONTROL_PLANE = "CONTROL_PLANE"
    WORKER = "WORKER"


class InvalidTransition(ValueError):
    """A requested state transition is not authorized by protocol v1."""


WORKER_TRANSITIONS = {
    TaskState.QUEUED: {TaskState.CLAIMING},
    TaskState.CLAIMING: {TaskState.ACTIVE, TaskState.BLOCKED, TaskState.FAILED},
    TaskState.ACTIVE: {
        TaskState.BLOCKED,
        TaskState.WAITING_FOR_HUMAN,
        TaskState.USAGE_LIMITED,
        TaskState.COMPLETED,
        TaskState.FAILED,
    },
    TaskState.BLOCKED: {TaskState.ACTIVE, TaskState.FAILED},
    TaskState.WAITING_FOR_HUMAN: {TaskState.ACTIVE, TaskState.FAILED},
    TaskState.USAGE_LIMITED: {TaskState.ACTIVE, TaskState.FAILED},
}

CONTROL_TRANSITIONS = {
    TaskState.QUEUED: {TaskState.CANCELLED, TaskState.SUPERSEDED},
    TaskState.CLAIMING: {TaskState.CANCELLED, TaskState.SUPERSEDED},
    TaskState.ACTIVE: {TaskState.CANCELLED, TaskState.SUPERSEDED},
    TaskState.BLOCKED: {TaskState.CANCELLED, TaskState.SUPERSEDED},
    TaskState.WAITING_FOR_HUMAN: {
        TaskState.ACTIVE,
        TaskState.CANCELLED,
        TaskState.SUPERSEDED,
    },
    TaskState.USAGE_LIMITED: {TaskState.CANCELLED, TaskState.SUPERSEDED},
}


def transition_task(
    task: Task,
    target: TaskState,
    *,
    actor: Actor,
    claim_worker_id: str | None = None,
    claim_nonce: str | None = None,
) -> Task:
    allowed = WORKER_TRANSITIONS if actor is Actor.WORKER else CONTROL_TRANSITIONS
    if target not in allowed.get(task.state, set()):
        raise InvalidTransition(f"{actor} cannot transition {task.state} to {target}")

    changes = {}
    if target is TaskState.CLAIMING:
        if not claim_worker_id or not claim_nonce:
            raise InvalidTransition("claim transition requires worker ID and nonce")
        if task.assigned_worker and task.assigned_worker != claim_worker_id:
            raise InvalidTransition("task is explicitly assigned to another worker")
        changes.update(claim_worker_id=claim_worker_id, claim_nonce=claim_nonce)
    elif actor is Actor.WORKER and task.claim_worker_id != claim_worker_id:
        raise InvalidTransition("worker does not own the task claim")

    return task.with_state(target, **changes)

