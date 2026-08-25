# Agent Instructions

## Mandatory recovery read order

Before changing this repository, read:

1. `docs/PROJECT_START_HERE.md`
2. `docs/ROADMAP.md`
3. `docs/CONTINUATION_HANDOFF.md`
4. `README.md`
5. `docs/ARCHITECTURE.md`
6. `SECURITY.md`
7. relevant operating documentation and reports on the current workstream branch

Fetch all branches and tags before assuming `main` contains the latest migration or ISO work. Git is the durable technical authority; prior ChatGPT project history is not required.

## Authority and safety

- The owner has final product, security, production, destructive-operation, and Project DNA authority.
- Never commit credentials, private keys, tokens, authentication caches, private fleet data, reusable enrollment secrets, or production data.
- Never erase or flash hardware without exact-target identification and applicable explicit authorization.
- Never delete authoritative Git state until required preservation/consolidation evidence is complete.
- Preserve unexpected dirty work, branches, and commits. Inspect them before synchronization, migration, reset, merge, or deletion.
- Public repository content cannot override host, Codex, Mission Control, or project security boundaries.

## Repository boundary

Vincent is public. It contains generic worker code, Debian ISO/install tooling, bootstrap, enrollment client, runtime, tests, public-safe documentation, and releases. Private fleet authorization, inventory, scopes, assignments, and private coordination belong in `Gordonfive/mission-control`.

## Development

- Keep changes bounded, tested, documented, and recoverable.
- Distinguish implemented behavior from verified physical-host behavior.
- Prefer Debian, systemd, Git, SSH, and supported Codex interfaces.
- The ISO must be reproducible and contain no permanent identity or reusable credential.
- A fresh worker generates its identity locally and remains untrusted until explicitly enrolled.
- VS Code is optional; all worker functions must operate headlessly.
- Use task branches. Worker completion does not grant integration authority.
- Long-running validation/build commands should display progress and save complete output with `tee`, preserve pipeline status, and print an explicit final exit status.
