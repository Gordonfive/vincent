# System Architecture

## Layers

1. **Durable control plane:** Git repositories containing Project DNA, project manifests, tasks, decisions, reports, reviews, and integration records.
2. **Operational coordinator:** replaceable service for registry, heartbeats, leases, dispatch, events, and stale-state detection.
3. **Worker supervisor:** systemd-managed local state machine that reconciles durable tasks, prepares isolated workspaces, invokes Codex, validates independently, publishes, and reports.
4. **Execution environment:** task-specific Git worktree and project-local/containerized tooling.
5. **Codex:** invoked through a supported noninteractive interface; not used for deterministic local steps that the supervisor can perform directly.

## Codex interface decision

The initial supervisor target is `codex exec`, because current official documentation marks it stable for scripted noninteractive runs, supports JSONL event output, and supports resuming a saved exec session. Phase 1 must verify actual installed-version behavior, exit codes, session IDs, failure events, and usage-limit signals before relying on automatic resumption.

The experimental app server may be evaluated later; it is not the Phase 1 dependency. Terminal keystroke injection is rejected.

## Durable versus ephemeral

| State | Authority |
|---|---|
| Project DNA, task definition, owner decision, completion report, source history | Git |
| Workspace changes not yet pushed | Local and at risk |
| Worker heartbeat, process ID, resource samples, short lease | Coordinator/local ephemeral state |
| Worker private key and Codex auth | Worker secret storage |
| Platform and project configuration | Git, excluding secret values |

## Replacement property

Loss of a worker must cost only reconstructable cache, local logs, worker-specific credentials, and at most bounded unpushed progress. Loss of the coordinator must not lose tasks, reports, decisions, or intent.

