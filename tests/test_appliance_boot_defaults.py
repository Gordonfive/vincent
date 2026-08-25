import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer/debian13"


class ApplianceBootDefaultsTests(unittest.TestCase):
    def test_account_creation_is_disabled_in_preseed_and_boot_entries(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("d-i passwd/root-login boolean false", preseed)
        self.assertIn("d-i passwd/make-user boolean false", preseed)
        for name in ("grub-mission-control.cfg", "isolinux-mission-control.cfg"):
            text = (INSTALLER / name).read_text()
            self.assertIn("passwd/root-login=false", text, name)
            self.assertIn("passwd/make-user=false", text, name)
            self.assertIn("preseed/file=/cdrom/preseed.cfg", text, name)

    def test_partitioning_defaults_to_guided_whole_disk_lvm_atomic(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("partman-auto/init_automatically_partition select Guided - use entire disk", preseed)
        self.assertIn("partman-auto/method string lvm", preseed)
        self.assertIn("partman-auto-lvm/guided_size string max", preseed)
        self.assertIn("partman-auto/choose_recipe select atomic", preseed)
        self.assertNotIn("partman-auto/disk", preseed)
        self.assertIn("partman/confirm_write_new_label boolean false", preseed)
        self.assertIn("partman/confirm boolean false", preseed)
        self.assertIn("partman/confirm_nooverwrite boolean false", preseed)


if __name__ == "__main__":
    unittest.main()
