import unittest
from concurrent.futures import ThreadPoolExecutor

from mission_control.claims import Claim, ClaimConflict, InMemoryClaimStore


def claim(worker):
    return Claim("MCP-001", 1, worker, f"nonce-{worker}", "a" * 40)


class ClaimTests(unittest.TestCase):
    def test_only_one_concurrent_claim_wins(self):
        store = InMemoryClaimStore()

        def attempt(worker):
            candidate = claim(worker)
            try:
                store.create(candidate)
                return candidate
            except ClaimConflict:
                return None

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(attempt, [f"worker-{i}" for i in range(32)]))

        winners = [result for result in results if result]
        self.assertEqual(len(winners), 1)
        self.assertTrue(store.verify(winners[0]))

    def test_claim_reference_is_task_specific(self):
        self.assertEqual(
            claim("worker-01").reference,
            "refs/mission-control/claims/MCP-001",
        )


if __name__ == "__main__":
    unittest.main()

