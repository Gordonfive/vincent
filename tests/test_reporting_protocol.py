import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from mission_control.reporting import BlockedReport, DecisionRequest, ReportPublisher


def git(path, *args):
    return subprocess.run(["git", *args], cwd=path, text=True, capture_output=True, check=True).stdout.strip()


class ReportingProtocolTests(unittest.TestCase):
    def test_blocked_report_contains_exact_decision_context(self):
        report = BlockedReport(1, "MCP-1101", "worker-1", "AMBIGUOUS_REQUIREMENT", ("Inspected both approaches",), ("Dirty worktree retained",), "Either option changes public behavior", ("A", "B"), "Choose A or B", "2026-08-24T00:00:00Z")
        data = json.loads(report.to_json())
        self.assertEqual(data["reason_code"], "AMBIGUOUS_REQUIREMENT")
        self.assertIn("Choose A or B", report.to_markdown())

    def test_decision_response_is_durable_data(self):
        request = DecisionRequest(1, "DEC-001", "MCP-1101", "worker-1", "Choose", ("A", "B"), "A", True, "RESOLVED", "A")
        data = json.loads(request.to_json())
        self.assertEqual(data["response"], "A")
        self.assertEqual(data["status"], "RESOLVED")

    def test_blocked_report_publishes_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            remote = root / "remote.git"
            git(root, "init", "--bare", str(remote))
            checkout = root / "checkout"
            git(root, "clone", str(remote), str(checkout))
            git(checkout, "config", "user.name", "Worker")
            git(checkout, "config", "user.email", "worker@example.invalid")
            git(checkout, "switch", "-c", "main")
            (checkout / "README.md").write_text("base\n")
            git(checkout, "add", ".")
            git(checkout, "commit", "-m", "base")
            git(checkout, "push", "origin", "main")
            start = git(checkout, "rev-parse", "HEAD")
            report = BlockedReport(1, "MCP-1102", "worker-1", "EXTERNAL_DEPENDENCY", (), ("workspace",), "dependency unavailable", ("wait",), "Wait?", "now")
            result = ReportPublisher(checkout).publish(report, expected_commit=start)
            self.assertEqual(result.ending_commit, result.remote_commit)
            self.assertTrue((checkout / "coordination/reports/MCP-1102/blocked.json").exists())


if __name__ == "__main__":
    unittest.main()
