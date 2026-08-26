# Vincent Decision Register

This register records owner-approved product and architecture decisions that affect Vincent's design or operation.

The roadmap describes what remains to be accomplished. Architecture and specification documents describe the resulting system. This register explains consequential choices and why they were made.

## Decision lifecycle and authority

- `Accepted` — current decision.
- `Superseded` — retained for history but replaced by another decision.
- `Withdrawn` — deliberately abandoned without a direct replacement.
- `Proposed` — under consideration and not authoritative.

Every decision must carry a full timestamp in ISO 8601 format including UTC offset, for example `2026-08-26T07:50:00-08:00`. A date alone is insufficient.

When two accepted decisions genuinely conflict and neither explicitly supersedes the other, the decision with the later authoritative timestamp controls. Explicit `Supersedes`/`Superseded by` relationships should still be recorded whenever a conflict is known. If timestamps are identical or ordering remains ambiguous, do not guess: require owner clarification and record the resolving decision with a new timestamp.

The timestamp represents when the owner made or explicitly approved the decision, not when a worker happened to edit the file. Git commit timestamps provide additional provenance but do not replace the decision timestamp.

Do not delete an accepted decision merely because the design later changes. Mark it `Superseded` and identify its replacement. Git history remains useful, but the current document must also make the decision chain understandable without reconstructing old commits.

Detailed ADRs may live under `docs/decisions/`. This file is the human-readable index and concise decision history. New ADRs and decision records must follow the same timestamp and conflict-resolution rule.

## VINCENT-DEC-001 — Worker Unix identity

**Timestamp:** 2026-08-26T07:50:00-08:00  
**Status:** Accepted

### Decision

Vincent workers use a dedicated local `vincent` Unix service account for automation. Vincent does not run as `nobody`, and installation does not require creation of a conventional human login account.

The `vincent` account is created automatically, is non-human, does not permit normal password login, and receives only required filesystem permissions, groups, capabilities, and privileged interfaces. It does not receive unrestricted sudo.

Root is reserved for installer/bootstrap and narrowly controlled system operations. Normal remote root login is disabled. Human administrative/recovery access is separate and optional, provisioned deliberately when required.

### Rationale

A dedicated service identity provides predictable ownership, least-privilege isolation, useful auditing, and clean systemd/service integration. `nobody` is a shared catch-all identity and provides poor ownership and audit semantics. A normal human account would unnecessarily couple unattended appliance operation to interactive credentials.

### Consequences

- The Debian installer must support unattended installation without prompting for an arbitrary human username/password.
- Runtime files and repositories requiring persistent ownership belong to `vincent` or another explicitly documented system identity.
- Privileged operations must use narrow root-owned helpers/systemd interfaces rather than broad sudo authority.
- Interactive troubleshooting must not require converting `vincent` into a normal privileged login account.
- Recovery/admin authentication requires a separately designed mechanism.

### Supersedes

Earlier implementation assumptions that a normal installer-created user such as `gitboy` or another human account is required for routine worker operation.

## Existing detailed decisions

- `docs/decisions/ADR-0001-CODEX-EXEC.md` — existing Codex execution ADR. Retain as a detailed ADR; reconcile/index its decision here when that architecture is next reviewed.
- `docs/decisions/WORKSTREAM_1_ACCEPTANCE.md` — acceptance evidence rather than a general architecture decision; retain as durable workstream evidence.
