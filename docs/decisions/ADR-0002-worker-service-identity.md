# ADR-0002 — Dedicated Vincent Unix service identity

**Status:** Accepted  
**Decision date:** 2026-08-26T07:50:00-08:00

## Context

A dedicated autonomous worker needs predictable filesystem ownership, auditing, service integration, and least-privilege behavior. Using `nobody` provides poor ownership/audit semantics, while requiring a conventional human account unnecessarily couples appliance operation to interactive credentials.

## Decision

Vincent runtime automation uses a dedicated locked non-human Unix service account named `vincent`.

The account must not permit normal password login and must receive only required groups, filesystem permissions, capabilities, and narrowly defined privileged interfaces. It does not receive unrestricted sudo.

Root remains reserved for installer/bootstrap and narrowly controlled system operations. Human administrative/recovery access is separate and optional.

## Rationale

A dedicated service identity provides clear ownership, least-privilege isolation, auditability, and conventional systemd integration without requiring a human login account for normal operation.

## Consequences

- Installation must support a worker with no conventional human account.
- Runtime files/repositories requiring persistent worker ownership belong to `vincent` or another explicitly documented system identity.
- Privileged operations use root-owned helpers/services or another narrow interface rather than broad sudo.
- Troubleshooting must not require converting `vincent` into a normal privileged login.

## Supersedes

Earlier assumptions requiring a `gitboy`/human installer account or using `nobody` for routine worker execution.
