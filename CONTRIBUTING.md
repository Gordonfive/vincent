# Contributing to Vincent

## Before starting

Read `AGENTS.md`, `docs/README.md`, `docs/STATUS.md`, and the documentation relevant to the change. Inspect open issues, pull requests, and active branches to avoid duplicating or overwriting current work.

## Work tracking

- Use a GitHub issue for non-trivial defects, features, refactors, or documentation work.
- Use milestones for release-level goals.
- Keep roadmap entries at outcome/milestone level rather than using the roadmap as a task list.
- Record consequential architecture or security choices as ADRs/decision records.

## Branches and pull requests

- Branch from the current intended base using a short descriptive name such as `fix/...`, `feature/...`, or `docs/...`.
- Keep one logical change per pull request when practical.
- Reconcile unexpected remote work rather than resetting or overwriting it.
- Delete temporary branches after merge or supersession.
- Do not infer release, production, credential, or destructive authority from pull-request approval.

## Validation

Run the repository's validation entry point before requesting review:

```text
sh scripts/validate.sh
```

For long-running commands, display progress and save complete timestamped output with `tee`; preserve pipeline exit status and print an explicit final status.

Installer, ISO, release, security, or protocol changes require the additional task-specific validation documented under `docs/operations/`, `docs/security/`, or `docs/protocols/`.

## Documentation

Update documentation in the same pull request when behavior, interfaces, installation, configuration, security boundaries, release acceptance, or operator procedures change.

Do not create permanent handoff documents for routine task state. Use issues and pull requests for active work and `docs/STATUS.md` only for concise cross-cutting project state.

## Security

Do not commit passwords, tokens, private keys, authentication caches, reusable enrollment credentials, production data, or private fleet state. See `SECURITY.md`.
