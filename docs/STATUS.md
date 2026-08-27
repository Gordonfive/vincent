# Vincent Status

**Updated:** 2026-08-27T08:17:00-08:00

## Current state

Repository consolidation is complete. Vincent and Mission Control are the only repositories required for normal project recovery and ongoing development.

The current product priority is Vincent 1.0 installer and worker proof: install reproducibly on disposable hardware, reach a generic unassigned READY state, self-test without requiring an interactive human login, connect to an operator-selected Git repository, complete one bounded task, and report results.

## Active development

Installer/physical-test development is active and may be ahead of `main` on a temporary workstream branch. Before modifying installer or ISO documentation, inspect current branches and pull requests and reconcile the newest accepted decisions rather than restoring older behavior from `main`.

Current accepted design direction includes:

- dedicated least-privileged `vincent` service identity;
- interactive operator control of network and disk choices;
- exclusion of the active installer medium from installation targets;
- visible, immutable installer-build provenance separate from the current Vincent software version/build;
- local self-tests and diagnostics suitable for appliance-style physical testing;
- generic READY operation without private Mission Control configuration;
- in-place Vincent and Debian/toolchain maintenance after installation.

## Documentation note

`docs/specification/` is a historical long-form source that predates several current decisions and naming changes. It must not override `docs/DECISIONS.md`. Useful requirements should be distilled into current product/architecture documentation before that archive is removed from the active tree.

## Recovery

Read `AGENTS.md`, `docs/README.md`, this file, `docs/DECISIONS.md`, and `docs/ROADMAP.md`, then inspect active branches, issues, pull requests, and task-specific reports before acting.
