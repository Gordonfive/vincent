import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mission_control.codex_runner import CodexFailure, CodexResult, ValidatedCodexExecutor
from mission_control.execution import ExecutionStatus
from mission_control.models import Task
from mission_control.validation import ValidationCommand


def task():
    return Task.from_mapping({"schema_version": 1, "task_id": "MCP-801", "project_id": "platform", "repository": "owner/repo", "base_branch": "main", "objective": "Implement safely", "acceptance_criteria": ["unit tests pass"], "state": "QUEUED", "revision": 1, "created_at": "2026-08-24T00:00:00Z"})


class FakeRunner:
    def __init__(self, result):
        self.result = result
        self.prompt = None

    def execute(self, workspace, prompt):
        self.prompt = prompt
        return self.result


class ValidatedExecutorTests(unittest.TestCase):
    def test_success_requires_independent_validation(self):
        runner = FakeRunner(CodexResult(0, (), "", None))
        with tempfile.TemporaryDirectory() as directory:
            executor = ValidatedCodexExecutor(runner, Path(directory), (ValidationCommand("unit", (sys.executable, "-c", "pass")),))
            outcome = executor.execute(task())
        self.assertEqual(outcome.status, ExecutionStatus.SUCCESS)
        self.assertIn("Do not push or merge", runner.prompt)
        self.assertTrue(executor.last_validation[0].passed)

    def test_validation_failure_overrides_codex_success(self):
        runner = FakeRunner(CodexResult(0, (), "", None))
        with tempfile.TemporaryDirectory() as directory:
            executor = ValidatedCodexExecutor(runner, Path(directory), (ValidationCommand("unit", (sys.executable, "-c", "raise SystemExit(1)")),))
            outcome = executor.execute(task())
        self.assertEqual(outcome.status, ExecutionStatus.TASK_FAILURE)

    def test_usage_limit_is_preserved_as_operational_state(self):
        runner = FakeRunner(CodexResult(1, (), "limit", CodexFailure.USAGE_LIMIT))
        with tempfile.TemporaryDirectory() as directory:
            executor = ValidatedCodexExecutor(runner, Path(directory), ())
            outcome = executor.execute(task())
        self.assertEqual(outcome.status, ExecutionStatus.USAGE_LIMITED)
        self.assertEqual(executor.last_validation, ())

    def test_authentication_failure_blocks_instead_of_retrying_task(self):
        runner = FakeRunner(CodexResult(1, (), "auth", CodexFailure.AUTHENTICATION_FAILURE))
        with tempfile.TemporaryDirectory() as directory:
            outcome = ValidatedCodexExecutor(runner, Path(directory), ()).execute(task())
        self.assertEqual(outcome.status, ExecutionStatus.BLOCKED)


if __name__ == "__main__":
    unittest.main()
