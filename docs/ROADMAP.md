# Vincent and Mission Control Roadmap

**Roadmap updated:** 2026-08-26T13:22:00-08:00

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
| `Gordonfive/vincent` | Public generic Vincent worker platform: installer, ISO tooling, first boot, self-checks, update logic, connection/enrollment client, worker runtime, public-safe documentation, tests, releases, and preserved public legacy history. |
| `Gordonfive/mission-control` | Private project/control repository for our deployment. It may supply Vincent assignments, project profiles, reports, coordination state, and later server-side control-plane implementation, but a fresh Vincent worker must not depend on or know this repository by default. |

Legacy repositories are migration/provenance sources only and are to be retired after verified consolidation. Exact migration refs and evidence belong in migration reports and continuation documentation rather than this roadmap.

## Primary Workstream A — Complete consolidation and retire legacy repositories

1. Inventory and preserve every required legacy branch, tag, reachable commit, report, installer/ISO artifact reference, Project DNA document, workflow, configuration, and unresolved work item.
2. Re-verify that useful legacy Git history is preserved in Vincent or Mission Control; do not rely only on file copies where history matters.
3. Consolidate generic/public worker implementation into Vincent and private project/control material into Mission Control.
4. Integrate accepted migration implementation and valid ISO corrections into the appropriate new default branches, reconciling rather than overwriting newer documentation.
5. Remove active product dependence on legacy repository names, bootstrap URLs, package metadata, and command names except immutable historical provenance.
6. Remove any generic Vincent assumption that `Gordonfive/mission-control` or another project-specific private repository is automatically contacted after installation.
7. Run full tests, link/reference checks, credential/secret scans, public/private-boundary scans, obsolete-name scans, and Git-history/ref comparisons.
8. Prove that a fresh ChatGPT/Codex session can understand and continue the project using only Vincent and Mission Control.
9. Record final consolidation evidence with exact source/destination refs and a deletion checklist.
10. After preservation is proven, delete the legacy `codex-worker-platform` and `GitBoy` repositories as previously directed by the owner.
11. Verify after deletion that no active documentation, workflow, bootstrap path, or recovery process requires either legacy repository.

**Acceptance:** Vincent and Mission Control alone preserve all required code, history, intent, control-plane state, reports, and recovery instructions, while the Vincent product remains generic and usable without Mission Control.

## Primary Workstream B — Complete Vincent ISO creation and physical testing

This workstream may proceed separately but remains coordinated through Git.

1. Before every build, compare the agent's last-known decision timestamp with `docs/DECISIONS.md`. Ingest all newer authoritative decisions before proceeding. If no trustworthy decision checkpoint exists, read the full current decision set once and establish one.
2. Refresh this roadmap only when its `Roadmap updated` timestamp is newer than the agent's recorded roadmap checkpoint.
3. Establish one exact authorized ISO source commit containing all accepted migration and corrective work.
4. Assign a unique monotonically increasing Vincent ISO build number before image creation, as required by `VINCENT-DEC-004`.
5. Build the Vincent Debian ISO from that exact source. The ISO filename and supported ISO/volume metadata must include the build number. Long-running commands must display progress and save complete timestamped output with `tee`, preserve pipeline exit status, and print an explicit final status.
6. Run full repository tests, source ISO signature/checksum verification, image inspection, manifest/checksum verification, embedded-commit verification, secret/credential scanning, identity-file scanning, active obsolete-name scanning, and build-number consistency validation.
7. Confirm the ISO contains no permanent worker identity, private key, personal credential, reusable enrollment secret, production credential, fleet-wide credential, private fleet configuration, or built-in project-specific private repository credential/URL.
8. Before flashing, apply the project's exact-device destructive-authorization gate.
9. When an ISO is written to USB media, ensure the USB's durable machine-readable label/identity exposes the same build number as the source image. Record that build number in flashing logs and physical-test evidence.
10. Fresh-install a disposable workstation. Disk partitioning must be chosen interactively through the normal Debian installer workflow as required by `VINCENT-DEC-003`; Vincent must not force guided partitioning, LVM, whole-disk use, or a fixed partition recipe.
11. Verify stable Vincent hostname, networking, generic runtime tooling, Vincent self-checks, diagnostics, status display, update checking, and management access without requiring any Mission Control connection.
12. Verify the accepted worker Unix identity architecture from `VINCENT-DEC-001`: no required human installer account, dedicated least-privileged `vincent` service identity, no use of `nobody` as the Vincent runtime identity, and separately controlled recovery/admin access.
13. Verify the worker status screen visibly displays the installed build number from durable local build metadata, as required by `VINCENT-DEC-005`, and that it matches the source image/build records.
14. Verify the V1 connection workflow from `VINCENT-DEC-006`: the unassigned worker accepts an operator-supplied Git repository URL, supports an interactive/private-repository authentication flow without baked credentials, and records the connected control source locally.
15. Define and validate a minimal Git control contract containing at least a project/dependency profile, an assignment input, and a report/output location. Project-specific dependencies must be installed after connection rather than assumed to belong in the generic image.
16. Execute one harmless real bounded task obtained from the connected Git repository, with atomic claim or equivalent safe assignment ownership, isolated work, independent validation, commit/push or other defined report publication, and non-secret result evidence.
17. Repeat a clean installation to prove reproducibility and publish the physical-test report.

**Acceptance:** two reproducible fresh installs reach an unassigned READY state without Mission Control or embedded private configuration. A worker can then connect to an operator-selected private Git repository, authenticate interactively, acquire its project profile and assignment, install required project-specific tooling, execute one scoped harmless task, and publish its report. Partition layout remains operator-selected. Every tested image and USB medium is traceable to one build number, and build-number identifiers agree across the image, media, installed worker status screen, manifest/checksums, logs, and reports.

## Product milestones

| Milestone | Outcome | Status |
|---|---|---|
| M0 | Architecture and Project DNA accepted | Complete |
| M1 | One generic Vincent worker reaches unassigned READY and completes one Git-assigned bounded task | In progress |
| M2 | Worker recovery proven | Not started |
| M3 | Universal installer proven | Prototype / in progress |
| M4 | Two-worker Git coordination proven | Not started |
| M5 | Phone-first control proven | Not started |
| M6 | Dedicated Mission Control service/backend evaluated or proven | Deferred / not started |
| M7 | Multi-project operation proven | Not started |
| M8 | Full operation recovery proven | Not started |

## Permanent roadmap constraints

- Git is the durable technical authority.
- Project DNA is canonical intent.
- Human judgment remains authoritative for destructive hardware actions, production actions, credential scope, major architecture, and Project DNA changes.
- Workers are replaceable and least-privileged.
- Vincent is generic by default; project-specific private control sources are operator-selected after installation.
- Public Vincent content must never expose private project/fleet state or secrets.
- Durable Git evidence and explicit owner decisions control; chat recency alone does not establish authority.
