import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class IsoWorkflowTests(unittest.TestCase):
    def test_checksum_verification_runs_from_repository_root(self):
        workflow = (ROOT / ".github/workflows/vincent-iso.yml").read_text()
        self.assertIn('sha256sum --check "$output_iso.sha256"', workflow)
        self.assertNotIn('(cd dist && sha256sum --check', workflow)


if __name__ == "__main__":
    unittest.main()
