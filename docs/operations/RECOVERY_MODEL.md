# Recovery Model

## Worker restart reconciliation

1. Start the Vincent supervisor and validate local installation identity/configuration.
2. Load crash-safe local operational state.
3. Re-establish network health and access to the operator-selected project/control source when one is configured.
4. Fetch authoritative remote task/repository state.
5. Revalidate task existence, ownership/lease state, schema, repository, worktree, branch, and untracked evidence.
6. Classify interruption and remote divergence.
7. Resume only when ownership and workspace state are deterministic; otherwise block and report.

A local `ACTIVE` marker alone never proves current task ownership.

## Failure classes

Representative classes include:

- AI-agent/provider failure;
- authentication/authorization failure;
- usage/capacity limit;
- network/DNS/TLS/repository failure;
- Git divergence or ownership conflict;
- validation failure;
- task failure;
- unknown failure.

Retries must be bounded and use backoff. Repeated or ambiguous failure becomes blocked/failed and preserves evidence.

## Checkpoints

Checkpoint coherent work before risky operations or long validation, before waiting for a decision, on detected capacity limitation, before planned shutdown, and at task completion. Avoid meaningless timer-driven commits.

Track local, committed, pushed, reviewed, integrated, and released state separately.

## Replacement recovery

A replacement worker should be reconstructable from:

- validated Vincent installer/release inputs;
- current Vincent and project/control Git repositories;
- project requirements/configuration and sanitized development fixtures;
- protected external authorization/authentication material as applicable.

No worker disk, terminal history, chat thread, or optional coordinator database may be the sole authoritative copy of project source, requirements, assignments, accepted decisions, or completion reports.
