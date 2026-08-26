# Vincent and Mission Control Roadmap

**Roadmap updated:** 2026-08-26T08:10:43-08:00

This roadmap describes the work that remains and the milestones used to judge progress. It intentionally does not duplicate detailed architecture decisions, historical validation evidence, or continuation instructions.

Agents should retain the newest roadmap timestamp they have incorporated. If `Roadmap updated` is newer than the agent's recorded roadmap checkpoint, refresh this document before continuing roadmap-directed work. If it is not newer, re-reading the roadmap is unnecessary.

Authoritative supporting documents:

- `docs/PROJECT_START_HERE.md` — entry point and current authoritative references.
- `docs/DECISIONS.md` and `docs/decisions/` — accepted/superseded design decisions and owner acceptances.
- `docs/ARCHITECTURE.md` and `docs/architecture/` — resulting system architecture.
- `docs/reports/` — build, migration, validation, and test evidence.
- `docs/CONTINUATION_HANDOFF.md` — operational continuation state.
- `docs/project-dna/` — canonical product intent.

Git is authoritative. Project DNA records why the system exists. Chat history is temporary.

## Repository roles

| Repository | Role |
|---|---|
| `Gordonfive/vincent` | Public Vincent worker platform: installer, ISO tooling, first boot, enrollment client, runtime, public-safe documentation, tests, releases, and preserved public legacy history. |
| `Gordonfive/mission-control` | Private fleet control plane: enrollment approval, authorization, inventory, roles, repository scopes, assignments, private coordination/reports, and private control-plane state. |

Legacy repositories are migration/provenance sources only and are to be retired after verified consolidation. Exact migration refs and evidence belong in migration reports and continuation documentation rather than this roadmap.

## Primary Workstream A — Complete consolidation and retire legacy repositories

1. Inventory and preserve every required legacy branch, tag, reachable commit, report, installer/ISO artifact reference, Project DNA document, workflow, configuration, and unresolved work item.
2. Re-verify that useful legacy Git history is preserved in Vincent or Mission Control; do not rely only on file copies where history matters.
3. Consolidate generic/public worker implementation into Vincent and private fleet-control material into Mission Control.
4. Integrate accepted migration implementation and valid ISO corrections into the appropriate new default branches, reconciling rather than overwriting newer documentation.
5. Remove active product dependence on legacy repository names, bootstrap URLs, package metadata, and command names except immutable historical provenance.
6. Run full tests, link/reference checks, credential/secret scans, public/private-boundary scans, obsolete-name scans, and Git-history/ref comparisons.
7. Prove that a fresh ChatGPT/Codex session can understand and continue the project using only Vincent and Mission Control.
8. Record final consolidation evidence with exact source/destination refs and a deletion checklist.
9. After preservation is proven, delete the legacy `codex-worker-platform` and `GitBoy` repositories as previously directed by the owner.
10. Verify after deletion that no active documentation, workflow, bootstrap path, or recovery process requires either legacy repository.

**Acceptance:** Vincent and Mission Control alone preserve all required code, history, intent, control-plane state, reports, and recovery instructions.

## Primary Workstream B — Complete Vincent ISO creation and physical testing

This workstream may proceed separately but remains coordinated through Git.

1. Before every build, compare the agent's last-known decision timestamp with `docs/DECISIONS.md`. Ingest all newer authoritative decisions before proceeding. If no trustworthy decision checkpoint exists, read the full current decision set once and establish one.
2. Refresh this roadmap only when its `Roadmap updated` timestamp is newer than the agent's recorded roadmap checkpoint.
3. Establish one exact authorized ISO source commit containing all accepted migration and corrective work.
4. Build the Vincent Debian ISO from that exact source. Long-running commands must display progress and save complete timestamped output with `tee`, preserve pipeline exit status, and print an explicit final status.
5. Run full repository tests, source ISO signature/checksum verification, image inspection, manifest/checksum verification, embedded-commit verification, secret/credential scanning, identity-file scanning, and active obsolete-name scanning.
6. Confirm the ISO contains no permanent worker identity, private key, personal credential, reusable enrollment secret, production credential, fleet-wide credential, or private fleet configuration.
7. Before flashing, apply the project's exact-device destructive-authorization gate.
8. Fresh-install a disposable workstation using the intended whole-disk installation layout.
9. Verify stable Vincent hostname, networking, required development/runtime tooling, Vincent runtime, and management access.
10. Verify the accepted worker Unix identity architecture from `VINCENT-DEC-001`: no required human installer account, dedicated least-privileged `vincent` service identity, no use of `nobody` as the Vincent runtime identity, and separately controlled recovery/admin access.
11. Verify fresh local identity/request generation, no authority before approval, explicit scoped enrollment, revocation, and clean recovery.
12. Execute one harmless real bounded task with atomic claim, isolated work, independent validation, commit, push, and non-secret report.
13. Repeat a clean installation to prove reproducibility and publish the physical-test report.

**Acceptance:** two reproducible fresh installs reach READY and one scoped harmless task completes without embedded secrets or hand-entered repair steps.

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

## Permanent roadmap constraints

- Git is the durable technical authority.
- Project DNA is canonical intent.
- Human judgment remains authoritative for destructive hardware actions, production actions, credential scope, major architecture, and Project DNA changes.
- Workers are replaceable and least-privileged.
- Public Vincent content must never expose private fleet state or secrets.
- Durable Git evidence and explicit owner decisions control; chat recency alone does not establish authority.
