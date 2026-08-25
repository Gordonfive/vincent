import json
import sys
import tempfile
import unittest
from pathlib import Path

from mission_control.reporting import CompletionReport
from mission_control.validation import ValidationCommand, run_validation, validation_passed


class ValidationReportingTests(unittest.TestCase):
    def test_supervisor_captures_independent_validation_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_validation(
                ValidationCommand("unit", (sys.executable, "-c", "print('verified')")),
                Path(directory),
            )
        self.assertTrue(result.passed)
        self.assertEqual(result.exit_status, 0)
        self.assertIn("verified", result.output_excerpt)
        self.assertEqual(len(result.output_sha256), 64)
        self.assertTrue(validation_passed((result,)))

    def test_failure_is_not_reported_as_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_validation(
                ValidationCommand("failure", (sys.executable, "-c", "raise SystemExit(7)")),
                Path(directory),
            )
        self.assertFalse(result.passed)
        self.assertEqual(result.exit_status, 7)
        self.assertFalse(validation_passed((result,)))

    def test_completion_report_has_json_and_markdown_views(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_validation(
                ValidationCommand("unit", (sys.executable, "-c", "pass")), Path(directory)
            )
        report = CompletionReport(
            1, "MCP-401", "worker-1", "platform", "owner/repo", "task/MCP-401",
            "a" * 40, "b" * 40, "COMPLETED", "start", "end", ("Added feature",),
            (result,), "VERIFIED", (), (), "0.1.0"
        )
        data = json.loads(report.to_json())
        self.assertEqual(data["task_id"], "MCP-401")
        self.assertEqual(data["validation"][0]["exit_status"], 0)
        self.assertIn("PASS: `unit`", report.to_markdown())


if __name__ == "__main__":
    unittest.main()
