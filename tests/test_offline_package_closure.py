import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer/debian13"


class OfflinePackageClosureTests(unittest.TestCase):
    def test_closure_uses_verified_debian_iso_and_isolated_trixie_sources(self):
        prepare = (INSTALLER / "prepare-offline-packages.sh").read_text()
        build = (INSTALLER / "build-image.sh").read_text()

        self.assertIn("VERIFIED_DEBIAN.iso", prepare)
        self.assertIn("/pool/main/d/debian-archive-keyring", prepare)
        self.assertIn("dpkg-deb -x", prepare)
        self.assertIn("debian-archive-keyring.gpg", prepare)
        self.assertIn("https://deb.debian.org/debian trixie main", prepare)
        self.assertIn("https://deb.debian.org/debian trixie-updates main", prepare)
        self.assertIn("https://security.debian.org/debian-security trixie-security main", prepare)
        self.assertIn("Dir::Etc::sourcelist=$sources", prepare)
        self.assertIn("Dir::Etc::sourceparts=$sourceparts", prepare)
        self.assertNotIn("builder's configured Debian sources", prepare)
        self.assertIn("packages='debian-archive-keyring ", prepare)
        self.assertIn('prepare-offline-packages.sh" "$payload_root/offline-packages.tar.gz" "$source_iso"', build)

    def test_archive_glob_is_expanded_inside_download_directory(self):
        prepare = (INSTALLER / "prepare-offline-packages.sh").read_text()
        self.assertIn('cd "$cache/archives"', prepare)
        self.assertIn('tar -czf "$output" ./*.deb', prepare)
        self.assertNotIn('tar -C "$cache/archives" -czf "$output" ./*.deb', prepare)


if __name__ == "__main__":
    unittest.main()
