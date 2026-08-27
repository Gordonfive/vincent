# Build and Flash the Vincent Debian Installer

This runbook describes the supported build/inspection/flashing safety model. Exact current commands and filenames must be taken from the selected source commit and installer scripts rather than copied from stale historical reports.

## Safety boundary

Building an ISO is non-destructive to target hardware. Flashing a USB and installing Debian are destructive operations and retain separate explicit operator authorization gates.

Never infer authorization from this document alone.

## Build source

For each physical test cycle:

1. select one exact Vincent source commit containing the intended installer/runtime changes;
2. confirm current product requirements/ADRs relevant to the build have been incorporated;
3. use the next unique monotonically increasing installer build number from the repository's installer build-number source;
4. build from a clean checkout of that exact commit;
5. verify the configured Debian source image/signatures/checksums using the repository tooling;
6. preserve complete build/validation output with `tee` for long-running commands and print the final pipeline exit status.

The ISO must not be built from uncommitted local files or an unreviewed moving branch tip.

## Required build properties

The image/build metadata must consistently identify:

- exact Vincent source commit;
- Debian source/version/architecture;
- installer build number;
- source image checksum/signature verification result;
- output image filename/volume/media identity where supported;
- generated manifest/checksum;
- embedded installer/runtime payload identity.

Installer build identity is immutable provenance and is separate from Vincent software SemVer.

## Image validation

Before any flash authorization, run the repository's full validation and image-inspection procedures. They must verify at least:

- repository tests and script syntax/checks;
- Debian source authenticity/integrity;
- expected Vincent payload and exact source identity;
- manifests/checksums/build-number consistency;
- absence of permanent worker identity and reusable credentials/secrets;
- absence of retired product/repository names in active payload where prohibited;
- no forced target disk, whole-disk recipe, LVM requirement or equivalent automatic partitioning choice;
- active installer-media exclusion support;
- installer network-preflight support used by current physical diagnostics;
- intended runtime networking/diagnostic/status components.

Do not flash an image that fails any applicable validation gate.

## Identify the USB target

Before flashing, inspect the build host and identify the exact removable USB device using a stable device identity such as `/dev/disk/by-id/usb-*` where supported.

Useful inspection commands include:

```text
lsblk -o NAME,PATH,TYPE,TRAN,RM,SIZE,MODEL,SERIAL,MOUNTPOINTS
ls -l /dev/disk/by-id/usb-*
```

Do not authorize a destructive write using an ambiguous `/dev/sdX` name alone. Do not proceed if the target identity, removability, whole-disk status, capacity, or mount state is uncertain.

## Flash

Use the repository's `installer/debian13/flash-usb.sh` interface from the selected source commit. The flasher is expected to:

- require a stable exact USB whole-device identity;
- reject non-removable/non-USB/ambiguous targets;
- reject mounted targets;
- require an exact device-specific destructive confirmation;
- write the validated image;
- verify the written bytes/media identity after flashing.

The exact command syntax must be read from the current script/help or current branch documentation before execution because installer tooling may evolve.

## Install on target hardware

A normal Vincent install preserves the operator interaction boundary:

1. boot the validated Vincent installer media;
2. select/configure the intended network interface; if using Wi-Fi, choose the SSID and enter the passphrase through the installer;
3. verify the active Vincent USB is not offered as an installation target;
4. select the intended target disk manually;
5. choose the desired Debian partitioning method/layout manually;
6. review the proposed disk changes and explicitly confirm final write;
7. allow Debian/Vincent installation and first boot to complete;
8. remove installation media when appropriate;
9. verify standalone READY, worker status, networking and diagnostics before adding project/fleet authority.

Vincent does **not** require a specific whole-disk/LVM layout and does **not** require creation of a conventional human account for routine operation.

## First-boot verification

Verify through the current Vincent console/status/diagnostic surfaces that:

- the worker reaches the expected READY/unassigned state;
- immutable installer build provenance is visible;
- current Vincent software identity is shown separately;
- the dedicated `vincent` service identity/runtime is healthy;
- wired/wireless interfaces and active route are visible;
- required self-tests/diagnostics pass or produce actionable failure evidence;
- no private project/fleet/provider authority was silently granted by the installer.

## Evidence handling

Keep concise durable acceptance facts in Git when they remain useful. Large raw logs, screenshots and generated ISO/build products belong in Actions/release artifacts or local test artifacts rather than ordinary Git.

A physical-test report should identify the exact source commit, installer build number, image checksum, target hardware summary, install outcome, first-boot/READY result, relevant network/storage behavior, and defects/retest state without embedding secrets.
