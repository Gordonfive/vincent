# Vincent Documentation

This directory contains the current product, architecture, operations, security, protocol, decision, and validation documentation for Vincent.

## Start here

1. `../AGENTS.md` — repository rules for automated contributors.
2. `STATUS.md` — current development state.
3. `ROADMAP.md` — release and milestone plan.
4. `DECISIONS.md` and `decisions/` — accepted architecture/product decisions.
5. `ARCHITECTURE.md` and `architecture/` — current system design.
6. `operations/` — build, install, recovery, and operating procedures.
7. `security/` — trust and credential boundaries.
8. `protocols/` — worker/task protocol contracts.

## Documentation classes

- **Product overview:** root `README.md`.
- **Current state:** `STATUS.md`.
- **Strategic plan:** `ROADMAP.md` and `PLANNED_FEATURES.md`.
- **Architecture:** `ARCHITECTURE.md` and `architecture/`.
- **Decisions:** `DECISIONS.md` and `decisions/`.
- **Operations:** `operations/`.
- **Evidence:** `reports/` for current or still-relevant validation evidence.

Completed migration/consolidation material should not remain in the active tree merely for history; Git history already provides provenance.

## Maintenance rules

- Keep operational documentation aligned with accepted decisions and current implementation.
- Do not duplicate volatile status across README, roadmap, handoff, and reports.
- Put active work in issues/pull requests; put milestone-level intent in the roadmap.
- Record consequential architecture choices as ADRs or indexed decisions.
- Remove superseded operational instructions after useful rationale has been retained.
- Historical specification material should be distilled into current requirements/decisions before it is removed from the active tree.
