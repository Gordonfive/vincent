# ADR-0007 — Vincent owns system and toolchain maintenance

**Status:** Accepted  
**Decision date:** 2026-08-26T13:10:00-08:00

## Context

A worker that can only be updated by rebuilding installation media becomes operationally expensive and quickly drifts from project needs. At the same time, project-specific version constraints must not be silently ignored by fleet-wide maintenance.

## Decision

Vincent owns routine maintenance of:

- the underlying Debian installation;
- Vincent itself;
- runtime dependencies;
- broadly required development tools;
- project-specific tooling installed for active project environments.

Active project profiles/requirements may constrain versions or update behavior, and Vincent must honor those constraints rather than forcing a globally newest version.

## Rationale

Workers should be maintainable appliances rather than disposable only because routine updates are impossible. Respecting project constraints preserves reproducibility and prevents maintenance from breaking active work.

## Consequences

- Maintenance state is visible in worker health/status.
- Updates are testable/observable and produce clear failure states.
- Significant drift can still be corrected by reprovisioning when that is safer than indefinite repair.
- Fleet policy may later influence timing/channels, but Vincent remains the component that performs local maintenance.
