# M1 Disposable-Host Deployment Gate

Status: READY FOR OWNER-SCHEDULED HOST PROOF

## Repository evidence

The repository-only implementation provides:

- strict protocol-v1 task models and authorized transitions;
- atomic task-specific Git ref claims;
- durable local state and deterministic startup gates;
- isolated project workspaces and stable DDEV-safe identifiers;
- noninteractive JSONL Codex boundary and classified failures;
- independent argument-vector validation;
- explicit-path, non-force checkpoint publication with remote verification;
- machine-readable and Markdown completion/blocked reports;
- durable human-decision objects;
- unique enrollment identities without embedded credentials;
- identity-gated continuous systemd service with bounded errors;
- ephemeral events/heartbeats separated from Git authority;
- canonical validation script and read-only CI workflow.

Current repository validation:

```text
Ran 91 tests
OK
wheel build: PASS
git diff --check: PASS
```

## Required owner-controlled inputs

The host proof cannot begin until these are deliberately supplied:

1. A disposable Debian 13 worker designated for the test.
2. Owner approval of the generated worker ID and Ed25519 fingerprint.
3. Narrow Git authorization for only repositories explicitly approved in the private Mission Control authorization object.
4. Supported Codex authentication for the locked service account.

No Ketchikan.net, OceanMail, BEMPIC, Rainroom, Tongass, Cloudflare, or unrelated GitHub resource is part of this proof.

## Proof sequence

1. Verify the platform checkout commit selected for installation.
2. Run the staged installer; confirm it does not enable or start the service.
3. Compare the enrollment fingerprint through a trusted owner channel.
4. Approve the worker and install revocable, per-worker Git authorization.
5. Complete supported Codex authentication as the service account.
6. Clone only `Gordonfive/vincent` into `/srv/codex/platform`.
7. Replace all example configuration values, including the generated worker ID.
8. Run `mission-control-worker ... doctor`; require every check to pass.
9. Queue one harmless task limited to a disposable example file in this repository.
10. Enable and start the systemd service.
11. Verify claim ownership, `CLAIMING`, `ACTIVE`, project branch publication, independent validation, terminal state, and report commits.
12. Reboot during a second harmless task after `ACTIVE`; verify the service refuses blind restart and preserves evidence.
13. Complete deterministic reconciliation and resume or block as specified.
14. Revoke the worker Git credential; verify access fails independently of other workers.
15. Disable the service and preserve the complete proof report in Git.

## Acceptance criteria

M1 is accepted only if:

- the installed package matches the selected Git commit;
- no permanent owner credential is present;
- the worker accesses only repositories explicitly approved in its private Mission Control authorization object;
- exactly one worker owns the exclusive task;
- Codex runs noninteractively in the prepared workspace;
- supervisor validation independently passes;
- project work and reports are pushed and remotely verified;
- reboot does not cause blind duplicate execution;
- revocation disables this worker without affecting another identity;
- no useful task state exists only on the worker.

Any failure preserves evidence and blocks M1 acceptance. It does not authorize destructive repair or access to another project.
