"""Small deterministic supervisor core independent of Codex and systemd."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4

from .claims import Claim, ClaimConflict, ClaimStore
from .execution import ExecutionOutcome, ExecutionStatus
from .models import Task, TaskState
from .state_machine import Actor, transition_task


class Executor(Protocol):
    def execute(self, task: Task) -> bool | ExecutionOutcome: ...


@dataclass(slots=True)
class MockExecutor:
    succeed: bool = True
    invocations: int = 0

    def execute(self, task: Task) -> bool:
        self.invocations += 1
        return self.succeed


class Supervisor:
    def __init__(
        self,
        worker_id: str,
        claims: ClaimStore,
        executor: Executor,
    ) -> None:
        self.worker_id = worker_id
        self.claims = claims
        self.executor = executor

    def run_once(self, task: Task, *, source_commit: str) -> Task:
        nonce = uuid4().hex
        claim = Claim(
            task_id=task.task_id,
            task_revision=task.revision,
            worker_id=self.worker_id,
            nonce=nonce,
            source_commit=source_commit,
        )
        try:
            self.claims.create(claim)
        except ClaimConflict:
            return task
        if not self.claims.verify(claim):
            return task

        claimed = transition_task(
            task,
            TaskState.CLAIMING,
            actor=Actor.WORKER,
            claim_worker_id=self.worker_id,
            claim_nonce=nonce,
        )
        active = transition_task(
            claimed,
            TaskState.ACTIVE,
            actor=Actor.WORKER,
            claim_worker_id=self.worker_id,
        )
        outcome = self.executor.execute(active)
        if isinstance(outcome, ExecutionOutcome):
            target = {
                ExecutionStatus.SUCCESS: TaskState.COMPLETED,
                ExecutionStatus.TASK_FAILURE: TaskState.FAILED,
                ExecutionStatus.BLOCKED: TaskState.BLOCKED,
                ExecutionStatus.WAITING_FOR_HUMAN: TaskState.WAITING_FOR_HUMAN,
                ExecutionStatus.USAGE_LIMITED: TaskState.USAGE_LIMITED,
            }[outcome.status]
        else:
            target = TaskState.COMPLETED if outcome else TaskState.FAILED
        return transition_task(
            active,
            target,
            actor=Actor.WORKER,
            claim_worker_id=self.worker_id,
        )
