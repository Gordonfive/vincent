import unittest

from mission_control.models import Task, TaskState
from mission_control.state_machine import Actor, InvalidTransition, transition_task
from test_models import valid_task


class StateMachineTests(unittest.TestCase):
    def test_worker_claims_then_activates_own_task(self):
        task = Task.from_mapping(valid_task())
        claimed = transition_task(
            task,
            TaskState.CLAIMING,
            actor=Actor.WORKER,
            claim_worker_id="worker-01",
            claim_nonce="nonce-01",
        )
        active = transition_task(
            claimed,
            TaskState.ACTIVE,
            actor=Actor.WORKER,
            claim_worker_id="worker-01",
        )
        self.assertIs(active.state, TaskState.ACTIVE)
        self.assertEqual(active.revision, 3)

    def test_non_owner_cannot_advance_claim(self):
        claimed = Task.from_mapping(
            valid_task(
                state="CLAIMING",
                claim_worker_id="worker-01",
                claim_nonce="nonce-01",
            )
        )
        with self.assertRaisesRegex(InvalidTransition, "does not own"):
            transition_task(
                claimed,
                TaskState.ACTIVE,
                actor=Actor.WORKER,
                claim_worker_id="worker-02",
            )

    def test_explicit_assignment_is_respected(self):
        task = Task.from_mapping(valid_task(assigned_worker="worker-02"))
        with self.assertRaisesRegex(InvalidTransition, "assigned"):
            transition_task(
                task,
                TaskState.CLAIMING,
                actor=Actor.WORKER,
                claim_worker_id="worker-01",
                claim_nonce="nonce-01",
            )

    def test_control_plane_can_cancel_but_worker_cannot(self):
        task = Task.from_mapping(valid_task())
        cancelled = transition_task(
            task, TaskState.CANCELLED, actor=Actor.CONTROL_PLANE
        )
        self.assertIs(cancelled.state, TaskState.CANCELLED)
        with self.assertRaises(InvalidTransition):
            transition_task(task, TaskState.CANCELLED, actor=Actor.WORKER)

    def test_terminal_task_cannot_transition(self):
        task = Task.from_mapping(valid_task(state="COMPLETED"))
        with self.assertRaises(InvalidTransition):
            transition_task(task, TaskState.ACTIVE, actor=Actor.CONTROL_PLANE)


if __name__ == "__main__":
    unittest.main()
