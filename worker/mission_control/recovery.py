"""Deterministic reconciliation of local evidence with durable remote authority."""

from __future__ import annotations

from dataclasses import dataclass

from .claims import Claim
from .durable_state import OperationalState, RecoveryAction
from .models import Task, TaskState


@dataclass(frozen=True, slots=True)
class WorkspaceSnapshot:
    head: str
    dirty: bool


@dataclass(frozen=True, slots=True)
class RecoveryDecision:
    action: RecoveryAction
    reason: str


def reconcile(
    local: OperationalState,
    remote_task: Task | None,
    remote_claim: Claim | None,
    remote_branch_head: str | None,
    workspace: WorkspaceSnapshot,
) -> RecoveryDecision:
    """Return the safe next action without mutating Git, state, or processes."""
    if local.task_id is None:
        return RecoveryDecision(RecoveryAction.IDLE, "no local task")
    if remote_task is None:
        return RecoveryDecision(RecoveryAction.ESCALATE, "remote task no longer exists")
    if remote_task.task_id != local.task_id:
        return RecoveryDecision(RecoveryAction.ESCALATE, "local and remote task IDs differ")
    if remote_task.state in {TaskState.CANCELLED, TaskState.SUPERSEDED}:
        return RecoveryDecision(RecoveryAction.ESCALATE, f"remote task is {remote_task.state}")
    if remote_task.state in {TaskState.COMPLETED, TaskState.FAILED}:
        return RecoveryDecision(RecoveryAction.IDLE, f"remote task is {remote_task.state}")
    if remote_claim is None:
        return RecoveryDecision(RecoveryAction.ESCALATE, "remote ownership claim is missing")
    if (
        remote_claim.worker_id != local.worker_id
        or remote_claim.nonce != local.claim_nonce
        or remote_claim.task_revision != local.task_revision
    ):
        return RecoveryDecision(RecoveryAction.ESCALATE, "remote ownership does not match local state")
    expected_head = local.last_checkpoint or local.source_commit
    if not expected_head or remote_branch_head != expected_head:
        return RecoveryDecision(RecoveryAction.ESCALATE, "remote branch changed unexpectedly")
    if workspace.head != expected_head or workspace.dirty:
        return RecoveryDecision(
            RecoveryAction.INSPECT_WORKSPACE,
            "workspace contains uncheckpointed or divergent evidence",
        )
    if remote_task.state in {
        TaskState.BLOCKED,
        TaskState.WAITING_FOR_HUMAN,
        TaskState.USAGE_LIMITED,
    }:
        return RecoveryDecision(RecoveryAction.WAIT, f"remote task is {remote_task.state}")
    if remote_task.state in {TaskState.CLAIMING, TaskState.ACTIVE}:
        return RecoveryDecision(RecoveryAction.RECONCILE_REMOTE, "ownership and Git state verified")
    return RecoveryDecision(RecoveryAction.ESCALATE, "remote task state is not resumable")
