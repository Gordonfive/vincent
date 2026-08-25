import subprocess
import tempfile
import unittest
from pathlib import Path

from mission_control.workspace import WorkspaceError, WorkspaceManager, stable_identifier


def git(path, *args):
    return subprocess.run(["git", *args], cwd=path, text=True, capture_output=True, check=True).stdout.strip()


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.workspaces = self.root / "worktrees"
        self.repository = self.workspaces / "project-worker-task"
        self.repository.mkdir(parents=True)
        git(self.repository, "init", "-b", "task/MCP-301")
        git(self.repository, "config", "user.name", "Test")
        git(self.repository, "config", "user.email", "test@example.invalid")
        git(self.repository, "remote", "add", "origin", "git@example.invalid:owner/repo.git")
        (self.repository / "README.md").write_text("test\n")
        git(self.repository, "add", "README.md")
        git(self.repository, "commit", "-m", "initial")
        self.manager = WorkspaceManager(self.workspaces)

    def tearDown(self):
        self.temporary.cleanup()

    def inspect(self, **changes):
        arguments = {"expected_remote": "git@example.invalid:owner/repo.git", "expected_branch": "task/MCP-301"}
        arguments.update(changes)
        return self.manager.inspect(self.repository, **arguments)

    def test_clean_workspace_is_accepted(self):
        status = self.inspect()
        self.assertTrue(status.clean)
        self.manager.require_clean(status)

    def test_untracked_file_is_preserved_and_blocks_reuse(self):
        (self.repository / "evidence.log").write_text("useful evidence\n")
        status = self.inspect()
        self.assertFalse(status.clean)
        with self.assertRaises(WorkspaceError):
            self.manager.require_clean(status)
        self.assertTrue((self.repository / "evidence.log").exists())

    def test_wrong_remote_is_rejected(self):
        with self.assertRaises(WorkspaceError):
            self.inspect(expected_remote="git@example.invalid:other/repo.git")

    def test_wrong_commit_is_rejected(self):
        with self.assertRaises(WorkspaceError):
            self.inspect(expected_head="0" * 40)

    def test_identifier_is_stable_unique_and_ddev_safe(self):
        first = stable_identifier("Ketchikan.net", "Worker Heavy 01", "KTN/204")
        self.assertEqual(first, stable_identifier("Ketchikan.net", "Worker Heavy 01", "KTN/204"))
        self.assertNotEqual(first, stable_identifier("Ketchikan.net", "Worker Heavy 02", "KTN/204"))
        self.assertLessEqual(len(first), 63)
        self.assertRegex(first, r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


if __name__ == "__main__":
    unittest.main()
