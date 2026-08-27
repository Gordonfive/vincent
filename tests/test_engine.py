import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from mission_control.claims import ClaimConflict, GitClaimStore
from mission_control.discovery import GitTaskSource
from mission_control.durable_state import DurableStateStore
from mission_control.engine import WorkerEngine
from mission_control.models import TaskState
from mission_control.supervisor import MockExecutor
from mission_control.task_repository import TaskRepository


def git(path, *args):
    return subprocess.run(["git", *args], cwd=path, text=True, capture_output=True, check=True).stdout.strip()


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        remote = self.root / "remote.git"
        git(self.root, "init", "--bare", str(remote))
        seed = self.root / "seed"
        git(self.root, "clone", str(remote), str(seed))
        git(seed, "config", "user.name", "Test")
        git(seed, "config", "user.email", "test@example.invalid")
        git(seed, "switch", "-c", "main")
        task = {"schema_version": 1, "task_id": "MCP-701", "project_id": "platform", "repository": "owner/repo", "base_branch": "main", "objective": "Run harmless executor", "acceptance_criteria": ["terminal state durable"], "state": "QUEUED", "revision": 1, "created_at": "2026-08-24T00:00:00Z"}
        path = seed / "coordination/tasks/MCP-701.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(task))
        git(seed, "add", ".")
        git(seed, "commit", "-m", "queue task")
        git(seed, "push", "origin", "main")
        self.checkout = self.root / "worker"
        git(self.root, "clone", "--branch", "main", str(remote), str(self.checkout))
        git(self.checkout, "config", "user.name", "Worker")
        git(self.checkout, "config", "user.email", "worker@example.invalid")
        self.state = DurableStateStore(self.root / "state.json")

    def tearDown(self):
        self.temporary.cleanup()

    def engine(self, executor, claims=None):
        return WorkerEngine(
            worker_id="worker-1", capabilities=frozenset(),
            source=GitTaskSource(self.checkout), task_repository=TaskRepository(self.checkout),
            claims=claims or GitClaimStore(self.checkout),
            state=self.state, executor=executor, available_ram_gb=16,
        )

    def test_harmless_task_reaches_durable_completed_state(self):
        executor = MockExecutor()
        result = self.engine(executor).run_once()
        self.assertEqual(result.task.state, TaskState.COMPLETED)
        self.assertEqual(executor.invocations, 1)
        self.assertEqual(GitTaskSource(self.checkout).tasks()[0].state, TaskState.COMPLETED)
        state = self.state.load()
        self.assertEqual(state.task_state, "COMPLETED")
        self.assertIsNone(state.claim_phase)

    def test_executor_failure_reaches_durable_failed_state(self):
        result = self.engine(MockExecutor(succeed=False)).run_once()
        self.assertEqual(result.task.state, TaskState.FAILED)

    def test_terminal_task_is_not_executed_again(self):
        executor = MockExecutor()
        engine = self.engine(executor)
        engine.run_once()
        self.assertIsNone(engine.run_once())
        self.assertEqual(executor.invocations, 1)

    def test_abrupt_termination_preserves_active_recovery_evidence(self):
        class InterruptedExecutor:
            def execute(self, task):
                raise KeyboardInterrupt

        with self.assertRaises(KeyboardInterrupt):
            self.engine(InterruptedExecutor()).run_once()
        self.assertEqual(GitTaskSource(self.checkout).tasks()[0].state, TaskState.ACTIVE)
        state = self.state.load()
        self.assertEqual(state.task_state, "ACTIVE")
        self.assertEqual(state.task_id, "MCP-701")

    def test_ambiguous_claim_creation_preserves_preclaim_intent(self):
        class AmbiguousClaims:
            def create(self, claim):
                raise RuntimeError("network outcome unknown")
            def get(self, task_id):
                return None
            def verify(self, claim):
                return False

        with self.assertRaisesRegex(RuntimeError, "outcome unknown"):
            self.engine(MockExecutor(), claims=AmbiguousClaims()).run_once()
        state = self.state.load()
        self.assertEqual(state.claim_phase, "INTENT")
        self.assertEqual(state.task_state, "QUEUED")
        self.assertTrue(state.claim_nonce)

    def test_unverified_created_claim_preserves_remote_created_state(self):
        class UnverifiedClaims:
            def create(self, claim):
                self.claim = claim
                return claim
            def get(self, task_id):
                return getattr(self, "claim", None)
            def verify(self, claim):
                return False

        result = self.engine(MockExecutor(), claims=UnverifiedClaims()).run_once()
        self.assertIsNone(result)
        state = self.state.load()
        self.assertEqual(state.claim_phase, "REMOTE_CREATED")
        self.assertEqual(state.task_state, "QUEUED")

    def test_claim_conflict_clears_only_local_preclaim_intent(self):
        class ConflictingClaims:
            def create(self, claim):
                raise ClaimConflict(claim.reference)
            def get(self, task_id):
                return None
            def verify(self, claim):
                return False

        self.assertIsNone(self.engine(MockExecutor(), claims=ConflictingClaims()).run_once())
        self.assertIsNone(self.state.load())


if __name__ == "__main__":
    unittest.main()
