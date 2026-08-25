# Build and Flash the Debian 13 Worker USB

Status: PROTOTYPE — DESTRUCTIVE INSTALLATION REQUIRES MANUAL DISK SELECTION

The image is built from a verified Debian 13 netinst ISO and a clean platform commit. The ISO contains no Git credential, Codex credential, administrative password, permanent worker identity, or private SSH key.

## Safety model

This prototype intentionally does not preseed a target disk or destructive confirmations.

- The normal Debian installer remains the default boot path.
- The Vincent entry is visibly labeled `DESTRUCTIVE`.
- The operator must select the installation disk.
- Debian asks for the target disk, proposes whole-disk guided LVM with all files in one root filesystem, displays the destructive changes, and requires final confirmation.
- No human login account or password is created. Root login remains disabled.
- The USB flasher accepts only `/dev/disk/by-id/usb-*` removable whole disks and requires an exact device-specific confirmation string.

## Build host prerequisites

Use a Debian development machine with a clean clone of the public `Gordonfive/vincent` repository:

```text
sudo apt-get update
sudo apt-get install -y xorriso curl gpgv debian-keyring python3 python3-pip python3-setuptools git
```

## Fetch and verify Debian

The pinned source metadata is `installer/debian13/source.env`. Fetching verifies Debian's signed `SHA512SUMS` and the ISO checksum:

```text
sh installer/debian13/fetch-source.sh
```

The current pinned source is Debian 13.6.0 amd64 netinst. Updating it is a deliberate reviewed commit, not an automatic moving target.

## Build

From a clean, pushed platform commit:

```text
sh installer/debian13/build-image.sh \
  installer/debian13/cache/debian-13.6.0-amd64-netinst.iso
```

The builder refuses to overwrite or append to an existing output ISO. Archive or remove a previous reconstructable artifact deliberately before rebuilding.

Outputs under `dist/`:

- customized hybrid ISO;
- SHA-256 file;
- JSON build manifest containing the platform commit and source/output hashes.

Inspect the result:

```text
sh installer/debian13/inspect-image.sh dist/vincent-debian-13.6.0-amd64.iso
```

The ISO is a build artifact and is not committed. Git contains everything needed to recreate it.

## Identify the USB device

Connect only the intended USB stick, then inspect stable device identity:

```text
lsblk -o NAME,PATH,TYPE,TRAN,RM,SIZE,MODEL,SERIAL,MOUNTPOINTS
ls -l /dev/disk/by-id/usb-*
```

Do not use `/dev/sdX` as the authorization identity. Do not proceed if the target is ambiguous or mounted.

## Flash

Example only; substitute the exact by-id path shown on the build host:

```text
sudo sh installer/debian13/flash-usb.sh \
  dist/vincent-debian-13.6.0-amd64.iso \
  /dev/disk/by-id/usb-EXACT_DEVICE_ID \
  'ERASE:usb-EXACT_DEVICE_ID'
```

The flasher verifies USB transport, removable status, whole-disk type, capacity, absence of mounts, and byte-for-byte image content after writing.

## Install the worker

1. Boot the disposable workstation from the USB in UEFI mode when available.
2. Select `Vincent installer (DESTRUCTIVE - manual disk selection)`.
3. Select the wired interface when it has a working link. Otherwise select the Wi-Fi interface, choose an SSID from Debian's scan, and enter its password. Wi-Fi credentials are used by the installer and are not embedded in the USB image.
4. Select only the verified disposable target disk.
5. Confirm that Debian proposes whole-disk guided LVM with the `atomic` all-files-in-one-filesystem recipe, then review and confirm destruction.
6. Remove the USB when Debian reboots.

No username, password, or local login is part of the Vincent install path. The installer creates only the locked service identities needed by Vincent.

## Unattended first boot and self-test

First boot installs the platform from the embedded Git archive, generates a new worker identity, installs Docker CE, DDEV, GitHub CLI, and the Codex CLI, verifies the toolchain, runs the Vincent appliance self-test, and stops without worker authority.

Vincent automatically validates at least:

- stable `vincent-worker-NNNNNN` hostname;
- default network route and DNS;
- SSH service;
- Git and GitHub CLI;
- Docker and DDEV;
- Codex CLI;
- Python pip/setuptools packaging support;
- locked Vincent service account and absence of human login accounts;
- unique enrollment request;
- embedded source payload integrity and private-key marker scan;
- worker service remains disabled before enrollment.

The physical console is owned by `vincent-console-status.service`, not a login getty. It persistently displays the self-test result and current state. The operator is not expected to log in or run diagnostic commands.

Expected successful endpoint:

```text
VINCENT WORKER SELF-TEST
...
OVERALL: PASS
STATE:   ENROLLMENT_REQUIRED
READY FOR REMOTE ENROLLMENT
No local login or diagnostic commands are required.
```

A failure displays `OVERALL: FAIL` or `STATE: FAILED` and remains visible for photographic acceptance evidence. Detailed machine-readable evidence is retained under `/var/lib/mission-control-install/` and the bootstrap log under `/var/log/mission-control/` for later authorized remote retrieval.

Do not enable `mission-control-worker.service` until fingerprint approval, repository authorization, Codex authentication, configuration replacement, and `doctor` success.
