"""One-cycle worker engine joining discovery, claiming, state, and execution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from .claims import Claim, ClaimConflict, ClaimStore
from .discovery import GitTaskSource
from .durable_state import DurableStateStore, OperationalState
from .execution import ExecutionOutcome, ExecutionStatus
from .models import Task, TaskState
from .state_machine import Actor, transition_task
from .supervisor import Executor
from typing import Callable
from .task_repository import TaskRepository


@dataclass(frozen=True, slots=True)
class EngineResult:
    task: Task
    coordination_commit: str


class WorkerEngine:
    def __init__(
        self,
        *,
        worker_id: str,
        capabilities: frozenset[str],
        source: GitTaskSource,
        task_repository: TaskRepository,
        claims: ClaimStore,
        state: DurableStateStore,
        executor: Executor | None = None,
        executor_factory: Callable[[Task], Executor] | None = None,
        reporter: Callable[[Task, ExecutionOutcome, Executor, str, str, str], str] | None = None,
    ) -> None:
        self.worker_id = worker_id
        self.capabilities = capabilities
        self.source = source
        self.task_repository = task_repository
        self.claims = claims
        self.state = state
        self.executor = executor
        self.executor_factory = executor_factory
        self.reporter = reporter
        if self.executor is None and self.executor_factory is None:
            raise ValueError("worker engine requires an executor or executor factory")

    def run_once(self) -> EngineResult | None:
        started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        source_commit = self.source.synchronize()
        candidates = self.source.eligible(self.worker_id, self.capabilities)
        for task in candidates:
            nonce = uuid4().hex
            claim = Claim(task.task_id, task.revision, self.worker_id, nonce, source_commit)
            try:
                self.claims.create(claim)
            except ClaimConflict:
                continue
            if not self.claims.verify(claim):
                continue
            claiming = transition_task(
                task, TaskState.CLAIMING, actor=Actor.WORKER,
                claim_worker_id=self.worker_id, claim_nonce=nonce,
            )
            published = self.task_repository.publish(claiming, expected_commit=source_commit)
            active = transition_task(
                claiming, TaskState.ACTIVE, actor=Actor.WORKER,
                claim_worker_id=self.worker_id,
            )
            published = self.task_repository.publish(active, expected_commit=published.ending_commit)
            self.state.save(
                OperationalState(
                    worker_id=self.worker_id,
                    task_id=task.task_id,
                    task_revision=task.revision,
                    task_state=active.state.value,
                    claim_nonce=nonce,
                    source_commit=source_commit,
                    report_pending=False,
                )
            )
            try:
                executor = self.executor_factory(active) if self.executor_factory else self.executor
                assert executor is not None
                outcome = executor.execute(active)
            except Exception:
                outcome = ExecutionOutcome(ExecutionStatus.TASK_FAILURE, "executor raised an exception")
            if isinstance(outcome, ExecutionOutcome):
                normalized = outcome
                target = {
                    ExecutionStatus.SUCCESS: TaskState.COMPLETED,
                    ExecutionStatus.TASK_FAILURE: TaskState.FAILED,
                    ExecutionStatus.BLOCKED: TaskState.BLOCKED,
                    ExecutionStatus.WAITING_FOR_HUMAN: TaskState.WAITING_FOR_HUMAN,
                    ExecutionStatus.USAGE_LIMITED: TaskState.USAGE_LIMITED,
                }[outcome.status]
            else:
                normalized = ExecutionOutcome(
                    ExecutionStatus.SUCCESS if outcome else ExecutionStatus.TASK_FAILURE,
                    "legacy boolean executor result",
                )
                target = TaskState.COMPLETED if outcome else TaskState.FAILED
            terminal = transition_task(
                active, target, actor=Actor.WORKER,
                claim_worker_id=self.worker_id,
            )
            published = self.task_repository.publish(terminal, expected_commit=published.ending_commit)
            self.state.save(
                OperationalState(
                    worker_id=self.worker_id,
                    task_id=task.task_id,
                    task_revision=task.revision,
                    task_state=terminal.state.value,
                    claim_nonce=nonce,
                    source_commit=source_commit,
                    report_pending=self.reporter is not None,
                )
            )
            if self.reporter is not None:
                completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                report_commit = self.reporter(
                    terminal, normalized, executor, published.ending_commit, started_at, completed_at
                )
                published = type(published)(
                    published.starting_commit,
                    report_commit,
                    report_commit,
                    published.branch,
                )
                self.state.save(
                    OperationalState(
                        worker_id=self.worker_id,
                        task_id=task.task_id,
                        task_revision=task.revision,
                        task_state=terminal.state.value,
                        claim_nonce=nonce,
                        source_commit=source_commit,
                        report_pending=False,
                    )
                )
            return EngineResult(terminal, published.ending_commit)
        return None
