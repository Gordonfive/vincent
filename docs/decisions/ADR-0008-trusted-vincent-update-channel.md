# ADR-0008 — Public Vincent releases are the trusted in-place update channel

**Status:** Accepted  
**Decision date:** 2026-08-26T13:30:00-08:00

## Context

The installer is a bootstrap/recovery artifact, not an efficient routine application-update mechanism. Workers need a trusted path to advance Vincent software without constantly rebuilding/reimaging USB media.

## Decision

Installed Vincent workers obtain approved Vincent software updates from the public `Gordonfive/vincent` release channel using validated release metadata/artifacts.

Workers must not blindly clone and execute arbitrary current `main` contents as an update mechanism.

Minimum safe in-place self-update belongs in Vincent 1.0 if it does not materially delay core worker acceptance. Advanced rollout/channel/rollback policy may follow in later releases.

## Rationale

This separates installation from application lifecycle, keeps workers current without needless reimaging, and provides an auditable public upstream boundary.

## Consequences

- Release metadata must identify exact software versions/artifacts and integrity evidence.
- Update success changes only the current Vincent software identity, never installer provenance.
- Update failures must preserve recoverability and provide actionable diagnostics.
- Mission Control may later express fleet adoption policy, but it does not replace the public Vincent release source.
