# Vincent Architecture Decision Records

Architecture Decision Records (ADRs) are the authoritative record of consequential Vincent design decisions.

## Rules

- One consequential decision per ADR.
- ADR filenames use `ADR-####-short-title.md`.
- ADR identifiers are immutable once merged into `main`.
- Every ADR records status, decision date/time, context, decision, rationale, consequences, and supersession relationships where applicable.
- Accepted ADRs are not deleted when later superseded. The old ADR is marked `Superseded` and links to the replacement.
- Do not maintain a second full-text decision register duplicating ADR contents.
- Branch-local draft ADR numbers may be renumbered before merge if required to avoid collision. Once merged, numbers are permanent.
- Requirements and architecture documents should reference the canonical ADR rather than copying its rationale.

## Current ADRs

| ADR | Status | Decision |
|---|---|---|
| [ADR-0001](ADR-0001-standalone-generic-worker.md) | Accepted | Vincent is a generic standalone worker first; operator-selected Git/control source in V1 |
| [ADR-0002](ADR-0002-worker-service-identity.md) | Accepted | Dedicated locked `vincent` Unix service identity |
| [ADR-0003](ADR-0003-installer-interaction-boundary.md) | Accepted | Network and storage choices remain operator-controlled |
| [ADR-0004](ADR-0004-installer-media-exclusion.md) | Accepted | Active installer media is excluded from installation targets |
| [ADR-0005](ADR-0005-installer-build-provenance.md) | Accepted | Monotonic installer build identity and durable provenance |
| [ADR-0006](ADR-0006-installer-software-version-separation.md) | Accepted | Installer provenance and Vincent software version are separate identities |
| [ADR-0007](ADR-0007-system-toolchain-maintenance.md) | Accepted | Vincent owns Debian/toolchain/runtime maintenance subject to project constraints |
| [ADR-0008](ADR-0008-trusted-vincent-update-channel.md) | Accepted | Public Vincent releases are the trusted in-place update channel |
| [ADR-0009](ADR-0009-runtime-network-resilience.md) | Accepted | Wired/Wi-Fi failover and layered diagnostics are worker requirements |
| [ADR-0010](ADR-0010-network-installer.md) | Proposed | Compatible installers may fetch the current approved Vincent release |
| [ADR-0011](ADR-0011-ai-provider-adapter-enrollment.md) | Accepted | Provider-neutral adapters; Vincent performs provider-specific local enrollment |
| [ADR-0012](ADR-0012-generic-worker-baseline.md) | Accepted | Generic worker baseline excludes project-specific tooling |
| [ADR-0013](ADR-0013-dns-resolver-policy.md) | Accepted | Resolver policy avoids unnecessary dependence on a single provider |
| [ADR-0014](ADR-0014-private-development-public-release.md) | Accepted | Development remains private until a deliberate public release |
| [ADR-0015](ADR-0015-versioning-and-build-identifiers.md) | Accepted | Vincent, installer, and Mission Control use independent SemVer and build counters |
| [ADR-0016](ADR-0016-rootless-container-runtime.md) | Accepted | Routine worker containers use rootless Podman instead of root-equivalent Docker-group access |

## Migrated legacy decisions

The former monolithic decision register was retired because concurrent branches reused identifiers for different decisions. The ADR migration preserves the decisions themselves while discarding ambiguous legacy numbering as active authority.

Historical identifiers may appear in Git history or traceability evidence only. Active documentation must reference the ADRs above.
