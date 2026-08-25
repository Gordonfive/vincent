import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer/debian13"


class ApplianceBootDefaultsTests(unittest.TestCase):
    def test_account_creation_is_disabled_without_triggering_debian_user_setup(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("d-i passwd/root-login boolean true", preseed)
        self.assertIn("d-i passwd/root-password-crypted password !vincent-installer-no-login!", preseed)
        self.assertIn("d-i passwd/make-user boolean false", preseed)
        self.assertIn("in-target passwd -l root", preseed)
        self.assertNotIn("passwd/username", preseed)
        self.assertNotIn("passwd/user-fullname", preseed)
        self.assertNotIn("passwd/user-password", preseed)
        for name in ("grub-mission-control.cfg", "isolinux-mission-control.cfg"):
            text = (INSTALLER / name).read_text()
            self.assertIn("passwd/root-login=true", text, name)
            self.assertIn("passwd/make-user=false", text, name)
            self.assertIn("preseed/file=/cdrom/preseed.cfg", text, name)

    def test_partitioning_defaults_to_guided_whole_disk_lvm_atomic(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("partman-auto/init_automatically_partition select 60some_device_lvm__________lvm", preseed)
        self.assertIn("partman-auto/method string lvm", preseed)
        self.assertIn("partman-auto-lvm/guided_size string max", preseed)
        self.assertIn("partman-auto-lvm/new_vg_name string vincent-vg", preseed)
        self.assertIn("partman-auto/choose_recipe select atomic", preseed)
        self.assertNotIn("partman-auto/disk", preseed)
        self.assertIn("partman/confirm_write_new_label boolean false", preseed)
        self.assertIn("partman/confirm boolean false", preseed)
        self.assertIn("partman/confirm_nooverwrite boolean false", preseed)


if __name__ == "__main__":
    unittest.main()
