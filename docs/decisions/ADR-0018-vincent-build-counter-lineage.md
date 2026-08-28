# ADR-0018 — Vincent runtime build counter continues at 0022

**Status:** Accepted  
**Decision date:** 2026-08-27 (America/Sitka)

## Context

ADR-0015 established independent Semantic Versions and monotonically increasing build counters for Vincent, the installer, and the control-plane product. It recorded the Vincent runtime/platform counter as starting at `0001`.

The owner subsequently clarified that Vincent itself had already undergone the implementation refinements represented by the earlier shared build history. Several installer build increments were caused by Vincent changes rather than installer-only changes. Vincent therefore begins its independent runtime/platform counter at `0022`, not `0001`.

The installer counter also happened to be `0022` at the point of separation, but the counters are independent from that point onward and may diverge immediately.

## Decision

- Vincent runtime/platform build identity starts its independent lineage at `0022`.
- Vincent installer build identity retains its own existing lineage, also `0022` at separation.
- Equal numeric values at the separation point do not imply a shared counter.
- Future Vincent and installer changes increment only the build counter(s) for the component(s) actually changed/tested.
- Semantic Versioning remains independent of both build counters.

Within `Gordonfive/vincent`:

- `/BUILD_NUMBER` is the independent Vincent runtime/platform build counter.
- `/installer/debian13/BUILD_NUMBER` is the independent installer build counter.

The value `0022` records the separation point, not a permanently synchronized value. Subsequent changes advance whichever component counters apply.

## Rationale

Continuing Vincent at 0022 preserves useful implementation provenance rather than falsely implying the current runtime is its first build. Independent counters still allow later installer-only and runtime-only work to diverge correctly.

## Consequences

- Issue #20 and version/build tooling must treat the two files as separate values even when they happen to match.
- Tests must not infer one counter from the other.
- Installer provenance and installed Vincent runtime identity remain separate as required by ADR-0006 and ADR-0015.

## Relationship

This ADR amends ADR-0015 only where ADR-0015 states that the Vincent runtime/platform build counter starts at `0001`. All other independent-version/build-counter decisions in ADR-0015 remain accepted.
