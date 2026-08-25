import subprocess
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from mission_control.claims import Claim, ClaimConflict, ClaimStoreError, GitClaimStore


def git(directory, *arguments):
    return subprocess.run(
        ["git", *arguments], cwd=directory, text=True, capture_output=True, check=True
    )


class GitClaimStoreTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.remote = self.root / "remote.git"
        git(self.root, "init", "--bare", str(self.remote))

    def tearDown(self):
        self.temporary.cleanup()

    def clone(self, name):
        path = self.root / name
        git(self.root, "clone", str(self.remote), str(path))
        return path

    def test_create_and_read_claim(self):
        repository = self.clone("worker")
        store = GitClaimStore(repository)
        claim = Claim("MCP-101", 1, "worker-1", "nonce-1", "a" * 40)
        self.assertEqual(store.create(claim), claim)
        self.assertEqual(store.get(claim.task_id), claim)

    def test_two_independent_workers_cannot_both_claim(self):
        stores = [GitClaimStore(self.clone(f"worker-{index}")) for index in range(2)]

        def attempt(index):
            candidate = Claim("MCP-102", 1, f"worker-{index}", f"nonce-{index}", "b" * 40)
            try:
                stores[index].create(candidate)
                return candidate
            except ClaimConflict:
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, range(2)))
        winners = [result for result in results if result]
        self.assertEqual(len(winners), 1)
        self.assertTrue(stores[0].verify(winners[0]))
        self.assertTrue(stores[1].verify(winners[0]))

    def test_invalid_task_id_cannot_form_a_reference(self):
        store = GitClaimStore(self.clone("worker"))
        with self.assertRaises(ClaimStoreError):
            store.create(Claim("../unsafe", 1, "worker", "nonce", "c" * 40))


if __name__ == "__main__":
    unittest.main()
