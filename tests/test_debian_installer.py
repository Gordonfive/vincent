import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer/debian13"


class DebianInstallerTests(unittest.TestCase):
    def test_all_installer_shell_scripts_parse(self):
        names = (
            "fetch-source.sh", "build-image.sh", "inspect-image.sh", "flash-usb.sh",
            "first-boot.sh", "self-test.sh", "console-status.sh", "codex-console.sh",
        )
        scripts = [INSTALLER / name for name in names]
        scripts += [ROOT / "bootstrap/provision-worker-baseline.sh", ROOT / "installer/install.sh"]
        for path in scripts:
            result = subprocess.run(["sh", "-n", str(path)])
            self.assertEqual(result.returncode, 0, path.name)

    def test_partitioning_is_normal_debian_interactive_workflow(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        for marker in (
            "partman-auto/disk", "partman-auto/method", "partman-auto/choose_recipe",
            "partman-auto-lvm", "partman/confirm_write_new_label", "partman/confirm boolean",
        ):
            self.assertNotIn(marker, preseed)

    def test_no_human_account_and_root_locked_before_first_boot(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("passwd/root-login boolean true", preseed)
        self.assertIn("passwd/root-password-crypted password !vincent-installer-no-login!", preseed)
        self.assertIn("passwd/make-user boolean false", preseed)
        self.assertIn("in-target passwd -l root", preseed)
        self.assertNotIn("passwd/username", preseed)
        self.assertNotIn("passwd/user-fullname", preseed)
        self.assertNotIn("passwd/user-password", preseed)

    def test_network_and_wifi_selection_remain_interactive(self):
        preseed = (INSTALLER / "preseed.cfg").read_text()
        self.assertIn("netcfg/get_hostname string vincent-worker", preseed)
        self.assertNotIn("unenrolled", preseed)
        self.assertNotIn("netcfg/choose_interface", preseed)

    def test_vincent_service_identity_is_dedicated_and_non_login(self):
        install = (ROOT / "installer/install.sh").read_text()
        unit = (ROOT / "installer/systemd/mission-control-worker.service").read_text()
        self.assertIn("service_user=vincent", install)
        self.assertIn("--shell /usr/sbin/nologin", install)
        self.assertIn("state_root=/var/lib/vincent", install)
        self.assertIn("User=vincent", unit)
        self.assertIn("Group=vincent", unit)
        self.assertNotIn("User=mission-control", unit)
        self.assertNotIn("runuser -u nobody", (ROOT / "bootstrap/provision-worker-baseline.sh").read_text())

    def test_build_number_is_durable_and_consistent(self):
        build_number = (INSTALLER / "BUILD_NUMBER").read_text().strip()
        self.assertRegex(build_number, r"^\d{4,}$")
        build = (INSTALLER / "build-image.sh").read_text()
        self.assertIn("BUILD_NUMBER", build)
        self.assertIn("build-${build_number}", build)
        self.assertIn("VINCENT_B${build_number}", build)
        self.assertIn('"build_number":build', build)
        self.assertIn('/vincent/build-number', build)
        console = (INSTALLER / "console-status.sh").read_text()
        self.assertIn("BUILD:", console)
        self.assertIn("/etc/vincent/build-number", console)

    def test_runtime_source_is_exact_public_git_commit(self):
        script = (INSTALLER / "first-boot.sh").read_text()
        self.assertIn("https://github.com/Gordonfive/vincent.git", script)
        self.assertIn("expected-commit", script)
        self.assertIn("git -C \"$source_root\" fetch --no-tags --depth=1 origin \"$expected_commit\"", script)
        self.assertNotIn("tar -xzf", script)

    def test_dashboard_and_tty2_codex_console_exist(self):
        dashboard = (INSTALLER / "console-status.sh").read_text()
        codex_console = (INSTALLER / "codex-console.sh").read_text()
        self.assertIn("LIVE WORK OUTPUT", dashboard)
        self.assertIn("LAST ERROR", dashboard)
        self.assertIn("Alt+F2", dashboard)
        self.assertIn("runuser -u \"$service_user\"", codex_console)
        self.assertIn("service_user=vincent", codex_console)
        self.assertNotIn("/bin/bash", codex_console)

    def test_build_never_writes_directly_to_block_devices(self):
        build = (INSTALLER / "build-image.sh").read_text()
        self.assertNotIn("/dev/sd", build)
        self.assertNotRegex(build, re.compile(r"\bdd\s+if="))
        self.assertIn("refusing to overwrite or append to existing output", build)

    def test_inspection_enforces_build_number_and_interactive_partitioning(self):
        inspect = (INSTALLER / "inspect-image.sh").read_text()
        self.assertIn("VINCENT_B${build_number}", inspect)
        self.assertIn("embedded build number mismatch", inspect)
        self.assertIn("forced partitioning detected", inspect)
        self.assertIn("INSTALLER_INSPECTION=PASS", inspect)

    def test_toolchain_uses_signed_repositories_and_service_environment(self):
        script = (ROOT / "bootstrap/provision-worker-baseline.sh").read_text()
        self.assertIn("Signed-By: /etc/apt/keyrings/docker.asc", script)
        self.assertIn("Signed-By: /etc/apt/keyrings/ddev.asc", script)
        self.assertIn("service_user=vincent", script)
        self.assertIn("service_run()", script)
        self.assertIn("HOME=\"$service_home\"", script)
        self.assertNotIn("runuser -u nobody", script)

    def test_first_boot_assigns_stable_vincent_hostname(self):
        script = (INSTALLER / "first-boot.sh").read_text()
        self.assertIn("/sys/class/dmi/id/product_uuid", script)
        self.assertIn('print(f"vincent-worker-{value:06d}")', script)
        self.assertIn('hostnamectl set-hostname "$vincent_hostname"', script)

    def test_fetch_requires_the_debian_cd_signing_keyring(self):
        script = (INSTALLER / "fetch-source.sh").read_text()
        self.assertIn("/usr/share/keyrings/debian-role-keys.gpg", script)
        self.assertNotIn("debian-archive-keyring.gpg", script)


if __name__ == "__main__":
    unittest.main()
