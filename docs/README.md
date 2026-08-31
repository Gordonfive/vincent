# Vincent Documentation

This directory contains the canonical current documentation for Vincent.

## Document authority

Each document type has one purpose. Do not duplicate the same editable source of truth across multiple files.

| Document | Purpose |
|---|---|
| [`PRODUCT.md`](PRODUCT.md) | Component definition, users, goals, non-goals, principles, and boundaries |
| [`REQUIREMENTS.md`](REQUIREMENTS.md) | Stable numbered functional and non-functional requirements |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Current high-level system architecture |
| [`architecture/`](architecture/) | Detailed component/design documentation |
| [`decisions/`](decisions/) | Architecture Decision Records (ADRs) and decision index |
| [`ROADMAP.md`](ROADMAP.md) | Vincent release/component outcomes and sequencing |
| [`STATUS.md`](STATUS.md) | Current implementation, validation, active blockers, and temporary development state |
| [`operations/`](operations/) | Supported operational procedures and acceptance runbooks |
| [`protocols/`](protocols/) | Protocol/schema contracts |
| [`history/`](history/) | Limited migration/traceability evidence retained only when it explains current authority |

Repository root documents provide conventional entry points:

- [`../README.md`](../README.md) — component/repository overview
- [`../AGENTS.md`](../AGENTS.md) — coding-agent instructions
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — repository workflow
- [`../SECURITY.md`](../SECURITY.md) — security policy
- [`../CHANGELOG.md`](../CHANGELOG.md) — release-level change history

## Authority rules

1. Git on `main` is the durable technical authority for Vincent.
2. `PRODUCT.md` defines Vincent component intent and boundaries.
3. `REQUIREMENTS.md` defines what Vincent must do. Requirement identifiers are permanent once merged.
4. ADRs record consequential design choices and their rationale. ADR identifiers are immutable once merged.
5. Architecture documents describe the current design resulting from accepted requirements and ADRs.
6. `ROADMAP.md` describes intended release outcomes; it is not a backlog or current-status log.
7. `STATUS.md` records temporary/current implementation and physical-test state.
8. GitHub issues are the unscheduled feature/work backlog. Pull requests carry integration/review evidence.
9. Historical migration/reset material is not an active source of direction. Git history is the archive after useful facts have been distilled.
10. `logrusbox/fleet` owns the overall Fleet roadmap, cross-component integration issues, and Fleet governance. Vincent documentation owns the worker component and the Vincent side of the integration boundary only.

## Documentation lifecycle

- Change component intent deliberately in `PRODUCT.md` and update affected requirements/ADRs.
- Add or supersede requirements without reusing identifiers.
- Record consequential architecture choices as ADRs rather than burying decisions in roadmap/status prose.
- Move scheduled work into the roadmap; keep unscheduled ideas as issues.
- Remove stale temporary status once it no longer affects current work.
- Keep raw logs, screenshots, generated images, large build outputs, and CI bundles outside ordinary Git when practical; use Actions/release artifacts instead.
- Documentation changes are reviewed and validated through the same pull-request/CI process as code.

## Fresh-session start order

A new human, ChatGPT session, or coding agent should normally read:

1. repository `README.md`;
2. `AGENTS.md` when acting as a coding agent;
3. this documentation index;
4. `PRODUCT.md` and `REQUIREMENTS.md`;
5. `STATUS.md` for current state;
6. the relevant roadmap, ADRs, architecture, operations, and active issues/PRs for the task at hand.

Permanent project-start, continuation-handoff, planned-feature-backlog, and retired product-intent documents are intentionally not part of the current documentation model.
