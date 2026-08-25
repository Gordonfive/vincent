# Worker Protocol Version 1

## Task states

`QUEUED → CLAIMING → ACTIVE → COMPLETED`

Exceptional terminal or waiting states:

- `BLOCKED`
- `WAITING_FOR_HUMAN`
- `USAGE_LIMITED`
- `FAILED`
- `CANCELLED`
- `SUPERSEDED`

Only the durable task/control-plane authority may create, cancel, supersede, or answer a decision. A worker may claim, checkpoint, block, report failure, or complete only a task it owns.

## Claiming

Git-only claiming must use a compare-and-swap equivalent against an expected remote commit/ref. A worker:

1. fetches the authoritative task state;
2. creates a claim containing worker ID, task ID, expected task revision, and nonce;
3. attempts one atomic remote ref/state update;
4. fetches and verifies the accepted owner;
5. starts Codex only if its exact claim won.

Two workers must never treat local file observation as ownership. Phase 0 leaves the exact GitHub primitive as an implementation decision to be proven in a safe test repository. A later coordinator may provide leases but may not weaken durable ownership rules.

## Publication

Before work: verify repository, remote, base, clean/known workspace, starting commit, task ownership, and schema compatibility.

Before completion: fetch, detect divergence, validate, commit, push, verify remote commit, publish report, then mark completed.

`commit succeeded; push failed` is not completion.

## Recovery

On restart, reconcile local state with remote task existence, cancellation/supersession, ownership, branch tip, and workspace evidence. Never resume solely from a local `ACTIVE` marker.

