# ADR-0001 — Vincent is a standalone generic worker first

**Status:** Accepted  
**Decision date:** 2026-08-26T13:22:00-08:00

## Context

Earlier worker-platform designs assumed a newly installed worker would immediately depend on a private Mission Control repository/control plane. That couples a public reusable worker image to one operator's private infrastructure and makes basic worker health dependent on fleet services.

## Decision

A fresh Vincent installation is generic and control-source agnostic. It reaches an unassigned READY state independently of Mission Control.

For Vincent V1, an operator can supply and authenticate to a selected Git/project source that provides project/dependency constraints, bounded assignment input, and result/report destinations.

Mission Control is an optional separate managed-fleet control plane entered through explicit enrollment/trust. Vincent's boot, diagnostics, system maintenance, local health, and trusted Vincent updates do not depend on Mission Control.

## Rationale

This keeps the public worker reusable, permits standalone operation, preserves a clean public/private boundary, and allows the fleet control plane to evolve independently.

## Consequences

- Universal installer images contain no private Mission Control repository assumption or credential.
- Standalone workers require a clear READY/unassigned state.
- Mission Control policy is authoritative only after explicit enrollment.
- Vincent architecture documents the Vincent side of the integration boundary; Mission Control owns fleet-control product behavior.
- Early Git-backed work remains useful even before the Mission Control server/API exists.

## Supersedes

Earlier assumptions that every newly installed worker automatically fetches private Mission Control policy/assignments during first boot.
