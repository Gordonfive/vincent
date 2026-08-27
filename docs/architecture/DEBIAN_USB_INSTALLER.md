# Debian USB Installer Architecture

## Approach

Vincent remasters a verified official Debian 13 amd64 installer image and adds the minimum public-safe Vincent provisioning payload required to create a generic worker.

The installer contains:

- Vincent installer configuration and boot entries;
- a reproducible Vincent payload identified by source and installer build metadata;
- first-boot provisioning and appliance services;
- no private credential, permanent worker identity, project authorization, or reusable fleet secret.

## Operator interaction boundary

Vincent must not choose deployment-specific network credentials or destructive storage policy for the operator.

The Debian installer remains interactive for:

- network interface selection;
- Wi-Fi SSID and passphrase when applicable;
- target-disk selection;
- partitioning method and layout;
- final confirmation of disk writes.

Vincent may supply non-destructive defaults such as locale and keyboard. It must not force whole-disk use, guided partitioning, LVM, or a fixed partition recipe.

## Active installer-media guard

The medium currently booting/providing the Vincent installer is not a legitimate installation target. Vincent must identify that active medium and exclude it from the set of target disks presented for partitioning while leaving all legitimate remaining disks operator-selectable.

This guard must not automatically select or prefer another disk.

## Flashing boundary

Building creates an image artifact only. Writing that image to removable media is a separate destructive operation. Flash tooling/procedure must identify the exact removable target using stable device identity, reject ambiguous or mounted targets, require applicable authorization, and verify the bytes written.

## Bootstrap sequence

```text
verified Debian installer source
  -> reproducible Vincent image build
  -> validation + manifest/checksum evidence
  -> operator-authorized removable-media flash
  -> interactive network and storage choices
  -> Debian base installation
  -> dedicated vincent service identity
  -> first-boot Vincent provisioning
  -> local installation identity generation
  -> self-tests and diagnostics
  -> UNASSIGNED READY
  -> operator-selected Git project/control source
```

## Trust boundary

Installer media is public-equivalent provisioning material. Possession grants no private repository, project, Mission Control, or AI-provider authority. Private authorization is established later through explicit operator-approved authentication/enrollment appropriate to the selected source.

## Lifecycle identity

The immutable installer build number identifies the image/media/install provenance. The installed Vincent software version/build is a separate value that may advance later through in-place updates. Status, reports, manifests, and validation must not conflate these identities.

## Reproducibility

Build evidence records the Vincent source, installer build number, Debian source identity/checksum, generated image checksum, and validation results. Uncommitted source must not silently enter a release image. Physical acceptance remains separate from image-build acceptance.
