import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer/debian13"


class DebianInstallerTests(unittest.TestCase):
    def test_all_installer_shell_scripts_parse(self):
        scripts = [INSTALLER / name for name in (
            "fetch-source.sh", "build-image.sh", "inspect-image.sh", "flash-usb.sh",
            "first-boot.sh", "self-test.sh", "console-status.sh", "codex-console.sh",
            "preseed-assert.sh",
        )]
        scripts.append(ROOT / "bootstrap/provision-worker-baseline.sh")
        for path in scripts:
            result = subprocess.run(["sh", "-n", str(path)])
            self.assertEqual(result.returncode, 0, path.name)

    def test_destructive_disk_choice_is_not_preseeded(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertNotIn("partman-auto/disk", preseed)
        self.assertNotIn("biggest_free", preseed)
        self.assertIn("partman-auto/init_automatically_partition select 60some_device_lvm__________lvm", preseed)
        self.assertIn("partman-auto/method string lvm", preseed)
        self.assertIn("partman-auto-lvm/guided_size string max", preseed)
        self.assertIn("partman-auto-lvm/new_vg_name string vincent-vg", preseed)
        self.assertIn("partman-auto/choose_recipe select atomic", preseed)
        self.assertIn("partman/confirm_write_new_label boolean false", preseed)
        self.assertIn("partman/confirm boolean false", preseed)
        self.assertIn("partman/confirm_nooverwrite boolean false", preseed)

    def test_appliance_creates_no_human_account_or_password(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("passwd/root-login boolean false", preseed)
        self.assertIn("passwd/make-user boolean false", preseed)
        self.assertNotRegex(preseed, r"passwd/(user-password|root-password)")
        self.assertNotIn("passwd/username", preseed)
        self.assertNotIn("passwd/user-fullname", preseed)
        self.assertNotIn("authorized_keys", preseed)

    def test_preseed_fails_closed_instead_of_interactive_fallback(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        assertion = (INSTALLER / "preseed-assert.sh").read_text()
        self.assertIn("preseed/early_command string /bin/sh /cdrom/mission-control/preseed-assert.sh", preseed)
        self.assertIn("VINCENT PRESEED FAILED", assertion)
        for marker in ("passwd/root-login false", "passwd/make-user false", "netcfg/get_hostname vincent-worker", "partman-auto/method lvm", "partman-auto/choose_recipe atomic"):
            self.assertIn(marker, assertion)

    def test_network_and_wifi_selection_remain_interactive(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("netcfg/get_hostname string vincent-worker", preseed)
        self.assertNotIn("unenrolled", preseed)
        self.assertNotIn("codex-worker", preseed)
        self.assertNotIn("netcfg/choose_interface", preseed)

    def test_usb_flasher_requires_stable_usb_identity_and_exact_confirmation(self):
        script = (INSTALLER / "flash-usb.sh").read_text()
        self.assertIn("/dev/disk/by-id/usb-", script)
        self.assertIn("ERASE:", script)
        self.assertIn("transport", script)
        self.assertIn("removable", script)
        self.assertIn("cmp -n", script)

    def test_boot_entries_are_visibly_destructive_but_not_defaulted(self):
        bios = (INSTALLER / "isolinux-mission-control.cfg").read_text()
        uefi = (INSTALLER / "grub-mission-control.cfg").read_text()
        for text in (bios, uefi):
            self.assertIn("DESTRUCTIVE", text)
            self.assertIn("Vincent installer", text)
            self.assertIn("passwd/root-login=false", text)
            self.assertIn("passwd/make-user=false", text)
            self.assertNotIn("interface=auto", text)
        self.assertNotIn("menu default", bios)
        self.assertNotIn("set default", uefi)

    def test_source_is_pinned_to_debian_13_amd64_https(self):
        source = (INSTALLER / "source.env").read_text()
        self.assertRegex(source, r"DEBIAN_VERSION=13\.\d+\.\d+")
        self.assertIn("DEBIAN_ARCH=amd64", source)
        self.assertIn("DEBIAN_BASE_URL=https://cdimage.debian.org/debian-cd/current/amd64/iso-cd", source)

    def test_build_never_writes_directly_to_block_devices(self):
        build = (INSTALLER / "build-image.sh").read_text()
        self.assertIn("dist/vincent-debian-", build)
        self.assertNotIn("/dev/sd", build)
        self.assertNotRegex(build, re.compile(r"\bdd\s+if="))
        self.assertIn("refusing to overwrite or append to existing output", build)

    def test_build_embeds_dashboard_codex_console_and_expected_commit(self):
        build = (INSTALLER / "build-image.sh").read_text()
        for marker in ("/mission-control/self-test.sh", "/mission-control/console-status.sh", "/mission-control/codex-console.sh", "/mission-control/vincent-codex-console.service", "/mission-control/preseed-assert.sh", "/mission-control/expected-commit"):
            self.assertIn(marker, build)
        self.assertIn('"interactive_codex_console": "tty2_non_root"', build)
        self.assertIn('"live_console_work_output": True', build)
        self.assertIn('"network_bootstrap_retry": True', build)
        self.assertIn('"runtime_source": "public_git_exact_commit"', build)

    def test_build_makes_extracted_boot_configs_writable_before_editing(self):
        build = (INSTALLER / "build-image.sh").read_text()
        chmod = 'chmod u+w "$work_root/menu.cfg" "$work_root/grub.cfg"'
        self.assertIn(chmod, build)
        self.assertLess(build.index(chmod), build.index("include mission-control.cfg"))

    def test_inspection_validates_dashboard_and_interactive_console(self):
        inspect = (INSTALLER / "inspect-image.sh").read_text()
        for marker in ("mission-control/preseed-assert.sh", "mission-control/expected-commit", "mission-control/codex-console.sh", "mission-control/vincent-codex-console.service", "LIVE WORK OUTPUT", "Alt+F2"):
            self.assertIn(marker, inspect)
        self.assertIn("vincent-vg", inspect)

    def test_toolchain_uses_signed_repositories_and_saved_codex_installer(self):
        script = (ROOT / "bootstrap/provision-worker-baseline.sh").read_text()
        self.assertIn("Signed-By: /etc/apt/keyrings/docker.asc", script)
        self.assertIn("Signed-By: /etc/apt/keyrings/ddev.asc", script)
        self.assertIn("https://chatgpt.com/codex/install.sh", script)
        self.assertIn("codex-install.sh.sha256", script)
        self.assertIn('install -o root -g root -m 0755 "$codex_binary" /usr/local/bin/codex', script)
        self.assertNotIn("curl -fsSL https://chatgpt.com/codex/install.sh |", script)

    def test_first_boot_retries_network_and_fetches_exact_public_git_commit(self):
        script = (INSTALLER / "first-boot.sh").read_text()
        self.assertIn("network_attempts=20", script)
        self.assertIn("getent ahosts github.com", script)
        self.assertIn("curl --fail", script)
        self.assertIn("https://github.com/Gordonfive/vincent.git", script)
        self.assertIn("expected-commit", script)
        self.assertIn("git -C \"$source_root\" fetch --no-tags --depth=1 origin \"$expected_commit\"", script)
        self.assertIn("SELF_TESTING", script)
        self.assertIn("ENROLLMENT_REQUIRED", script)
        self.assertNotIn("tar -xzf", script)

    def test_console_has_fixed_status_live_output_and_codex_hint(self):
        service = (INSTALLER / "vincent-console-status.service").read_text()
        script = (INSTALLER / "console-status.sh").read_text()
        self.assertIn("Conflicts=getty@tty1.service", service)
        self.assertIn("TTYPath=/dev/tty1", service)
        for marker in ("VINCENT WORKER", "LIVE WORK OUTPUT", "EXPECTED GIT", "GITHUB DNS", "Alt+F2", "FAILED CHECKS"):
            self.assertIn(marker, script)
        self.assertNotIn("unenrolled", script)

    def test_tty2_codex_console_is_non_root_and_no_login_prompt(self):
        service = (INSTALLER / "vincent-codex-console.service").read_text()
        script = (INSTALLER / "codex-console.sh").read_text()
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("TTYPath=/dev/tty2", service)
        self.assertIn("Conflicts=getty@tty2.service", service)
        self.assertIn("runuser -u mission-control", script)
        self.assertIn("VINCENT INTERACTIVE CODEX CONSOLE", script)
        self.assertIn("systemctl mask getty@tty1.service getty@tty2.service", preseed)
        self.assertIn("vincent-codex-console.service", preseed)
        self.assertNotIn("/bin/bash", script)

    def test_self_test_covers_required_appliance_components(self):
        script = (INSTALLER / "self-test.sh").read_text()
        for marker in ("hostname", "network_route", "network_dns", "ssh_service", "git", "github_cli", "docker", "ddev", "codex", "python_packaging", "git_exact_commit", "git_public_remote", "service_account", "no_human_login_accounts", "enrollment_request", "embedded_recovery_payload", "embedded_private_key_scan", "worker_authority_disabled", "VINCENT_SELF_TEST"):
            self.assertIn(marker, script)

    def test_fetch_requires_the_debian_cd_signing_keyring(self):
        script = (INSTALLER / "fetch-source.sh").read_text()
        self.assertIn("/usr/share/keyrings/debian-role-keys.gpg", script)
        self.assertIn("install the debian-keyring package", script)
        self.assertNotIn("debian-archive-keyring.gpg", script)


if __name__ == "__main__":
    unittest.main()
