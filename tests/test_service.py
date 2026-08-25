import json
import unittest
from threading import Event

from mission_control.service import WorkerService


class FakeEngine:
    def __init__(self, results=None, error=False):
        self.results = list(results or [])
        self.error = error
        self.calls = 0

    def run_once(self):
        self.calls += 1
        if self.error:
            raise RuntimeError("network unavailable")
        return self.results.pop(0) if self.results else None


class ServiceTests(unittest.TestCase):
    def test_stop_request_exits_cleanly(self):
        stop = Event()
        events = []

        def sleeper(_):
            stop.set()

        status = WorkerService(FakeEngine(), 5, stop, sleeper=sleeper, emit=events.append).run()
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(events[0])["event"], "WORKER_ONLINE")
        self.assertEqual(json.loads(events[-1])["event"], "WORKER_OFFLINE")

    def test_repeated_failures_are_bounded(self):
        stop = Event()
        events = []
        status = WorkerService(
            FakeEngine(error=True), 5, stop, maximum_consecutive_errors=3,
            sleeper=lambda _: None, emit=events.append,
        ).run()
        self.assertEqual(status, 1)
        errors = [json.loads(item) for item in events if json.loads(item)["event"] == "SUPERVISOR_ERROR"]
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[-1]["consecutive_errors"], 3)


if __name__ == "__main__":
    unittest.main()
