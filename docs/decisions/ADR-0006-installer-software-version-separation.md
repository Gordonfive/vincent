# ADR-0006 — Installer provenance and Vincent software version are separate identities

**Status:** Accepted  
**Decision date:** 2026-08-26T13:35:00-08:00

## Context

Workers are installed from an image but Vincent software is expected to advance through in-place updates. A single build/version value cannot accurately describe both the immutable installation provenance and the current running application.

## Decision

Vincent maintains two distinct lifecycle identities:

1. **Installer build number** — immutable provenance identifying the image/media/build used to create the installation.
2. **Vincent software version** — independently advancing Semantic Version identifying the currently installed Vincent application/runtime.

Status, reports, update metadata, validation, and release tooling must distinguish them explicitly.

## Rationale

This preserves forensic/install provenance while allowing routine Vincent application updates without reimaging or falsifying the worker's origin.

## Consequences

- Updating Vincent changes the software version only.
- Installer provenance remains available after any number of supported updates.
- Release/update compatibility must reason about both the installer/base environment and the target Vincent version where relevant.
- The console/status UI must not label installer build identity as the current Vincent version.

## Supersedes

Earlier wording that treated a single installed build number as both installer provenance and current Vincent software identity.
