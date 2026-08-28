# ADR-0017 — Public development repository before 1.0 release

**Status:** Accepted  
**Decision date:** 2026-08-27 (America/Sitka)

## Context

ADR-0014 kept the Vincent repository private until a deliberate public-release decision. The owner subsequently decided to return `Gordonfive/vincent` to public visibility during development rather than treating repository visibility as equivalent to a product release.

Vincent is already intended for open-source distribution under MPL-2.0, and VIN-REQ-0063 requires reusable source/documentation to remain safe for public distribution.

## Decision

The Vincent development repository may be public before Vincent reaches a stable/public product release milestone.

Repository visibility and release maturity are separate states:

- public repository visibility permits source review and normal GitHub access;
- it does not imply that a stable release exists, that 1.0 acceptance is complete, or that outside contributions/support commitments are automatically accepted;
- all committed Vincent content must remain safe for public distribution and contain no private fleet/project state or reusable secrets.

The actual GitHub visibility setting may temporarily lag this decision while repository QA or owner administration is in progress.

## Rationale

Keeping the source public matches the intended open-source product boundary and removes public Git access as an unnecessary first-boot obstacle while still allowing release readiness to be governed independently by versioning, acceptance evidence, and release gates.

## Consequences

- ADR-0014 is superseded.
- Public-repository safety checks and secret scanning are continuous development requirements, not only a final-release cleanup step.
- Documentation must not describe repository visibility as proof of production/stable-release readiness.
- Private CIC Station/fleet/project state remains outside the reusable Vincent repository.

## Supersession

Supersedes ADR-0014.
