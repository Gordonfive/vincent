# Debian USB Installer Architecture

## Prototype choice

The reference image remasters the official Debian 13 amd64 netinst hybrid ISO and adds:

- a preseed file;
- BIOS and UEFI Mission Control boot entries;
- a Git-archived platform payload;
- a first-boot bootstrap service;
- no credential or permanent identity.

This uses Debian Installer preseeding rather than cloning an existing worker disk.

## Destructive boundary

The prototype automates ordinary configuration but not target-disk authorization. After the operator selects a disk, guided partitioning replaces the entire selected disk with LVM using Debian's `atomic` recipe (all files in one root filesystem) and allocates the maximum available space. It does not select “largest free space.” Disk selection and final partition confirmation remain interactive. Network-interface selection also remains interactive so a machine without Ethernet presents Debian's scanned Wi-Fi SSID list and password prompt instead of silently choosing a network. These are deliberate bootstrap and safety gates, not missing automation.

The build operation writes only an ISO file. A separate flasher requires a stable USB by-id path, verifies removable USB hardware, rejects mounted devices, requires an exact confirmation tied to that identity, and verifies the bytes written.

## Default disk layout

The initial profile uses Debian's simple `atomic` guided recipe on one operator-selected disk:

- EFI/boot structures selected by Debian for the firmware mode;
- one main ext4 filesystem;
- swap according to the installer recipe.

This keeps recovery simple and makes all local state disposable. Multi-disk optimization and separate Docker storage are deferred until measured workload evidence justifies them.

## Bootstrap sequence

```text
verified Debian ISO
  -> reproducible remaster from clean Git commit
  -> operator-authorized USB flash
  -> visibly destructive boot selection
  -> manual target-disk selection and confirmation
  -> Debian base + SSH + development prerequisites
  -> embedded platform archive
  -> first-boot platform installation
  -> unique identity generation
  -> signed Docker/DDEV repositories and tool verification
  -> official Codex CLI installation, no authentication
  -> ENROLLMENT_REQUIRED
```

## Trust boundary

The USB is public-equivalent provisioning material. Possession grants no private-repository or Codex access. Initial trust is established later by comparing the generated fingerprint and granting a revocable credential to that worker identity.

## Reproducibility boundary

The build manifest records the platform commit, Debian version, architecture, source ISO hash, and output hash. The platform payload is produced with `git archive`, so uncommitted files cannot enter the image. Exact output bytes may vary with ISO-tool implementation metadata; source inputs and resulting checksum are always recorded.
