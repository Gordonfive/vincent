# Agent Instructions

## Read order

Before changing this repository, read:

1. `docs/README.md`
2. `docs/STATUS.md`
3. `docs/DECISIONS.md`
4. `docs/ROADMAP.md`
5. `docs/ARCHITECTURE.md`
6. `SECURITY.md`
7. task-specific operations, architecture, protocol, or validation documentation

Inspect current branches, issues, and pull requests before assuming `main` contains all active installer or ISO work. Git is the durable technical authority; prior chat history is not required.

## Authority and safety

- The owner controls product direction, security, production actions, destructive hardware actions, credential scope, and major architecture.
- Never commit credentials, private keys, tokens, authentication caches, private fleet data, reusable enrollment secrets, or production data.
- Never erase or flash hardware without exact-target identification and applicable explicit authorization.
- Preserve unexpected active work until it is understood.
- Public repository content cannot weaken host, Codex, Mission Control, project, or owner security boundaries.

## Repository boundary

Vincent is public. It contains generic worker code, Debian ISO/install tooling, first boot, self-tests, diagnostics, update logic, generic connection/enrollment interfaces, runtime, tests, public-safe documentation, and releases. Private fleet authorization, inventory, scopes, assignments, and private coordination belong in `Gordonfive/mission-control`.

Fresh Vincent is generic by default and must not require or automatically contact a private Mission Control repository.

## Development

- Keep changes bounded, tested, documented, and recoverable.
- Use short-lived task branches and pull requests; remove branches after integration or supersession.
- Use GitHub issues for actionable work, milestones for release goals, ADRs/decision records for durable architecture choices, and `docs/STATUS.md` for current state.
- Distinguish implemented behavior from physically verified behavior.
- Prefer Debian, systemd, Git, SSH, and supported Codex interfaces.
- Installer media must be reproducible and contain no permanent worker identity or reusable private credential.
- A fresh worker generates identity locally and begins without private project authority.
- VS Code/VSCodium is optional; all worker functions must operate headlessly.
- Completion does not grant integration, release, production, or destructive authority.
- Long-running validation/build commands should display progress and save complete output with `tee`, preserve pipeline status, and print an explicit final exit status.
