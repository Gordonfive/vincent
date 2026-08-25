import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer/debian13"


class DebianInstallerTests(unittest.TestCase):
    def test_all_installer_shell_scripts_parse(self):
        scripts = [INSTALLER / name for name in ("fetch-source.sh", "build-image.sh", "inspect-image.sh", "flash-usb.sh", "first-boot.sh")]
        scripts.append(ROOT / "bootstrap/provision-worker-baseline.sh")
        for path in scripts:
            result = subprocess.run(["sh", "-n", str(path)])
            self.assertEqual(result.returncode, 0, path.name)

    def test_destructive_disk_choice_is_not_preseeded(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertNotIn("partman-auto/disk", preseed)
        self.assertNotIn("biggest_free", preseed)
        self.assertIn("partman-auto/method string lvm", preseed)
        self.assertIn("partman-auto-lvm/guided_size string max", preseed)
        self.assertIn("partman-auto/choose_recipe select atomic", preseed)
        self.assertIn("partman/confirm_write_new_label boolean false", preseed)
        self.assertIn("partman/confirm boolean false", preseed)
        self.assertIn("partman/confirm_nooverwrite boolean false", preseed)

    def test_account_secrets_are_not_preseeded(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertNotRegex(preseed, r"passwd/(user-password|root-password)")
        self.assertNotIn("authorized_keys", preseed)

    def test_network_and_wifi_selection_remain_interactive(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("netcfg/get_hostname string vincent-worker-unenrolled", preseed)
        self.assertNotIn("codex-worker-unenrolled", preseed)
        self.assertNotIn("netcfg/choose_interface", preseed)
        self.assertNotIn("netcfg/wireless_essid string", preseed)
        self.assertNotIn("netcfg/wireless_wpa string", preseed)
        self.assertNotIn("netcfg/wireless_wep string", preseed)

    def test_usb_flasher_requires_stable_usb_identity_and_exact_confirmation(self):
        script = (INSTALLER / "flash-usb.sh").read_text()
        self.assertIn("/dev/disk/by-id/usb-", script)
        self.assertIn('ERASE:', script)
        self.assertIn('transport', script)
        self.assertIn('removable', script)
        self.assertIn('cmp -n', script)

    def test_boot_entries_are_visibly_destructive_but_not_defaulted(self):
        bios = (INSTALLER / "isolinux-mission-control.cfg").read_text()
        uefi = (INSTALLER / "grub-mission-control.cfg").read_text()
        self.assertIn("DESTRUCTIVE", bios)
        self.assertIn("DESTRUCTIVE", uefi)
        self.assertIn("Vincent installer", bios)
        self.assertIn("Vincent installer", uefi)
        self.assertNotIn("interface=auto", bios)
        self.assertNotIn("interface=auto", uefi)
        self.assertNotIn("menu default", bios)
        self.assertNotIn("set default", uefi)

    def test_source_is_pinned_to_debian_13_amd64_https(self):
        source = (INSTALLER / "source.env").read_text()
        self.assertRegex(source, r"DEBIAN_VERSION=13\.\d+\.\d+")
        self.assertIn("DEBIAN_ARCH=amd64", source)
        self.assertIn(
            "DEBIAN_BASE_URL=https://cdimage.debian.org/debian-cd/current/amd64/iso-cd",
            source,
        )

    def test_build_never_writes_directly_to_block_devices(self):
        build = (INSTALLER / "build-image.sh").read_text()
        self.assertIn("dist/vincent-debian-", build)
        self.assertNotIn("/dev/sd", build)
        self.assertNotRegex(build, re.compile(r"\bdd\s+if="))
        self.assertIn("refusing to overwrite or append to existing output", build)

    def test_build_makes_extracted_boot_configs_writable_before_editing(self):
        build = (INSTALLER / "build-image.sh").read_text()
        chmod = 'chmod u+w "$work_root/menu.cfg" "$work_root/grub.cfg"'
        self.assertIn(chmod, build)
        self.assertLess(build.index(chmod), build.index("include mission-control.cfg"))

    def test_inspection_extracts_and_validates_embedded_payloads(self):
        inspect = (INSTALLER / "inspect-image.sh").read_text()
        self.assertIn('-extract "$required" "$extracted"', inspect)
        self.assertIn('tar -tzf "$inspection_root/platform.tar.gz"', inspect)
        self.assertIn("mission-control/first-boot.sh", inspect)

    def test_toolchain_uses_signed_repositories_and_saved_codex_installer(self):
        script = (ROOT / "bootstrap/provision-worker-baseline.sh").read_text()
        self.assertIn("Signed-By: /etc/apt/keyrings/docker.asc", script)
        self.assertIn("Signed-By: /etc/apt/keyrings/ddev.asc", script)
        self.assertIn("https://pkg.ddev.com/apt/", script)
        self.assertIn("apt-get install -y ca-certificates curl gpg jq gh git", script)
        self.assertIn("https://chatgpt.com/codex/install.sh", script)
        self.assertIn("codex-install.sh.sha256", script)
        self.assertIn("install -d -o root -g mission-control -m 0750", script)
        self.assertIn('chown root:mission-control "$codex_installer"', script)
        self.assertIn('chmod 0750 "$codex_installer"', script)
        self.assertIn('install -o root -g root -m 0755 "$codex_binary" /usr/local/bin/codex', script)
        self.assertIn("runuser -u nobody -- /usr/local/bin/codex --version", script)
        self.assertNotIn('ln -sfn "$codex_binary" /usr/local/bin/codex', script)
        self.assertNotIn("curl -fsSL https://chatgpt.com/codex/install.sh |", script)

    def test_first_boot_assigns_stable_vincent_hostname(self):
        script = (INSTALLER / "first-boot.sh").read_text()
        self.assertIn("/sys/class/dmi/id/product_uuid", script)
        self.assertIn("/etc/machine-id", script)
        self.assertIn('print(f"vincent-worker-{value:06d}")', script)
        self.assertIn('hostnamectl set-hostname "$vincent_hostname"', script)

    def test_fetch_requires_the_debian_cd_signing_keyring(self):
        script = (INSTALLER / "fetch-source.sh").read_text()
        self.assertIn("/usr/share/keyrings/debian-role-keys.gpg", script)
        self.assertIn("install the debian-keyring package", script)
        self.assertNotIn("debian-archive-keyring.gpg", script)


if __name__ == "__main__":
    unittest.main()
