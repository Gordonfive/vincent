# M1 Protocol Core Checkpoint

Date: 2026-08-24  
Status: PASS

## Scope

This checkpoint implements the first executable M1 substrate without provisioning or modifying a workstation:

- versioned task models and strict parsing;
- authorized task-state transitions;
- atomic create-if-absent claim-store contract;
- deterministic single-task supervisor core;
- mock executor boundary;
- concurrent ownership and losing-worker safety tests;
- create-only Git remote claim adapter and two-clone race proof;
- crash-safe local operational state and restart reconciliation;
- workspace contamination checks and stable DDEV-safe identifiers;
- supervisor-owned validation and completion report schemas;
- classified `codex exec --json` process boundary with bounded retry policy.

The in-memory claim store remains the supervisor test double. The Git adapter implements the same contract with a create-only, force-with-lease ref push. Its race behavior is proven against a local bare remote; a hosted-private-repository proof remains required before parallel physical workers are enabled.

## Validation evidence

Command:

```text
PYTHONPATH=worker python3 -m unittest discover -s tests -q
```

Result:

```text
Ran 91 tests
OK
```

Repository hygiene was independently checked with `git diff --check` and passed.

The in-memory concurrency test launches 32 simultaneous claim attempts for one task and requires exactly one winner. A separate test races two independent clones against one bare Git remote. Supervisor tests establish that a losing worker never invokes the executor and that executor failure yields the protocol's `FAILED` state.

This environment does not contain a Codex CLI executable. Command construction, JSONL parsing, failure classification, and retry policy are unit tested, but actual installed-version behavior and authentication remain deployment gates.

## Safety boundary

No other repository was accessed. No external workstation was provisioned, erased, or modified. No production credential or secret was stored in the repository.

## Next checkpoint

Run the controlled disposable-host gate in `docs/operations/M1_DEPLOYMENT_GATE.md`. This requires owner-controlled enrollment approval, per-worker Git authorization, and supported Codex authentication.
