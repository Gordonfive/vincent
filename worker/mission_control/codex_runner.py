"""Noninteractive Codex boundary with explicit interruption classification."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable

from .execution import ExecutionOutcome, ExecutionStatus
from .models import Task
from .validation import ValidationCommand, ValidationResult, run_validation, validation_passed


class CodexFailure(StrEnum):
    TRANSIENT_CODEX_FAILURE = "TRANSIENT_CODEX_FAILURE"
    AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"
    USAGE_LIMIT = "USAGE_LIMIT"
    TASK_FAILURE = "TASK_FAILURE"
    UNKNOWN_FAILURE = "UNKNOWN_FAILURE"


@dataclass(frozen=True, slots=True)
class CodexResult:
    exit_status: int | None
    events: tuple[dict, ...]
    stderr: str
    failure: CodexFailure | None

    @property
    def succeeded(self) -> bool:
        return self.exit_status == 0 and self.failure is None


def classify_failure(exit_status: int | None, text: str) -> CodexFailure | None:
    if exit_status == 0:
        return None
    normalized = text.lower()
    if any(marker in normalized for marker in ("usage limit", "rate limit", "quota exceeded", "capacity")):
        return CodexFailure.USAGE_LIMIT
    if any(marker in normalized for marker in ("unauthorized", "authentication", "not logged in", "invalid api key")):
        return CodexFailure.AUTHENTICATION_FAILURE
    if any(marker in normalized for marker in ("timed out", "connection reset", "temporarily unavailable")):
        return CodexFailure.TRANSIENT_CODEX_FAILURE
    if any(marker in normalized for marker in ("task failed", "turn.failed")):
        return CodexFailure.TASK_FAILURE
    return CodexFailure.UNKNOWN_FAILURE


class CodexRunner:
    def __init__(
        self,
        executable: str = "codex",
        process_runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    ) -> None:
        self.executable = executable
        self.process_runner = process_runner

    def execute(self, workspace: Path, prompt: str) -> CodexResult:
        command = [
            self.executable,
            "exec",
            "--json",
            "--sandbox",
            "workspace-write",
            "-",
        ]
        try:
            completed = self.process_runner(
                command,
                cwd=workspace,
                input=prompt,
                text=True,
                capture_output=True,
                check=False,
            )
        except FileNotFoundError:
            return CodexResult(None, (), "Codex executable not found", CodexFailure.UNKNOWN_FAILURE)
        events: list[dict] = []
        invalid_lines: list[str] = []
        for line in completed.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                invalid_lines.append(line)
                continue
            if isinstance(event, dict):
                events.append(event)
        evidence = "\n".join([completed.stderr, *invalid_lines, *(json.dumps(e) for e in events)])
        failure = classify_failure(completed.returncode, evidence)
        return CodexResult(completed.returncode, tuple(events), completed.stderr, failure)


def retry_allowed(failure: CodexFailure | None, attempt: int, *, maximum_attempts: int = 3) -> bool:
    return failure is CodexFailure.TRANSIENT_CODEX_FAILURE and attempt < maximum_attempts


class ValidatedCodexExecutor:
    """Run Codex in one prepared workspace, then independently validate its work."""

    def __init__(
        self,
        runner: CodexRunner,
        workspace: Path,
        validations: tuple[ValidationCommand, ...],
    ) -> None:
        self.runner = runner
        self.workspace = workspace
        self.validations = validations
        self.last_codex_result: CodexResult | None = None
        self.last_validation: tuple[ValidationResult, ...] = ()

    @staticmethod
    def prompt(task: Task) -> str:
        acceptance = "\n".join(f"- {criterion}" for criterion in task.acceptance_criteria)
        forbidden = "\n".join(f"- {action}" for action in task.forbidden_actions) or "- None specified"
        return (
            f"Task ID: {task.task_id}\nObjective: {task.objective}\n\n"
            f"Acceptance criteria:\n{acceptance}\n\nForbidden actions:\n{forbidden}\n\n"
            "Work only in the prepared repository. Preserve unexpected state. Do not push or merge; "
            "the supervisor owns validation and Git publication."
        )

    def execute(self, task: Task) -> ExecutionOutcome:
        self.last_codex_result = self.runner.execute(self.workspace, self.prompt(task))
        if not self.last_codex_result.succeeded:
            status = {
                CodexFailure.USAGE_LIMIT: ExecutionStatus.USAGE_LIMITED,
                CodexFailure.AUTHENTICATION_FAILURE: ExecutionStatus.BLOCKED,
                CodexFailure.TASK_FAILURE: ExecutionStatus.TASK_FAILURE,
                CodexFailure.TRANSIENT_CODEX_FAILURE: ExecutionStatus.BLOCKED,
                CodexFailure.UNKNOWN_FAILURE: ExecutionStatus.BLOCKED,
            }[self.last_codex_result.failure]
            return ExecutionOutcome(status, self.last_codex_result.failure.value)
        self.last_validation = tuple(
            run_validation(command, self.workspace) for command in self.validations
        )
        if not validation_passed(self.last_validation):
            return ExecutionOutcome(ExecutionStatus.TASK_FAILURE, "independent validation failed")
        return ExecutionOutcome(ExecutionStatus.SUCCESS, "Codex and independent validation passed")
