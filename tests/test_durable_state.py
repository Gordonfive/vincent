import json
import tempfile
import unittest
from pathlib import Path

from mission_control.durable_state import (
    DurableStateStore,
    OperationalState,
    RecoveryAction,
    recovery_action,
)
from mission_control.models import ProtocolError


class DurableStateTests(unittest.TestCase):
    def test_missing_state_is_idle(self):
        with tempfile.TemporaryDirectory() as directory:
            store = DurableStateStore(Path(directory) / "state.json")
            self.assertIsNone(store.load())
            self.assertEqual(recovery_action(store.load()), RecoveryAction.IDLE)

    def test_round_trip_and_permissions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state" / "worker.json"
            state = OperationalState(
                worker_id="worker-01",
                task_id="TASK-1",
                task_revision=2,
                task_state="ACTIVE",
                claim_nonce="nonce",
                source_commit="a" * 40,
            )
            store = DurableStateStore(path)
            store.save(state)
            self.assertEqual(store.load(), state)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_active_requires_remote_reconciliation(self):
        state = OperationalState(worker_id="worker-01", task_id="T", task_state="ACTIVE")
        self.assertEqual(recovery_action(state), RecoveryAction.RECONCILE_REMOTE)

    def test_waiting_state_does_not_restart_execution(self):
        state = OperationalState(
            worker_id="worker-01", task_id="T", task_state="WAITING_FOR_HUMAN"
        )
        self.assertEqual(recovery_action(state), RecoveryAction.WAIT)

    def test_corrupt_state_is_evidence_not_silently_discarded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text("{not-json", encoding="utf-8")
            with self.assertRaises(ProtocolError):
                DurableStateStore(path).load()

    def test_unknown_schema_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text(json.dumps({"schema_version": 2, "worker_id": "w"}))
            with self.assertRaises(ProtocolError):
                DurableStateStore(path).load()


if __name__ == "__main__":
    unittest.main()
