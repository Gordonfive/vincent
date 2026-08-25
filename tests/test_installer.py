import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def test_shell_syntax(self):
        result = subprocess.run(["sh", "-n", str(ROOT / "installer/install.sh")])
        self.assertEqual(result.returncode, 0)

    def test_installer_does_not_enable_or_start_service(self):
        content = (ROOT / "installer/install.sh").read_text()
        self.assertNotIn("systemctl enable", content)
        self.assertNotIn("systemctl start", content)
        self.assertNotIn("systemctl --now", content)

    def test_installer_contains_no_embedded_private_key(self):
        content = (ROOT / "installer/install.sh").read_text()
        self.assertNotIn("BEGIN " + "OPENSSH PRIVATE KEY", content)
        self.assertNotIn("BEGIN " + "PRIVATE KEY", content)

    def test_offline_package_build_can_see_debian_setuptools(self):
        content = (ROOT / "installer/install.sh").read_text()
        self.assertIn("python3 -m venv --system-site-packages", content)
        self.assertIn("import setuptools.build_meta", content)
        self.assertIn("--no-deps --no-build-isolation", content)


if __name__ == "__main__":
    unittest.main()
