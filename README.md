# Vincent

**Verified Intelligent Node for Codex Execution, Networking, and Tasks**

> **Project recovery:** a fresh ChatGPT/Codex project should begin with `docs/PROJECT_START_HERE.md`, then read `docs/ROADMAP.md` and `docs/CONTINUATION_HANDOFF.md`.

Vincent is the public, Linux-first worker platform for reproducible Codex development machines. It provides the Debian installer, first-boot bootstrap, enrollment client, worker runtime, health reporting, and optional VS Code workspace defaults.

Vincent does not contain private fleet configuration, project authority, permanent credentials, or production access. Those belong to the private `Gordonfive/mission-control` repository and the assigned project repository.

## Repository boundary

This repository owns:

- reproducible Debian 13 ISO and installer source;
- the `vincent` command and first-boot experience;
- generation of a unique worker identity and enrollment request;
- generic Codex, Git, service, logging, reporting, and health components;
- optional VS Code/VSCodium defaults;
- tests, public documentation, checksums, release artifacts, and preserved public legacy history.

This repository must never contain:

- private keys, passwords, access tokens, or authentication caches;
- owner or fleet credentials;
- private infrastructure configuration that belongs in Mission Control;
- private project-specific operating state;
- permanent worker identities;
- unrestricted or shared fleet credentials.

## Authority chain

1. Vincent's built-in safety boundaries.
2. Private Mission Control fleet policy.
3. The assigned project's `AGENTS.md` and Project DNA.
4. The bounded task packet.
5. Interactive operator direction.

Lower layers may add specificity but cannot weaken higher-level security restrictions.

## Migration state

The generic worker implementation, installer, bootstrap, runtime, tests, Project DNA, protocols, Workstream 1 acceptance evidence, Workstream 2 corrections, and complete specification preservation records are consolidated on the migration-completion candidate. The default branch should be treated as authoritative only after the recorded consolidation merge and validation gates are complete.
