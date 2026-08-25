# Recovery Model

## Reboot reconciliation

1. systemd starts supervisor.
2. Validate worker identity and configuration.
3. Load atomic local operational state.
4. Fetch authoritative remote state.
5. Revalidate task ownership and schema.
6. Inspect repository, worktree, branch, and untracked evidence.
7. Classify interruption and remote divergence.
8. Resume only when deterministic; otherwise block and report.

## Failure classes

- `TRANSIENT_CODEX_FAILURE`
- `AUTHENTICATION_FAILURE`
- `USAGE_LIMIT`
- `NETWORK_FAILURE`
- `GIT_DIVERGENCE`
- `VALIDATION_FAILURE`
- `TASK_FAILURE`
- `UNKNOWN_FAILURE`

Retries are bounded and back off. Repeated unknown failure becomes blocked or failed.

## Checkpoints

Checkpoint after coherent milestones, before risky operations or long tests, before waiting for a decision, at detected usage limitation, before planned shutdown, and at completion. Avoid timer-driven meaningless commits.

Track separately: local, committed, pushed, reviewed, and integrated progress.

## Fleet recovery

Blank machines plus reproducible installer inputs, enrollment authority, platform/project Git repositories, Project DNA, project manifests, and sanitized fixtures must reconstruct the development operation. No worker disk, terminal history, or ChatGPT history is authoritative.

