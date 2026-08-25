import subprocess
import tempfile
import unittest
from pathlib import Path

from mission_control.publication import GitPublisher, PublicationError


def git(path, *args):
    return subprocess.run(["git", *args], cwd=path, text=True, capture_output=True, check=True).stdout.strip()


class PublicationTests(unittest.TestCase):
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
        (seed / "README.md").write_text("base\n")
        git(seed, "add", "README.md")
        git(seed, "commit", "-m", "base")
        git(seed, "push", "origin", "main")

    def tearDown(self):
        self.temporary.cleanup()

    def worker(self, name):
        path = self.root / name
        git(self.root, "clone", "--branch", "main", str(self.remote), str(path))
        git(path, "config", "user.name", "Worker")
        git(path, "config", "user.email", "worker@example.invalid")
        git(path, "switch", "-c", "task/MCP-501")
        return path

    def test_checkpoint_push_and_remote_verification(self):
        worker = self.worker("worker")
        (worker / "result.txt").write_text("complete\n")
        result = GitPublisher(worker).publish(
            branch="task/MCP-501", expected_remote_head=None,
            paths=("result.txt",), message="Complete MCP-501"
        )
        self.assertEqual(result.ending_commit, result.remote_commit)
        self.assertNotEqual(result.starting_commit, result.ending_commit)

    def test_remote_change_blocks_second_worker_without_force(self):
        first = self.worker("first")
        second = self.worker("second")
        (first / "first.txt").write_text("first\n")
        GitPublisher(first).publish(branch="task/MCP-501", expected_remote_head=None, paths=("first.txt",), message="First")
        (second / "second.txt").write_text("second\n")
        with self.assertRaises(PublicationError):
            GitPublisher(second).publish(branch="task/MCP-501", expected_remote_head=None, paths=("second.txt",), message="Second")
        self.assertTrue((second / "second.txt").exists())

    def test_only_explicit_paths_are_committed(self):
        worker = self.worker("worker")
        (worker / "included.txt").write_text("included\n")
        (worker / "evidence.log").write_text("preserve\n")
        GitPublisher(worker).publish(branch="task/MCP-501", expected_remote_head=None, paths=("included.txt",), message="Explicit")
        self.assertIn("evidence.log", git(worker, "status", "--porcelain"))

    def test_path_escape_is_rejected(self):
        worker = self.worker("worker")
        with self.assertRaises(PublicationError):
            GitPublisher(worker).publish(branch="task/MCP-501", expected_remote_head=None, paths=("../outside",), message="Unsafe")


if __name__ == "__main__":
    unittest.main()
