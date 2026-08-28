import json
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from mission_control import vincent_cli

class Response:
    def __enter__(self): return self
    def __exit__(self, *_): return False

class VincentCliTests(unittest.TestCase):
    @patch("mission_control.vincent_cli.json.load")
    @patch("mission_control.vincent_cli.urllib.request.urlopen")
    def test_public_bootstrap_policy_is_validated(self, urlopen, load):
        urlopen.return_value = Response()
        load.return_value = {"schema_version": 1, "product": "Vincent", "bootstrap_repository": "logrusbox/vincent", "platform_repository": "logrusbox/vincent"}
        self.assertEqual(vincent_cli.load_instructions()["product"], "Vincent")

    @patch("mission_control.vincent_cli.json.load")
    @patch("mission_control.vincent_cli.urllib.request.urlopen")
    def test_untrusted_bootstrap_repository_is_rejected(self, urlopen, load):
        urlopen.return_value = Response()
        load.return_value = {"schema_version": 1, "product": "Vincent", "bootstrap_repository": "attacker/repository", "platform_repository": "attacker/repository"}
        with self.assertRaises(RuntimeError): vincent_cli.load_instructions()

    def test_enrollment_request_uses_identity_directory(self):
        self.assertEqual(
            vincent_cli.ENROLLMENT_REQUEST,
            Path("/var/lib/vincent/identity/enrollment-request.json"),
        )

    def test_authorization_must_match_worker(self):
        with TemporaryDirectory() as temporary:
            authorization = Path(temporary) / "authorization.json"
            authorization.write_text(json.dumps({"schema_version": 1, "worker_id": "worker-other", "repository_scopes": []}))
            with patch.object(vincent_cli, "AUTHORIZATION", authorization):
                with self.assertRaises(RuntimeError): vincent_cli.load_authorization("worker-this")

    def test_missing_authorization_is_enrollment_required(self):
        with TemporaryDirectory() as temporary:
            with patch.object(vincent_cli, "AUTHORIZATION", Path(temporary) / "missing.json"):
                self.assertIsNone(vincent_cli.load_authorization("worker-this"))

if __name__ == "__main__": unittest.main()
