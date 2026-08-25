import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositorySafetyTests(unittest.TestCase):
    def test_validation_script_syntax(self):
        result = subprocess.run(["sh", "-n", str(ROOT / "scripts/validate.sh")])
        self.assertEqual(result.returncode, 0)

    def test_ci_has_read_only_repository_permission(self):
        workflow = (ROOT / ".github/workflows/ci.yml").read_text()
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)

    def test_no_private_key_material_in_source_tree(self):
        forbidden = tuple("BEGIN " + key + " PRIVATE KEY" for key in ("OPENSSH", "RSA", "EC"))
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for marker in forbidden:
                self.assertNotIn(marker, content, str(path))


if __name__ == "__main__":
    unittest.main()
