import json
import tempfile
import unittest
from pathlib import Path

from mission_control.events import Event, EventType, Heartbeat, HeartbeatFile


class EventTests(unittest.TestCase):
    def test_event_vocabulary_is_machine_readable(self):
        event = Event.create(EventType.HUMAN_DECISION_REQUIRED, "worker-1", "MCP-1301", {"decision_id": "DEC-1"})
        data = json.loads(event.to_json())
        self.assertEqual(data["event"], "HUMAN_DECISION_REQUIRED")
        self.assertEqual(data["details"]["decision_id"], "DEC-1")

    def test_heartbeat_is_ephemeral_file_not_git_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run/heartbeat.json"
            heartbeat = Heartbeat("worker-1", "now", "0.1.0", "IDLE", None, {"load": 0})
            HeartbeatFile(path).write(heartbeat)
            self.assertEqual(json.loads(path.read_text())["worker_id"], "worker-1")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
