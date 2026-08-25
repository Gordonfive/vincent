import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from mission_control import vincent_cli


class Response:
    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class VincentCliTests(unittest.TestCase):
    @patch("mission_control.vincent_cli.json.load")
    @patch("mission_control.vincent_cli.urllib.request.urlopen")
    def test_public_bootstrap_policy_is_validated(self, urlopen, load):
        urlopen.return_value = Response()
        load.return_value = {
            "schema_version": 1,
            "product": "Vincent",
            "bootstrap_repository": "Gordonfive/vincent",
            "platform_repository": "Gordonfive/vincent",
        }
        self.assertEqual(vincent_cli.load_instructions()["product"], "Vincent")

    @patch("mission_control.vincent_cli.json.load")
    @patch("mission_control.vincent_cli.urllib.request.urlopen")
    def test_untrusted_bootstrap_repository_is_rejected(self, urlopen, load):
        urlopen.return_value = Response()
        load.return_value = {
            "schema_version": 1,
            "product": "Vincent",
            "bootstrap_repository": "attacker/repository",
            "platform_repository": "attacker/repository",
        }
        with self.assertRaises(RuntimeError):
            vincent_cli.load_instructions()

    def test_report_is_local_and_contains_no_credential(self):
        with TemporaryDirectory() as temporary:
            enrollment = {
                "worker_id": "worker-test",
                "fingerprint": "SHA256:test",
            }
            with patch.object(Path, "home", return_value=Path(temporary)):
                report = vincent_cli.write_local_report(
                    {"platform_repository": "Gordonfive/vincent"}, enrollment, None
                )
            content = report.read_text()
            self.assertIn('"status": "ENROLLMENT_REQUIRED"', content)
            self.assertNotIn("credential", content.lower())


if __name__ == "__main__":
    unittest.main()
