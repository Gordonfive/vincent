# ADR-0010 — Compatible installer may fetch the current approved Vincent release

**Status:** Proposed  
**Decision date:** 2026-08-26T13:40:00-08:00  
**Target:** Vincent 1.1.x unless promoted by a later accepted decision

## Context

Vincent software can advance faster than physical installation media. Requiring USB reimaging for every Vincent application release is unnecessary if an older installer remains compatible with the newer application.

## Proposed decision

When network connectivity is available, a compatible Vincent installer may contact the trusted public Vincent release channel, retrieve and validate the current compatible approved Vincent release, and install that release instead of being limited to the payload bundled with the USB/ISO.

The installer must retain a validated bundled offline/recovery payload and deterministically fall back to it when network retrieval fails or the current release is incompatible.

The installer must fetch published/approved release metadata/artifacts; it must not blindly clone and execute current `main`.

## Rationale

This would keep older compatible installation media useful while preserving offline recovery and exact provenance.

## Consequences if accepted

- Installer build identity remains unchanged regardless of which compatible Vincent software version is installed.
- Release metadata needs an installer/base compatibility contract.
- Network retrieval requires authenticated/integrity-checked metadata and payloads.
- Status/reporting must show both installer provenance and the actually installed Vincent version.
- Network failure/incompatibility falls back safely to the bundled payload.
