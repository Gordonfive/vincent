# Vincent

**Verified Intelligent Node for Codex Execution, Networking, and Tasks**

Vincent is the public, Linux-first worker platform for reproducible Codex development machines. It provides the Debian installer, first-boot bootstrap, enrollment client, worker runtime, health reporting, and optional VS Code workspace defaults.

Vincent does not contain private fleet configuration, project authority, permanent credentials, or production access. Those belong to a private Mission Control repository and the assigned project repository.

## Repository boundary

This repository owns:

- reproducible Debian 13 ISO and installer source;
- the `vincent` command and first-boot experience;
- generation of a unique worker identity and enrollment request;
- generic Codex, Git, service, logging, reporting, and health components;
- optional VS Code/VSCodium defaults;
- tests, public documentation, checksums, and release artifacts.

This repository must never contain:

- private keys, passwords, access tokens, or authentication caches;
- owner or fleet credentials;
- private infrastructure configuration;
- project-specific operating instructions;
- permanent worker identities;
- unrestricted or shared fleet credentials.

## Authority chain

1. Vincent's built-in safety boundaries.
2. Private Mission Control fleet policy.
3. The assigned project's `AGENTS.md` and Project DNA.
4. The bounded task packet.
5. Interactive operator direction.

Lower layers may add specificity but cannot weaken higher-level security restrictions.

## Migration

Vincent replaces the public GitBoy name. The implementation and ISO work currently preserved in `Gordonfive/codex-worker-platform` will be migrated here with history and validation evidence. `Gordonfive/GitBoy` remains a legacy public bootstrap repository until migration is verified.
