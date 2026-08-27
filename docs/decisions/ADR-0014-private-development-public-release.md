# ADR-0014 — Private Development Before Public Release

**Status:** Accepted  
**Decision date:** 2026-08-27 (America/Sitka)

## Context

Vincent is intended to become a publicly available product, but active development is not yet ready for public release or outside contributions.

## Decision

Vincent development remains private until a deliberate public-release decision is made.

Public release is a product/release milestone, not an automatic consequence of repository maturity or licensing preparation. Before publication, the repository must be reviewed for private operational information, secrets, deployment-specific material, and documentation that should not ship with the public product.

## Rationale

Keeping development private allows architecture, naming, installer behavior, and repository boundaries to stabilize without implying production readiness or inviting unsupported contributions.

## Consequences

- Current private repository state is intentional.
- Public licensing/release preparation may proceed while the repository remains private.
- Publication requires an explicit release gate and repository-content review.
