# Vincent and Mission Control Roadmap

This file exists so the project can be recovered from Git without relying on ChatGPT project history.

## Repository authority

| Repository | Visibility | Authority |
|---|---|---|
| `Gordonfive/vincent` | Public | Vincent worker platform, Debian ISO builder, installer, first boot, enrollment client, worker runtime, safe documentation, optional VS Code defaults, tests, releases, preserved public legacy history |
| `Gordonfive/mission-control` | Private | Fleet enrollment approval, authorization, inventory, roles, repository scopes, assignments, private coordination, private reports, preserved private control-plane state |
| `Gordonfive/codex-worker-platform` | Private legacy | Migration source only; scheduled for deletion after verified consolidation into the two new repositories |
| `Gordonfive/GitBoy` | Public legacy | Migration/provenance source only; scheduled for deletion after verified consolidation into the two new repositories |

Git is authoritative. Project DNA records why the system exists. Chat history is temporary.

## Current state — 2026-08-25

### Migration and acceptance

- Vincent initial `main` before the reset handoff was `c6c160e5c7776752370a424852a9be9f95ac7a23`.
- Complete native legacy histories have already been copied into Vincent under:
  - `legacy/codex-worker-platform/main` = `0f6e93bb8cccc26edf8887eb50641ae0fe1495a2`
  - `legacy/codex-worker-platform/checkpoint/vincent-migration-20260825` = `5521b3fc1fd273ffc71e47c344d6bb9083cfdb3f`
  - `legacy/GitBoy/main` = `191f21a30ddf94d6181cbfbee1206c3fc5029c66`
- Migration integration source accepted for Workstream 2 testing: `fc032f8df1c0abde295122a8a515e9cdcf7c7b70`.
- Durable acceptance record: `d6fb92a6a07905dc29a1431b17d2a953abd5fbc8` on `migration/integrate-worker-platform`.
- Migration verification at the accepted source passed 112 Python tests, installer parsing, credential-pattern scanning, public/private-boundary scanning, and native-history verification.

### ISO work already attempted

The accepted source was built and inspected. It produced:

- `vincent-debian-13.6.0-amd64.iso`
- SHA-256 `bcebd5fed3c82f86c7259b8dd71297e99057f630698c1742e4461265b78842a2`
- embedded platform commit `fc032f8df1c0abde295122a8a515e9cdcf7c7b70`

That image was **rejected and must never be flashed** because the active obsolete-name scan found generated package metadata exposing obsolete GitBoy command/file references. Build validation ended with `BUILD_STATUS=22`.

Corrective source:

- code correction commit: `3a6abb330fb11faffbd638b101ed11dca47f4216`
- report/branch tip: `4edd5e95a403d605664402a7b1dc2d5c4f53b71b`
- branch: `workstream/ws2-iso-corrections`
- report: `docs/reports/VINCENT_WS2_ISO_VALIDATION.md` on that branch

The correction removed tracked generated egg-info metadata, obsolete duplicate GitBoy CLI files/tests, fixed executable bits, and strengthened the ISO workflow. Non-destructive validation passed 109 Python tests, `git diff --check`, and wheel build. The corrected source has not yet been accepted as an authorized replacement ISO source.

No USB has been identified or flashed. No release has been published. No production/project authority has been granted.

## Primary Workstream A — Consolidate into the new repositories and retire legacy repositories

This is the first primary task.

1. Fetch **all** refs from `Gordonfive/vincent`, `Gordonfive/mission-control`, `Gordonfive/codex-worker-platform`, and `Gordonfive/GitBoy` before making destructive changes.
2. Inventory every branch, tag, reachable commit, report, installer/ISO artifact reference, roadmap, Project DNA document, workflow, configuration, and unresolved work item in both legacy repositories.
3. Re-verify that every useful legacy Git DAG is preserved in Vincent or Mission Control. Do not rely only on file copies; preserve history where history matters.
4. Consolidate generic/public worker implementation into Vincent. This includes installer, ISO tooling, first boot, enrollment client, runtime, tests, public-safe docs, and historical evidence.
5. Consolidate private fleet-control material into Mission Control. This includes enrollment approvals, authorization model/config, inventory, roles, repository scopes, assignments, private coordination, and private reports. Do not place raw secrets, tokens, private keys, authentication caches, or production data in Git.
6. Integrate the accepted migration implementation and the valid Workstream 2 corrections into the appropriate new default branches. Reconcile rather than blindly overwrite newer documentation.
7. Remove active product dependence on `codex-worker-platform`, `GitBoy`, `gitboy`, old bootstrap URLs, obsolete package metadata, and legacy command names except where retained as immutable historical provenance.
8. Run full tests, link/reference checks, credential/secret scans, public/private-boundary scans, obsolete-name scans, and Git-history/ref comparisons.
9. Prove that a completely fresh ChatGPT/Codex session can understand and continue the project using only `Gordonfive/vincent` and `Gordonfive/mission-control`.
10. Record a final consolidation report with exact source and destination refs and a deletion checklist.
11. **Owner directive dated 2026-08-25:** after consolidation and preservation are verified, delete `Gordonfive/codex-worker-platform` and `Gordonfive/GitBoy`. This supersedes the older roadmap dependency that delayed legacy-repository deletion until after ISO acceptance. Never delete them before the preservation proof is complete.
12. After deletion, verify that no active documentation, workflow, bootstrap path, or recovery process requires either deleted repository.

Acceptance: Vincent and Mission Control alone preserve all required code, history, intent, control-plane state, reports, and recovery instructions; legacy repositories can be removed without losing authoritative information.

## Primary Workstream B — Resume Vincent ISO creation and physical testing

This is the second primary task and may run in a separate thread, coordinated through Git.

1. Start by fetching the current Vincent branches and reading the correction branch at `workstream/ws2-iso-corrections` tip `4edd5e95a403d605664402a7b1dc2d5c4f53b71b` and code correction `3a6abb330fb11faffbd638b101ed11dca47f4216`.
2. Do not use the rejected ISO or treat `fc032f8...` as a sufficient build source after the discovered defect.
3. Establish one exact authorized replacement source commit after reviewing the correction and any consolidation commits that supersede it.
4. Build `vincent-debian-13.6.0-amd64.iso` from that exact source. Long-running commands must display progress and save complete timestamped output with `tee`, preserve pipeline exit status, and print an explicit final status.
5. Run the full repository tests, source ISO signature/checksum verification, image inspection, manifest/checksum verification, embedded commit verification, secret/credential scan, identity-file scan, and active obsolete-name scan.
6. Confirm the ISO contains no permanent worker identity, private key, personal credential, reusable enrollment secret, production credential, fleet-wide credential, or private fleet configuration.
7. Do not flash until the exact removable target is identified by model, serial, transport, removability, and `/dev/disk/by-id`, and destructive authorization applies to that exact device.
8. Fresh-install a disposable workstation using whole-disk guided LVM and one root filesystem.
9. Verify stable `vincent-worker-NNNNNN` hostname, persistent networking, local login, SSH, Git, GitHub CLI, Docker, DDEV, Codex, Vincent, and Python packaging tools.
10. On the headless console, routine operation should require only the `vincent` command. Diagnostics/repair should be automated or performed remotely over SSH rather than hand-editing the installed machine into compliance.
11. Verify fresh local identity/request generation, no authority before approval, explicit scoped enrollment, revocation, and clean recovery.
12. Execute one harmless real bounded task with atomic claim, isolated work, independent validation, commit, push, and non-secret report.
13. Repeat a clean install to prove reproducibility and publish the physical-test report.

Acceptance: two reproducible fresh installs reach READY and one scoped harmless task completes without embedded secrets or hand-entered repair steps.

## Worker operating-system identity architecture

Vincent workers are appliances, not conventional multi-user workstations. Installation must not require the owner to invent a normal username or password merely to satisfy the Debian installer.

- Create a dedicated local `vincent` Unix service account automatically. Do not run Vincent as `nobody` and do not use a normal human account as the automation identity.
- The `vincent` account owns Vincent runtime state, work directories, repositories, and other files that require persistent ownership. Vincent services run under this identity.
- The `vincent` account is non-human and should not permit normal password login. It receives only the groups, filesystem permissions, capabilities, and privileged operations actually required.
- Do not grant `vincent` unrestricted sudo. Privileged operations should use narrowly scoped root-owned helpers or systemd units with explicit interfaces and validation.
- Root remains reserved for installer/bootstrap and tightly controlled system operations. Normal remote root login should be disabled.
- A conventional human administrative account is optional rather than an installation requirement. If enabled for physical recovery or interactive CLI troubleshooting, it remains separate from the Vincent automation identity and follows an explicit authentication policy.
- The preferred default installation is therefore: **no required human login account, an automatically created locked `vincent` service account, and deliberately provisioned recovery/admin access when needed.**
- Interactive Vincent/Codex troubleshooting must not require weakening the service account or permanently granting broad privileges. Recovery mechanisms should preserve least privilege and auditable separation between automated and human actions.

Acceptance: an unattended fresh installation reaches operational state without prompting for a human username/password; Vincent runs under its dedicated least-privileged identity; `nobody` is not used as the Vincent runtime identity; and administrative recovery remains possible through a separately controlled mechanism.

## Product milestones

| Milestone | Outcome | Status |
|---|---|---|
| M0 | Architecture and Project DNA accepted | Complete |
| M1 | One disposable Vincent worker completes a bounded task | In progress |
| M2 | Worker recovery proven | Not started |
| M3 | Universal installer proven | Prototype / in progress |
| M4 | Two-worker coordination proven | Not started |
| M5 | Phone-first control proven | Not started |
| M6 | Mission Control proven | Not started |
| M7 | Multi-project operation proven | Not started |
| M8 | Full operation recovery proven | Not started |

## Permanent principles

- Git is the durable technical authority.
- Project DNA is canonical intent.
- ChatGPT selects priorities and workers; Mission Control dispatches and records; workers do not invent product direction.
- Human judgment remains authoritative for destructive hardware actions, production actions, credential scope, major architecture, and Project DNA changes.
- Workers are replaceable and least-privileged.
- Public Vincent content must never expose private fleet state or secrets.
- No chat thread is authoritative merely because it is newer; durable Git evidence and explicit owner decisions control.
