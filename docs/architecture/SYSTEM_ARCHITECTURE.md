# System Architecture

## Layers

1. **Durable Git authority:** Vincent source/releases plus the operator-selected project/control repository containing project requirements, assignments, reports, tests, and provenance.
2. **Worker supervisor:** systemd-managed Vincent runtime that reconciles durable task state, prepares isolated workspaces, invokes the configured AI agent, validates results, publishes, reports, and maintains local health.
3. **Execution environment:** task-specific Git worktree and project-local or containerized tooling constrained by the active project profile.
4. **AI agent provider:** initially Codex; invoked through a supported automation interface rather than terminal keystroke injection.
5. **Optional coordinator/control plane:** Mission Control or another future coordinating service may add enrollment, inventory, heartbeats, leases, dispatch, and fleet health when those capabilities are required. Its loss must not erase durable project work or intent.

## Codex interface

The initial provider target is `codex exec` because it supports scripted noninteractive execution. Vincent must validate actual installed-version behavior, exit codes, event output, session identifiers, failure signals, and usage-limit behavior before depending on automatic recovery/resumption.

Agent-specific behavior should remain behind a provider boundary so future supported agents do not require redesigning Vincent's generic lifecycle.

## Durable versus ephemeral

| State | Authority |
|---|---|
| Vincent releases, project requirements, task definition, owner decision, completion report, source history | Git |
| Workspace changes not yet pushed | Local and at risk |
| Process IDs, resource samples, transient link state, short-lived liveness/lease data | Local or optional coordinator |
| Worker private key and agent authentication | Protected worker secret storage |
| Platform/project configuration | Git or local protected configuration, excluding secret values |

## Replacement property

Loss of a worker should cost only reconstructable cache, local logs, worker-specific credentials, and at most bounded unpushed progress. Loss of an optional coordinator must not lose project source, assignments, reports, accepted decisions, or intent.
