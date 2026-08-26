# Vincent Decision Register

**Register updated:** 2026-08-26T13:40:00-08:00

This register records owner-approved product and architecture decisions that affect Vincent's design or operation.

The roadmap describes what remains to be accomplished. Architecture and specification documents describe the resulting system. This register explains consequential choices and why they were made.

## Decision lifecycle and authority

- `Accepted` — current decision.
- `Superseded` — retained for history but replaced by another decision.
- `Withdrawn` — deliberately abandoned without a direct replacement.
- `Proposed` — under consideration and not authoritative.

Every decision must carry a full timestamp in ISO 8601 format including UTC offset. When accepted decisions conflict, the later authoritative timestamp controls unless explicit supersession resolves the conflict. Do not delete superseded decisions.

## Incremental refresh rule

Agents retain the newest authoritative decision timestamp already incorporated. Before consequential execution, refresh and ingest only newer decisions. If no trustworthy checkpoint exists, read the full current decision set once.

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

Vincent uses two lifecycle identities: immutable **installer build number** for ISO/media/install provenance, and independently advancing **Vincent software version/build** for the currently installed application/runtime. The status screen, reports, validation, and release tooling distinguish them.

## VINCENT-DEC-010 — Network installer can fetch current Vincent release

**Timestamp:** 2026-08-26T13:40:00-08:00  
**Status:** Proposed

### Proposal

Add a Debian-netinstall-like Vincent installation path. When network connectivity is available, the installer may contact the trusted public Vincent release channel associated with `Gordonfive/vincent`, retrieve the current approved Vincent software release, validate it, and install that release instead of being limited to the Vincent software payload bundled when the USB/ISO installer was created.

The installer retains an offline/base path using its bundled validated Vincent payload so installation and recovery do not depend absolutely on GitHub or Internet availability.

The network installer must fetch a published/approved release artifact or signed/validated release manifest. It must not blindly clone and execute arbitrary current `main` contents.

### Intended lifecycle

- The **installer build number** continues to identify the USB/ISO and remains unchanged.
- The **Vincent software version/build** installed during network installation may be newer than the version originally bundled with that installer build.
- After installation, the normal Vincent self-updater from `VINCENT-DEC-008` maintains the application.
- Old but still-compatible USB installers therefore remain useful without constant reimaging merely because Vincent application software has advanced.

### Proposed release target

Version 1.1. This feature is not required to prove the V1.0 worker architecture because V1.0 already provides installation plus in-place Vincent updating. It may be promoted into V1.0 only if implementation is low-risk and does not delay the core V1 proof.

### Safety requirements before acceptance

- authenticated/integrity-checked release metadata and payload;
- explicit compatibility contract between installer build/base Debian environment and fetched Vincent release;
- deterministic fallback to the bundled offline payload when network retrieval fails or the remote release is incompatible;
- clear status/reporting of both installer build and actually installed Vincent software version/build;
- no dependency on private Mission Control state or credentials.

## Existing detailed decisions

- `docs/decisions/ADR-0001-CODEX-EXEC.md` — existing Codex execution ADR; retain and reconcile when next reviewed.
- `docs/decisions/WORKSTREAM_1_ACCEPTANCE.md` — durable workstream acceptance evidence.
