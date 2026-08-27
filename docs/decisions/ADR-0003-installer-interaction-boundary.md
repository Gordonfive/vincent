# ADR-0003 — Installer network and storage choices remain operator-controlled

**Status:** Accepted  
**Decision date:** 2026-08-26T10:30:46-08:00

## Context

Earlier installer prototypes automated network and disk choices in pursuit of unattended provisioning. Physical testing showed that network credentials, interface selection, target disks, and partitioning are deployment-specific and sufficiently destructive/sensitive that Vincent should not select them on the operator's behalf.

## Decision

Vincent preserves normal interactive Debian Installer choices for:

- network interface selection;
- Wi-Fi SSID selection and passphrase entry when applicable;
- target-disk selection;
- partitioning method/layout;
- final disk-write confirmation.

Vincent may automate non-destructive appliance defaults such as `en_US.UTF-8` locale and `us` keyboard layout.

Vincent must not preseed a Wi-Fi passphrase, target disk, guided partitioning/LVM choice, whole-disk use, fixed partition recipe, or equivalent destructive selection.

## Rationale

This keeps credentials and destructive device/layout choices with the operator while still allowing the installer to automate safe appliance defaults.

## Consequences

- Boot parameters/build logic must not enable an automatic-install mode that suppresses required network/storage questions.
- ISO validation must detect forced partitioning or preselected targets.
- Physical acceptance evaluates successful operator-selected installs rather than requiring one storage layout.
- Account behavior remains governed separately by ADR-0002.

## Supersedes

Earlier requirements for forced whole-disk guided LVM/unattended network selection.
