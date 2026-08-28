import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_scanner():
    path = ROOT / "scripts/check_secrets.py"
    spec = importlib.util.spec_from_file_location("vincent_check_secrets", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SecretPatternTests(unittest.TestCase):
    def test_openai_project_and_service_keys_are_detected(self):
        scanner = load_scanner()
        project_key = "sk-" + "proj-" + "A" * 24
        service_key = "sk-" + "svcacct-" + "B" * 24
        pattern = scanner.PATTERNS["OpenAI project/service key"]
        self.assertIsNotNone(pattern.search(project_key))
        self.assertIsNotNone(pattern.search(service_key))

    def test_openai_legacy_secret_key_is_detected(self):
        scanner = load_scanner()
        key = "sk-" + "C" * 40
        self.assertIsNotNone(scanner.PATTERNS["OpenAI legacy secret key"].search(key))


if __name__ == "__main__":
    unittest.main()
