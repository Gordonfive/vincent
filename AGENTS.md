# Agent Instructions

Read `docs/PROJECT_START_HERE.md` and Project DNA before changing this repository.

## Authority and safety

- Git is the durable technical authority.
- The owner has final product, security, production, and Project DNA authority.
- Phase gates require explicit acceptance; do not implement a later phase early.
- Never commit credentials, private keys, tokens, auth caches, or production data.
- Never erase hardware, deploy to production, force-push, or delete authoritative remote state without explicit authorization.
- Preserve unexpected dirty work. Do not use destructive cleanup as routine recovery.

## Development rules

- Keep changes bounded, testable, documented, and recoverable.
- Update affected current documentation in the same change.
- Distinguish implemented behavior from verified behavior.
- Prefer standard Debian, systemd, Git, SSH, Docker, and supported Codex interfaces.
- Use task branches; worker completion does not imply integration authority.

## Phase 0 boundary

Phase 0 may create documentation, schemas, tests, prototypes that do not invoke Codex, and implementation plans. It may not provision or erase a worker, install credentials on a worker, or begin unattended execution.

