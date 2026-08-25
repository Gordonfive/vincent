import unittest

from mission_control.claims import Claim
from mission_control.durable_state import OperationalState, RecoveryAction
from mission_control.models import Task
from mission_control.recovery import WorkspaceSnapshot, reconcile


def task(state="ACTIVE"):
    claimed = state in {"CLAIMING", "ACTIVE"}
    return Task.from_mapping({"schema_version": 1, "task_id": "MCP-201", "project_id": "platform", "repository": "owner/repo", "base_branch": "main", "objective": "Test recovery", "acceptance_criteria": ["tests pass"], "state": state, "revision": 2, "created_at": "2026-08-24T00:00:00Z", "claim_worker_id": "worker-1" if claimed else None, "claim_nonce": "nonce-1" if claimed else None})


def local():
    return OperationalState(worker_id="worker-1", task_id="MCP-201", task_revision=1, task_state="ACTIVE", claim_nonce="nonce-1", source_commit="a" * 40)


def claim(worker="worker-1", nonce="nonce-1"):
    return Claim("MCP-201", 1, worker, nonce, "a" * 40)


class RecoveryTests(unittest.TestCase):
    def decide(self, remote_task=None, remote_claim=None, branch=None, dirty=False, head=None):
        return reconcile(local(), task() if remote_task is None else remote_task, claim() if remote_claim is None else remote_claim, "a" * 40 if branch is None else branch, WorkspaceSnapshot("a" * 40 if head is None else head, dirty))

    def test_verified_active_task_is_eligible_for_resume(self):
        self.assertEqual(self.decide().action, RecoveryAction.RECONCILE_REMOTE)

    def test_lost_claim_escalates(self):
        self.assertEqual(self.decide(remote_claim=claim(worker="worker-2")).action, RecoveryAction.ESCALATE)

    def test_cancelled_task_never_resumes(self):
        self.assertEqual(self.decide(remote_task=task("CANCELLED")).action, RecoveryAction.ESCALATE)

    def test_remote_branch_change_escalates(self):
        self.assertEqual(self.decide(branch="b" * 40).action, RecoveryAction.ESCALATE)

    def test_dirty_workspace_is_preserved_for_inspection(self):
        self.assertEqual(self.decide(dirty=True).action, RecoveryAction.INSPECT_WORKSPACE)

    def test_missing_remote_task_escalates(self):
        decision = reconcile(local(), None, claim(), "a" * 40, WorkspaceSnapshot("a" * 40, False))
        self.assertEqual(decision.action, RecoveryAction.ESCALATE)


if __name__ == "__main__":
    unittest.main()
