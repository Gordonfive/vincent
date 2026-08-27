# Vincent

**Verified Intelligent Node for Codex Execution, Networking, and Tasks**

Vincent is a public, Linux-first platform for building reproducible, disposable AI development workers. It provides Debian installer/ISO tooling, first-boot provisioning, a worker runtime, self-tests and diagnostics, update mechanisms, Git-based task execution, and optional human-facing development tooling.

Vincent is generic by default. A fresh installation must be able to boot, self-test, update, and reach an unassigned READY state without private Mission Control configuration.

## Documentation

- `docs/README.md` — documentation index and maintenance rules.
- `docs/STATUS.md` — current development state.
- `docs/ROADMAP.md` — release and milestone plan.
- `docs/DECISIONS.md` — accepted product and architecture decisions.
- `docs/ARCHITECTURE.md` — architecture overview.
- `docs/operations/` — build, install, and recovery procedures.
- `SECURITY.md` and `docs/security/` — security policy and threat model.

## Repository boundary

This repository owns:

- Debian 13 ISO and installer source;
- the `vincent` command and first-boot experience;
- worker identity/request generation and generic enrollment interfaces;
- worker runtime, Git integration, logging, reporting, self-tests, and diagnostics;
- Vincent application update and system/toolchain maintenance logic;
- optional VS Code/VSCodium defaults;
- tests, public-safe documentation, checksums, and release artifacts.

This repository must never contain:

- raw passwords, access tokens, private keys, authentication caches, or reusable enrollment credentials;
- private fleet authorization, inventory, assignments, or repository scopes;
- production credentials or private project operating state;
- permanent worker identities baked into installer media.

Private fleet/control-plane state belongs in `Gordonfive/mission-control`. Project-specific requirements, source, tests, and task authority belong in the project repository selected by the operator.

## Development model

Git is the durable technical authority. Use short-lived branches and pull requests for implementation, issues/milestones for active planning, decision records for durable architecture choices, and reproducible validation evidence for build/release acceptance.
