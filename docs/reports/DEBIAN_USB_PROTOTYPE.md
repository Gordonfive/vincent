# Debian 13 USB Prototype Checkpoint

Date: 2026-08-24  
Status: IMAGE BUILD AND USB FLASH VERIFIED; TARGET INSTALLATION UNVERIFIED

## Implemented

- Debian 13.6.0 amd64 netinst source metadata;
- signed Debian checksum verification;
- preseed prototype with locale, Sitka timezone, DHCP, minimal packages, SSH, whole-disk guided LVM using the atomic all-files-in-one-filesystem recipe, and first-boot hook;
- manual disk selection and destructive confirmations retained;
- BIOS and UEFI boot entries visibly labeled destructive and not defaulted;
- clean-Git ISO payload generation with platform commit and checksums;
- post-build payload and private-key inspection;
- removable USB by-id flasher with exact confirmation and byte verification;
- first-boot platform installation and unique identity generation;
- stable hardware-derived `gitboy-worker-NNNNNN` hostname;
- single `gitboy` command with public bootstrap-policy retrieval, interactive GitHub/Codex authentication, repository allowlisting, and enrollment reporting;
- Docker CE, DDEV, and official Codex CLI installation with observed-version recording;
- `ENROLLMENT_REQUIRED` status gate before credentials or service activation;
- build, flash, architecture, and operating instructions.

## Validation

```text
Ran 108 tests
OK
git diff --check: PASS
```

Shell syntax, destructive-boundary properties, absence of preseeded account secrets, stable USB identification, signed package-repository configuration, and build/flash separation are tested.

## Physical build and flash evidence

- build host: HAL-9000, Debian 13 amd64;
- Debian CD signature: good signature from `Debian CD signing key <debian-cd@lists.debian.org>`;
- source ISO SHA-256: `65273beed27b2df543b68b65630ba525cfbad8df2b12035732b2dff87d6664e7`;
- embedded platform commit: `9de1668a719bbfc4d8a4572288344743e5d7bf2b`;
- output ISO: `gitboy-debian-13.6.0-amd64.iso`;
- output ISO SHA-256: `ec50a07bad5e50d799aa8cebf786f72fff9b1ad464f937aee1f67f499067ed76`;
- embedded payload inspection: `INSTALLER_INSPECTION=PASS`;
- latest target: removable USB SanDisk 3.2Gen1, serial `03007622121425193247`;
- bytes written and compared: `790953984`;
- flash verification: `USB_FLASH_VERIFICATION=PASS`.

The first laptop boot exposed automatic Wi-Fi network selection without an SSID list. Review then found that `interface=auto` remained in both bootloader kernel command lines, overriding the preseed correction. Those arguments were removed and the boot entry was renamed `GitBoy installer (DESTRUCTIVE - manual disk selection)`. The GitBoy image was rebuilt, inspected, checksummed, flashed to a second explicitly authorized SanDisk, and byte-verified. Installer-network retesting remains pending.

A later physical installation exposed that `partman-auto/init_automatically_partition select biggest_free` restricted guided partitioning to existing free space. That setting has been removed. The installer now uses guided LVM, allocates the maximum selected-disk space, and selects Debian's `atomic` recipe. The installer still does not preseed a target disk or the final destructive write confirmation.

The same installation confirmed networking, Git, SSH, and stable hostname generation, but first-boot provisioning stopped before installing GitHub CLI, Docker, DDEV, Codex, or the `gitboy` command. The captured log identified `BackendUnavailable: Cannot import 'setuptools.build_meta'`: the virtual environment hid Debian's installed `python3-setuptools` while pip was correctly prohibited from creating an unpinned online build environment. The installer now creates the venv with system site packages visible, explicitly verifies the build backend import, and retains `--no-deps --no-build-isolation` for the local platform package.

Physical validation also passed for UEFI boot, full-disk LVM, automatic Ethernet reconnection, persistent hardware-derived hostname, local login, and remote SSH login. The preseed's temporary hostname was renamed from `codex-worker-unenrolled` to `gitboy-worker-unenrolled` so Debian-generated LVM identifiers use current product branding before first boot assigns the stable numeric hostname.

The next rebuilt-image test passed the Python package installation and reached baseline tool provisioning. It then exposed a permission mismatch: the root-owned Codex installer artifact was mode `0700` inside a root-only directory, but execution correctly dropped to the `mission-control` account. The evidence directory and installer remain root-owned but now grant only the `mission-control` group traverse/read/execute access (`0750`), allowing least-privilege installation without making the artifact public.

The subsequent end-to-end audit found that linking `/usr/local/bin/codex` into the service account's mode-`0700` home would make the command unreachable to the console owner invoking `gitboy`. Provisioning now installs a root-owned mode-`0755` copy of the verified Codex executable into `/usr/local/bin` and independently executes `codex --version` as the unprivileged `nobody` account. The locked service account retains its private state and authentication boundary.

The physical write occurred only after stable by-id resolution, serial verification, unmounting, and the exact destructive confirmation.

## Not yet proven

- hybrid BIOS/UEFI boot on the disposable target;
- corrected interactive Wi-Fi selection after image rebuild;
- hardware compatibility and firmware loading;
- Debian installation on the disposable target;
- first-boot network/package bootstrap;
- Docker/DDEV/Codex operation on that host;
- enrollment and autonomous task execution.

These steps require the owner's physical build host, USB device selection, and disposable target workstation.
