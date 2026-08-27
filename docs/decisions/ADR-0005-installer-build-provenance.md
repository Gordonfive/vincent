# ADR-0005 — Installer builds have unique durable provenance

**Status:** Accepted  
**Decision date:** 2026-08-26T08:20:01-08:00

## Context

Physical installer testing requires unambiguous correlation among source, ISO files, USB media, installed systems, manifests, checksums, and test evidence. Reusing or omitting build identities makes it easy to test or install the wrong image.

## Decision

Every Vincent installer image build receives a unique monotonically increasing installer build number.

The same build identity must be represented consistently in the generated image filename, supported ISO/volume metadata, USB/media identity, build manifest, checksum/validation evidence, and durable installed provenance.

Installer build identifiers may contain an internal revision (for example `0021.2`) when needed, but they remain installer-build identities rather than software versions.

## Rationale

A durable build identity makes physical media and installed provenance traceable to exact validation evidence and source state.

## Consequences

- Build tooling allocates/records the build number before image creation.
- Validation fails when build identifiers disagree.
- Flash/install evidence records the build number.
- Installer build numbering is lifecycle-independent from Vincent software Semantic Versioning; see ADR-0006.
