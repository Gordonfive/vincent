# Vincent and Mission Control Roadmap

Git records what exists. Project DNA records why. This roadmap records the intended order and acceptance gates.

## Repository boundaries

| Repository | Visibility | Authority |
|---|---|---|
| `Gordonfive/vincent` | Public | Worker platform, Debian ISO, installer, first boot, enrollment client, runtime, safe documentation, optional VS Code defaults, tests, releases |
| `Gordonfive/mission-control` | Private | Fleet enrollment approval, authorization, inventory, roles, repository scopes, assignments, private reports |
| `Gordonfive/codex-worker-platform` | Private legacy | Preserved implementation and ISO-development history; migration source |
| `Gordonfive/GitBoy` | Public legacy | Temporarily preserved history and old links; never credentials |

## Current evidence

- M0 architecture accepted at `8ed265b05cb9549f2deed43ed8a4612150a496fe`.
- Legacy implementation includes protocol, claiming, recovery, isolation, validation, publication, enrollment, supervisor, installer, ISO, health, logging, reporting, and tests.
- Physical testing proved UEFI, full-disk LVM, one root filesystem, stable six-digit hostname, persistent Ethernet, and automated first-boot console execution.
- Workstream 2 physical testing changed the account model: Vincent is an appliance with no human local login account and no owner-chosen username/password. Root is locked before first boot. Runtime work uses the locked `mission-control` system account. See `decisions/ADR-0002-APPLIANCE-ACCOUNTS-AND-CONSOLE.md`.
- First-boot tests found and fixed Python `setuptools.build_meta` isolation, Codex installer/global-executable permission, DNS/network-readiness, and service-account HOME/XDG environment defects.
- The first-boot dashboard now exposes fixed critical state plus live work output; tty2 provides an optional non-root interactive Codex console after Codex installation.
- Last legacy image: embedded commit `8a06965f610ceb6a4a7becfdfaae0ce528a7394e`; SHA-256 `485f45a0af366ba86c2daaace0a28edaef368356a1bb52b9b19befc7a6685725`; 108 tests and image inspection passed. It was not flashed after the Vincent split.
- Workstream 1 implementation and complete native legacy histories are present in Vincent. The integrated tree passes 112 tests and its public/private and credential scans.

## Workstream 1 — Repository migration

This workstream must finish before ISO work resumes.

1. Preserve every useful legacy change on a non-destructive checkpoint branch and push it without force.
2. Record source branch, commit, status, legacy ISO path/hash, validation, known failures, and physical-test results.
3. Add Vincent as a separate remote and push legacy history to `migration/codex-worker-platform`; never overwrite Vincent `main`.
4. Create an integration branch from Vincent `main`, preserve both histories, and reconcile overlapping README, AGENTS, Project DNA, security, architecture, and migration documents deliberately.
5. Keep generic public worker code in Vincent. Keep fleet inventory, policy, assignments, scopes, credentials, private infrastructure, and private reports in Mission Control.
6. Rename product surfaces to `Vincent`, command `vincent`, hostname `vincent-worker-<stable six digits>`, and `vincent-*` artifacts.
7. Search for `GitBoy`, `gitboy`, obsolete repository URLs, private details, and secrets. Document every compatibility identifier that remains.
8. Push the integrated migration branch and verification report with exact commits. Stop before merging Vincent `main`, publishing a release, or deleting legacy repositories.

Status: **Complete pending the final explicit owner acceptance record.** Native histories, integrated implementation, verification report, public/private boundaries, and remaining compatibility identifiers are pushed. Vincent `main` remains untouched.

Acceptance: the owner explicitly accepts one exact commit after the continuation and full roadmap are present on the integration branch.

## Workstream 2 — Vincent ISO and physical testing

Start only from the exact accepted Vincent migration commit supplied by Workstream 1.

1. Build `vincent-debian-13.6.0-amd64.iso` from Vincent, showing progress and saving timestamped output with `tee` and a final exit status.
2. Run all tests, image inspection, manifest/checksum verification, secret scan, and obsolete-name scan.
3. Confirm no permanent worker identity, private key, personal credential, reusable enrollment secret, production credential, or fleet-wide credential is embedded.
4. Identify the flash target immediately before writing. During current local ISO iteration the owner may use `/dev/sda` for swappable USB media only when an automatic guard confirms it is a whole removable USB disk and has no mounted filesystems.
5. Fresh-install a disposable workstation using manual physical-disk selection and final destructive confirmation, with guided whole-disk LVM, `vincent-vg`, and the atomic all-files-in-one-filesystem recipe selected automatically.
6. Do not create a human local account or request an owner username/password. Lock root before first boot. Verify no human UID-range login accounts exist and root remains locked.
7. Verify stable `vincent-worker-NNNNNN` hostname and networking after reboot. First boot must wait/retry for route, DNS, HTTPS, and exact-commit Git fetch rather than permanently failing on transient network readiness.
8. Fetch the exact ISO-pinned Vincent commit from the public `Gordonfive/vincent` Git repository as the normal runtime source. Keep the embedded platform archive only as recovery/evidence material.
9. Run unattended self-tests for SSH, Git, GitHub CLI, Docker, DDEV, Codex, Vincent, Python packaging, account state, identity, Git commit/remote, embedded recovery payload, secrets, and pre-enrollment authority.
10. tty1 must remain a persistent self-testing/status dashboard with fixed critical information, current task/last error, test results, and live scrolling work output suitable for photographic evidence. No local login or hand-entered diagnostic commands are part of acceptance.
11. tty2 may provide an optional interactive Codex console after Codex is installed. It runs as the locked `mission-control` service account with an explicit user environment; it is not a root shell or general Linux login.
12. Verify unique local identity/request generation, explicit scoped enrollment, revocation, and absence of authority before approval.
13. Execute one harmless real task: atomic claim, isolated work, independent validation, commit, push, and non-secret report.
14. Repeat a clean install to prove reproducibility and publish the test report for owner acceptance.

Acceptance: two reproducible fresh installs reach READY and one scoped harmless task completes without hand-entered repair commands, human local login credentials, or embedded secrets.

## Product milestones

| Milestone | Outcome | Status | Gate |
|---|---|---|---|
| M0 | Architecture and Project DNA accepted | Complete | Accepted architecture commit |
| M1 | One disposable Vincent worker completes a bounded task | In progress | Fresh install, enrollment, task, validation, push, report |
| M2 | Worker recovery proven | Not started | Failure injection and replacement recovery |
| M3 | Universal installer proven | Prototype | Repeated heterogeneous installs reach READY |
| M4 | Two-worker coordination proven | Not started | Exclusive claims and conflict handling |
| M5 | Phone-first control proven | Not started | Owner directs and accepts without SSH |
| M6 | Mission Control proven | Not started | Replaceable private control plane |
| M7 | Multi-project operation proven | Not started | Isolated project policies and scopes |
| M8 | Full operation recovery proven | Not started | Recover fleet, coordinator, and work from durable state |

## Permanent principles

- Git is authoritative; chat is temporary.
- Project DNA is canonical intent.
- ChatGPT selects priorities and workers; Mission Control dispatches; workers do not invent product direction.
- Human approval remains required for destructive actions, production, new credential scope, major architecture, and Project DNA changes.
- Workers are replaceable and least-privileged.
- Vincent workers are appliances: no human local login account is required for normal operation.
- Legacy repositories remain preserved until separately authorized for archival or deletion.
