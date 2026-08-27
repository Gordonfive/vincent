# ADR-0012 — Generic Worker Baseline

**Status:** Accepted  
**Decision date:** 2026-08-27 (America/Sitka)

## Context

Vincent is intended to be a reusable AI worker platform. Earlier development included project-specific tools such as DDEV in the base worker image. That makes the base installation larger, more fragile, and incorrectly couples every worker to one development stack.

## Decision

The generic Vincent baseline excludes project-specific tooling and dependencies.

The base system may include broadly applicable worker/development prerequisites such as Git, GitHub CLI, Docker, networking tools, and the selected AI-agent runtime. Project-specific tools are installed later from the assigned work profile or task requirements.

DDEV is not part of the generic Vincent base installation.

## Rationale

A minimal generic baseline:

- reduces installation and bootstrap failure surface;
- keeps Vincent reusable across unrelated projects;
- avoids unnecessary package and repository dependencies;
- makes project requirements explicit and assignment-driven.

## Consequences

Project assignments that require DDEV or other specialized tooling must provision those requirements after the generic worker reaches a healthy baseline.
