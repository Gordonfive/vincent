import unittest

from mission_control.claims import InMemoryClaimStore
from mission_control.models import Task, TaskState
from mission_control.supervisor import MockExecutor, Supervisor
from test_models import valid_task


class SupervisorTests(unittest.TestCase):
    def test_winner_executes_and_completes(self):
        executor = MockExecutor()
        supervisor = Supervisor("worker-01", InMemoryClaimStore(), executor)
        result = supervisor.run_once(Task.from_mapping(valid_task()), source_commit="a" * 40)
        self.assertIs(result.state, TaskState.COMPLETED)
        self.assertEqual(executor.invocations, 1)

    def test_loser_never_invokes_executor(self):
        store = InMemoryClaimStore()
        first = MockExecutor()
        second = MockExecutor()
        task = Task.from_mapping(valid_task())
        Supervisor("worker-01", store, first).run_once(task, source_commit="a" * 40)
        result = Supervisor("worker-02", store, second).run_once(
            task, source_commit="a" * 40
        )
        self.assertIs(result.state, TaskState.QUEUED)
        self.assertEqual(first.invocations, 1)
        self.assertEqual(second.invocations, 0)

    def test_failed_execution_is_reported_as_failed_state(self):
        executor = MockExecutor(succeed=False)
        supervisor = Supervisor("worker-01", InMemoryClaimStore(), executor)
        result = supervisor.run_once(Task.from_mapping(valid_task()), source_commit="a" * 40)
        self.assertIs(result.state, TaskState.FAILED)


if __name__ == "__main__":
    unittest.main()
