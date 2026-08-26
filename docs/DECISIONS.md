# Vincent Decision Register

**Register updated:** 2026-08-26T13:30:00-08:00

This register records owner-approved product and architecture decisions that affect Vincent's design or operation.

The roadmap describes what remains to be accomplished. Architecture and specification documents describe the resulting system. This register explains consequential choices and why they were made.

## Decision lifecycle and authority

- `Accepted` — current decision.
- `Superseded` — retained for history but replaced by another decision.
- `Withdrawn` — deliberately abandoned without a direct replacement.
- `Proposed` — under consideration and not authoritative.

Every decision must carry a full timestamp in ISO 8601 format including UTC offset. A date alone is insufficient. When accepted decisions conflict, the later authoritative timestamp controls unless explicit supersession resolves the conflict. The timestamp records owner decision/approval time, not merely file-edit time.

Do not delete superseded decisions. Preserve the decision chain. Detailed ADRs may live under `docs/decisions/`; this file is the concise authoritative register.

## Incremental refresh rule

Agents should retain the newest authoritative decision timestamp already incorporated. Before consequential execution, refresh and ingest only newer decisions. If no trustworthy checkpoint exists, read the full current decision set once.

## VINCENT-DEC-001 — Worker Unix identity

**Timestamp:** 2026-08-26T07:50:00-08:00  
**Status:** Accepted

Vincent uses a dedicated, locked, least-privileged `vincent` Unix service account. It does not run as `nobody`; a normal human login account is not required for routine operation. Root and human recovery/admin access remain separately controlled.

## VINCENT-DEC-002 — Incremental decision refresh before builds

**Timestamp:** 2026-08-26T08:10:43-08:00  
**Status:** Accepted

Before every build, ChatGPT or Codex checks for decisions newer than its last-known decision timestamp. The roadmap carries a full update timestamp and is refreshed only when newer than the agent's checkpoint.

## VINCENT-DEC-003 — Installer disk partitioning remains interactive

**Timestamp:** 2026-08-26T08:12:25-08:00  
**Status:** Accepted

Vincent must not force guided partitioning, LVM, whole-disk use, or a fixed partition recipe. Disk configuration is selected through the normal Debian installer workflow.

## VINCENT-DEC-004 — Build numbers identify images and USB media

**Timestamp:** 2026-08-26T08:20:01-08:00  
**Status:** Accepted

Every Vincent ISO build has a unique monotonically increasing build number consistently represented in the ISO filename/metadata, USB identity, manifests, checksums, logs, and validation evidence.

## VINCENT-DEC-005 — Worker status displays installed build number

**Timestamp:** 2026-08-26T08:30:34-08:00  
**Status:** Accepted

The worker status screen visibly displays the installed build number from durable local build metadata.

## VINCENT-DEC-006 — Vincent V1 is control-source agnostic and uses operator-selected Git

**Timestamp:** 2026-08-26T13:22:00-08:00  
**Status:** Accepted

Fresh Vincent does not know about or depend on a private Mission Control repository. It reaches an unassigned READY state independently. V1 lets the operator supply and authenticate to a Git repository, from which Vincent obtains a project/dependency profile, assignment input, and report/output location. Dedicated Mission Control server software is deferred.

## VINCENT-DEC-007 — Vincent owns system and toolchain maintenance

**Timestamp:** 2026-08-26T13:10:00-08:00  
**Status:** Accepted

Vincent maintains the underlying Debian installation, Vincent itself, runtime dependencies, generic development tools, and project-specific tooling. Active project profiles may impose version constraints that Vincent must honor when maintaining task environments.

## VINCENT-DEC-008 — Public Vincent repository is the upstream self-update source

**Timestamp:** 2026-08-26T13:30:00-08:00  
**Status:** Accepted

### Decision

Installed Vincent workers must periodically check the public `Gordonfive/vincent` upstream for Vincent software updates independently of any connected project/control repository. When an approved newer Vincent release/update is available, the worker must be capable of updating its installed Vincent software in place rather than requiring creation and installation of a new ISO.

The ISO is a bootstrap/recovery/install artifact, not the routine Vincent application upgrade mechanism. Reimaging remains available for recovery, destructive reset, or changes that cannot safely be delivered in place.

The update mechanism must use an explicitly defined trusted release/update channel rather than blindly executing arbitrary current repository contents. Updates must be identifiable by version/build/release metadata, validated before activation, and leave the worker recoverable if update installation or post-update self-checks fail.

### Release target

This capability belongs in **Version 1.0 if it can be implemented without delaying the core V1 proof materially**. The minimum V1 requirement is a reliable upstream update check plus a safe path to update Vincent itself in place. More advanced unattended rollout policy, staged/canary deployment, rollback orchestration, fleet scheduling, or differential updates may move to **Version 1.1**.

If safe in-place Vincent self-update cannot be completed without materially delaying V1, it becomes a required V1.1 feature rather than weakening V1's safety criteria.

### Consequences

- Generic Vincent may know its own public upstream repository/update endpoint even though it must not know any private Mission Control repository by default.
- Update checks work while the worker is unassigned.
- Installed Vincent records its current software release/version separately from the immutable original ISO build number where necessary; an in-place software update must not falsely rewrite the historical installation-image identity.
- Status output should expose current Vincent software version/update state as well as the original installed build identity.
- Update metadata and artifacts must be authenticated/integrity-checked before privileged installation.
- Updating Vincent must run post-update self-checks and must not report READY after an incomplete/broken activation.
- Routine Vincent software updates must not require generating or flashing a fresh ISO.

### Relationship to VINCENT-DEC-007

This specifies the authoritative upstream and lifecycle behavior for the Vincent-software portion of the broader maintenance responsibility established by `VINCENT-DEC-007`.

## Existing detailed decisions

- `docs/decisions/ADR-0001-CODEX-EXEC.md` — existing Codex execution ADR; retain and reconcile when next reviewed.
- `docs/decisions/WORKSTREAM_1_ACCEPTANCE.md` — durable workstream acceptance evidence.
