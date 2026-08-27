# ADR-0015 — Independent semantic versions and build identifiers

**Status:** Accepted  
**Decision date:** 2026-08-27T13:17:00-08:00

## Context

Vincent, the Vincent installer, and Mission Control are distinct software components. During prototype development, each may undergo many small implementation and physical-test iterations that do not justify a semantic-version change. Exact build provenance is still required for reproducibility and debugging.

Vincent and its installer share a repository but have independent implementation lifecycles. Mission Control is a separate component with its own lifecycle.

## Decision

All three components use Semantic Versioning independently:

- Vincent: current development version `0.1.0`.
- Vincent installer: current development version `0.1.0`.
- Mission Control: current development version `0.1.0`.

Each component also has an independent monotonically increasing build counter:

- Vincent runtime/platform build numbering starts at `0001`.
- Vincent installer retains its existing installer build sequence; the current consolidated installer build is `0022`.
- Mission Control build numbering starts at `0001`.

Semantic versions change only at meaningful product/release boundaries. Build numbers may advance for implementation or test iterations without changing the semantic version. Build counters are independent and must never be inferred from one another.

Within `Gordonfive/vincent`:

- `/VERSION` is the Vincent semantic version.
- `/BUILD_NUMBER` is the Vincent runtime/platform build number.
- `/installer/debian13/VERSION` is the installer semantic version.
- `/installer/debian13/BUILD_NUMBER` is the installer build number.

Mission Control owns its equivalent version/build files in its own repository.

## Rationale

This separates release compatibility from exact test/build provenance and prevents installer iterations from falsely changing Vincent runtime identity or vice versa.

## Consequences

- Status, diagnostics, manifests, releases and test evidence should identify the relevant semantic version and build number when practical.
- Installer provenance remains distinct from the currently installed Vincent runtime version/build as required by ADR-0006.
- A deployed system may therefore report both its immutable installer provenance and its independently advancing Vincent runtime identity.
- Build-number increments alone do not imply a new semantic release.

## Relationship to existing decisions

This refines ADR-0005 and ADR-0006; it does not supersede them.
