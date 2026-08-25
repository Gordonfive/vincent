import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from mission_control.discovery import DiscoveryError, GitTaskSource


def git(path, *args):
    return subprocess.run(["git", *args], cwd=path, text=True, capture_output=True, check=True).stdout.strip()


def task(task_id, *, priority="NORMAL", assigned=None, capabilities=None):
    return {
        "schema_version": 1, "task_id": task_id, "project_id": "platform",
        "repository": "owner/repo", "base_branch": "main", "objective": "Harmless task",
        "acceptance_criteria": ["tests pass"], "state": "QUEUED", "revision": 1,
        "created_at": "2026-08-24T00:00:00Z", "priority": priority,
        "assigned_worker": assigned, "required_capabilities": capabilities or [],
    }


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.remote = self.root / "remote.git"
        git(self.root, "init", "--bare", str(self.remote))
        seed = self.root / "seed"
        git(self.root, "clone", str(self.remote), str(seed))
        git(seed, "config", "user.name", "Test")
        git(seed, "config", "user.email", "test@example.invalid")
        git(seed, "switch", "-c", "main")
        tasks = seed / "coordination/tasks"
        tasks.mkdir(parents=True)
        for item in (task("LOW", priority="LOW"), task("HIGH", priority="HIGH", capabilities=["python"]), task("OTHER", priority="CRITICAL", assigned="worker-2")):
            (tasks / f"{item['task_id']}.json").write_text(json.dumps(item))
        git(seed, "add", ".")
        git(seed, "commit", "-m", "tasks")
        git(seed, "push", "origin", "main")
        self.checkout = self.root / "worker"
        git(self.root, "clone", "--branch", "main", str(self.remote), str(self.checkout))
        self.source = GitTaskSource(self.checkout)

    def tearDown(self):
        self.temporary.cleanup()

    def test_synchronizes_and_orders_eligible_tasks(self):
        self.source.synchronize()
        eligible = self.source.eligible("worker-1", frozenset({"python"}))
        self.assertEqual([item.task_id for item in eligible], ["HIGH", "LOW"])

    def test_missing_capability_excludes_task(self):
        eligible = self.source.eligible("worker-1", frozenset())
        self.assertEqual([item.task_id for item in eligible], ["LOW"])

    def test_dirty_coordination_checkout_blocks_sync(self):
        (self.checkout / "evidence.log").write_text("preserve\n")
        with self.assertRaises(DiscoveryError):
            self.source.synchronize()
        self.assertTrue((self.checkout / "evidence.log").exists())

    def test_filename_must_match_task_identity(self):
        source = GitTaskSource(self.checkout)
        original = self.checkout / "coordination/tasks/LOW.json"
        original.rename(self.checkout / "coordination/tasks/WRONG.json")
        with self.assertRaises(DiscoveryError):
            source.tasks()


if __name__ == "__main__":
    unittest.main()
