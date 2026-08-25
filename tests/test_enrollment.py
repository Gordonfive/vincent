import json
import tempfile
import unittest
from pathlib import Path

from mission_control.enrollment import EnrollmentError, generate_enrollment


class EnrollmentTests(unittest.TestCase):
    def test_generates_unique_identity_and_public_request(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "identity"
            request = generate_enrollment(root, hostname="worker-host")
            self.assertTrue(request.worker_id.startswith("worker-"))
            self.assertEqual(request.hostname, "worker-host")
            self.assertTrue(request.public_key.startswith("ssh-ed25519 "))
            self.assertTrue(request.fingerprint.startswith("SHA256:"))
            identity = json.loads((root / "identity.json").read_text())
            self.assertEqual(identity["worker_id"], request.worker_id)
            self.assertEqual((root / "worker_ed25519").stat().st_mode & 0o777, 0o600)
            serialized = json.loads((root / "enrollment-request.json").read_text())
            self.assertNotIn("private_key", serialized)

    def test_reinstall_cannot_impersonate_existing_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "identity"
            generate_enrollment(root)
            with self.assertRaises(EnrollmentError):
                generate_enrollment(root)

    def test_separate_installations_receive_distinct_identities(self):
        with tempfile.TemporaryDirectory() as directory:
            first = generate_enrollment(Path(directory) / "first")
            second = generate_enrollment(Path(directory) / "second")
            self.assertNotEqual(first.worker_id, second.worker_id)
            self.assertNotEqual(first.public_key, second.public_key)


if __name__ == "__main__":
    unittest.main()
