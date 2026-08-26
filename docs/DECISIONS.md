# Vincent Decision Register

**Register updated:** 2026-08-26T08:12:25-08:00

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

## Incremental refresh rule

Agents should retain the timestamp of the newest authoritative decision they have already incorporated. Before any build, release, flash-preparation step, or other consequential execution, ChatGPT or Codex must refresh the decision register and ingest every decision newer than that remembered timestamp.

Agents do **not** need to re-read older decisions that are already known and whose authoritative timestamps are at or before the agent's recorded decision checkpoint. If the agent has no trustworthy checkpoint, it must read the full current decision set once and establish one.

A build must not proceed from stale decision knowledge. If a newer decision changes build requirements, architecture, safety gates, account behavior, naming, credentials, installer behavior, or acceptance criteria, the build instructions and source must be reconciled first.

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

## VINCENT-DEC-002 — Incremental decision refresh before builds

**Timestamp:** 2026-08-26T08:10:43-08:00  
**Status:** Accepted

### Decision

Before every build, ChatGPT or Codex must check the authoritative decision register for decisions newer than its last-known decision timestamp and incorporate those changes before execution. Previously known decisions do not need to be re-read unless the agent lacks a trustworthy decision checkpoint or a newer decision indicates that earlier material must be revisited.

The roadmap must carry a full last-updated timestamp so an agent can determine whether its roadmap knowledge is stale and refresh only when necessary.

### Rationale

This preserves authoritative owner decisions at build time while avoiding repeated re-reading of unchanged project history. It also gives long-lived agents, new sessions, and concurrent workers an inexpensive freshness check before consequential operations.

### Consequences

- Build workflows need an explicit decision-refresh gate before build execution.
- Agents should record the newest incorporated decision timestamp in their work logs/handoffs when practical.
- `docs/ROADMAP.md` must expose an ISO 8601 last-updated timestamp with UTC offset.
- If the roadmap timestamp is newer than an agent's known roadmap checkpoint, the roadmap must be refreshed before continuing roadmap-directed work.

## VINCENT-DEC-003 — Installer disk partitioning remains interactive

**Timestamp:** 2026-08-26T08:12:25-08:00  
**Status:** Accepted

### Decision

Remove Vincent-specific installer code that automatically selects guided partitioning with LVM. Disk configuration must be chosen during installation through the normal Debian installer partitioning workflow and defaults rather than being forced by Vincent automation.

Vincent may provide documentation or recommendations, but it must not preselect guided partitioning, LVM, whole-disk use, a partition recipe, or an equivalent destructive disk-layout choice on behalf of the installer operator.

### Rationale

Disk layout is hardware- and deployment-specific and is sufficiently destructive that the normal installer should present the available choices to the operator. Keeping partition selection interactive also avoids baking one storage policy into a reusable Vincent image.

### Consequences

- Remove any active preseed, installer configuration, scripts, or build logic that force guided partitioning or LVM.
- ISO validation must confirm that the normal Debian disk-partitioning choice remains available during installation.
- Physical-install acceptance must no longer require a specific whole-disk or LVM layout unless a later decision explicitly reintroduces one.
- Destructive device-selection and flashing authorization gates remain separate and unchanged.

### Supersedes

Earlier requirements or implementation assumptions that Vincent automatically selects whole-disk guided partitioning with LVM or a fixed partitioning recipe.

## Existing detailed decisions

- `docs/decisions/ADR-0001-CODEX-EXEC.md` — existing Codex execution ADR. Retain as a detailed ADR; reconcile/index its decision here when that architecture is next reviewed.
- `docs/decisions/WORKSTREAM_1_ACCEPTANCE.md` — acceptance evidence rather than a general architecture decision; retain as durable workstream evidence.
