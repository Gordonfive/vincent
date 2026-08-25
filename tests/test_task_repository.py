import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from mission_control.discovery import GitTaskSource
from mission_control.models import TaskState
from mission_control.publication import PublicationError
from mission_control.state_machine import Actor, transition_task
from mission_control.task_repository import TaskRepository


def git(path, *args):
    return subprocess.run(["git", *args], cwd=path, text=True, capture_output=True, check=True).stdout.strip()


class TaskRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        remote = root / "remote.git"
        git(root, "init", "--bare", str(remote))
        seed = root / "seed"
        git(root, "clone", str(remote), str(seed))
        git(seed, "config", "user.name", "Test")
        git(seed, "config", "user.email", "test@example.invalid")
        git(seed, "switch", "-c", "main")
        path = seed / "coordination/tasks/MCP-601.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"schema_version": 1, "task_id": "MCP-601", "project_id": "platform", "repository": "owner/repo", "base_branch": "main", "objective": "Update state", "acceptance_criteria": ["state durable"], "state": "QUEUED", "revision": 1, "created_at": "2026-08-24T00:00:00Z"}))
        git(seed, "add", ".")
        git(seed, "commit", "-m", "task")
        git(seed, "push", "origin", "main")
        self.checkout = root / "worker"
        git(root, "clone", "--branch", "main", str(remote), str(self.checkout))
        git(self.checkout, "config", "user.name", "Worker")
        git(self.checkout, "config", "user.email", "worker@example.invalid")

    def tearDown(self):
        self.temporary.cleanup()

    def test_transition_is_committed_pushed_and_readable(self):
        source = GitTaskSource(self.checkout)
        starting = source.synchronize()
        queued = source.tasks()[0]
        claiming = transition_task(queued, TaskState.CLAIMING, actor=Actor.WORKER, claim_worker_id="worker-1", claim_nonce="nonce")
        result = TaskRepository(self.checkout).publish(claiming, expected_commit=starting)
        self.assertEqual(result.ending_commit, result.remote_commit)
        stored = GitTaskSource(self.checkout).tasks()[0]
        self.assertEqual(stored.state, TaskState.CLAIMING)
        self.assertEqual(stored.revision, 2)

    def test_stale_expected_commit_is_rejected(self):
        source = GitTaskSource(self.checkout)
        queued = source.tasks()[0]
        claiming = transition_task(queued, TaskState.CLAIMING, actor=Actor.WORKER, claim_worker_id="worker-1", claim_nonce="nonce")
        with self.assertRaises(PublicationError):
            TaskRepository(self.checkout).publish(claiming, expected_commit="0" * 40)


if __name__ == "__main__":
    unittest.main()
