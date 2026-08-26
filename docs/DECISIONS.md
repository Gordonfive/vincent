# Vincent Decision Register

**Register updated:** 2026-08-26T13:35:00-08:00

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

Every Vincent installer image build has a unique monotonically increasing installer build number consistently represented in the ISO filename/metadata, USB identity, manifests, checksums, logs, and validation evidence.

## VINCENT-DEC-005 — Worker status displays installed build number

**Timestamp:** 2026-08-26T08:30:34-08:00  
**Status:** Superseded by `VINCENT-DEC-009`

The worker status screen displays build identity. `VINCENT-DEC-009` separates installer provenance from current Vincent software identity.

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

Installed Vincent workers periodically check the public `Gordonfive/vincent` upstream for approved Vincent software updates and update in place. The ISO remains a bootstrap/recovery/install artifact rather than the routine application upgrade mechanism. Updates use a trusted, validated release channel and preserve recoverability.

Minimum safe self-update belongs in V1.0 if it does not materially delay the core proof; advanced rollout/rollback policy may move to V1.1.

## VINCENT-DEC-009 — Installer build and Vincent software build are separate identities

**Timestamp:** 2026-08-26T13:35:00-08:00  
**Status:** Accepted

### Decision

Vincent uses two separate build/version identities:

1. **Installer build number** — identifies the ISO/install media and the installation provenance of a worker. It is immutable for that installed system and does not change when Vincent updates itself in place.
2. **Vincent software build/version** — identifies the currently installed Vincent application/runtime release. It may advance independently through in-place updates from the public Vincent upstream.

The two identifiers may initially match or be derived from the same source revision, but they must never be treated as the same lifecycle value.

### Consequences

- ISO filename, ISO/volume metadata, USB label, installer manifest, installer checksums, and installation provenance use the **installer build number**.
- Vincent release/update artifacts and update metadata use the **Vincent software build/version**.
- The worker status screen must display both values clearly, for example `Installer build: 0017` and `Vincent version/build: 1.0.3 / 0042`.
- In-place Vincent updates change only the Vincent software build/version, not the installer build number.
- Reports and diagnostics must record both identifiers when relevant.
- Validation must fail if installer artifacts disagree on installer build identity or if Vincent update artifacts disagree on software build/version identity.
- Future release tooling may choose semantic versions, monotonic build numbers, commit identifiers, or a combination for Vincent software, but installer and software identities remain distinct.

### Supersedes

`VINCENT-DEC-005` to the extent it referred to one ambiguous installed build number, and any wording elsewhere that uses `build number` without distinguishing installer provenance from current Vincent software identity.

## Existing detailed decisions

- `docs/decisions/ADR-0001-CODEX-EXEC.md` — existing Codex execution ADR; retain and reconcile when next reviewed.
- `docs/decisions/WORKSTREAM_1_ACCEPTANCE.md` — durable workstream acceptance evidence.
