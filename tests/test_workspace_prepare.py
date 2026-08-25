import subprocess
import tempfile
import unittest
from pathlib import Path

from mission_control.workspace import WorkspaceError, WorkspaceManager


def git(path, *args):
    return subprocess.run(["git", *args], cwd=path, text=True, capture_output=True, check=True).stdout.strip()


class WorkspacePrepareTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.remote = self.root / "project.git"
        git(self.root, "init", "--bare", str(self.remote))
        seed = self.root / "seed"
        git(self.root, "clone", str(self.remote), str(seed))
        git(seed, "config", "user.name", "Test")
        git(seed, "config", "user.email", "test@example.invalid")
        git(seed, "switch", "-c", "main")
        (seed / "README.md").write_text("base\n")
        git(seed, "add", ".")
        git(seed, "commit", "-m", "base")
        git(seed, "push", "origin", "main")
        self.manager = WorkspaceManager(self.root / "worktrees")

    def tearDown(self):
        self.temporary.cleanup()

    def prepare(self):
        return self.manager.prepare(project_id="platform", repository=str(self.remote), base_branch="main", worker_id="worker-1", task_id="MCP-901")

    def test_creates_isolated_task_branch_from_remote_base(self):
        prepared = self.prepare()
        self.assertTrue(prepared.path.is_dir())
        self.assertTrue(prepared.branch.startswith("mission-control/"))
        self.assertEqual(git(prepared.path, "rev-parse", "HEAD"), prepared.starting_commit)
        self.assertEqual(git(prepared.path, "status", "--porcelain"), "")

    def test_clean_existing_workspace_is_reused(self):
        first = self.prepare()
        second = self.prepare()
        self.assertEqual(first, second)

    def test_dirty_existing_workspace_is_preserved_and_blocks_reuse(self):
        prepared = self.prepare()
        evidence = prepared.path / "evidence.log"
        evidence.write_text("preserve\n")
        with self.assertRaises(WorkspaceError):
            self.prepare()
        self.assertTrue(evidence.exists())

    def test_owner_repo_locator_maps_to_private_ssh_style(self):
        self.assertEqual(
            WorkspaceManager.repository_url("owner/project"),
            "git@github.com:owner/project.git",
        )


if __name__ == "__main__":
    unittest.main()
