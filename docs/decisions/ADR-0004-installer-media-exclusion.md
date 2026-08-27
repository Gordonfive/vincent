# ADR-0004 — Exclude active installer media from installation targets

**Status:** Accepted  
**Decision date:** 2026-08-26T10:38:00-08:00

## Context

Physical testing reproduced a dangerous condition on multiple machines: the USB medium currently booting the Vincent installer was presented as an installation/partitioning target.

## Decision

Vincent must reliably identify the active boot/install medium and exclude that device from the target disks offered by the installer.

The exclusion must affect only the active installer medium and must not automatically select, prefer, repartition, or otherwise choose among the remaining legitimate target disks.

## Rationale

The active installer medium is not a legitimate destination for the installation it is currently providing. Offering it creates an avoidable self-destruction path while providing no useful operator choice.

## Consequences

- Installer/build logic must include an active-media guard.
- Validation must confirm the guard is present and does not preselect another disk.
- Physical acceptance must verify the USB is absent from target choices on representative hardware.
- Firmware/storage-detection defects such as RST/VMD/RAID hiding an internal disk are separate issues and must not be conflated with this requirement.
