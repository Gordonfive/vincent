# Vincent and Mission Control Roadmap

**Roadmap updated:** 2026-08-26T13:30:00-08:00

This roadmap describes remaining work and milestones. Detailed decisions are in `docs/DECISIONS.md`; historical validation evidence belongs in `docs/reports/`; continuation state belongs in `docs/CONTINUATION_HANDOFF.md`.

Agents retain the newest roadmap and decision timestamps incorporated and refresh only when those authoritative timestamps advance.

## Repository roles

| Repository | Role |
|---|---|
| `Gordonfive/vincent` | Public generic Vincent worker platform and trusted upstream source for Vincent software/releases: installer, ISO tooling, first boot, self-checks, update logic, connection client, runtime, public documentation, tests, and releases. |
| `Gordonfive/mission-control` | Private project/control repository for our deployment. It may supply assignments, project profiles, reports, and coordination state, but fresh Vincent does not know or require it by default. |

## Primary Workstream A — Complete consolidation and retire legacy repositories

1. Preserve required legacy Git history, reports, intent, configuration, and unresolved work in Vincent or Mission Control.
2. Consolidate generic/public implementation into Vincent and private project/control material into Mission Control.
3. Remove active dependence on legacy repository names, bootstrap paths, obsolete package metadata, and legacy command names.
4. Remove generic Vincent assumptions that a project-specific private repository is automatically contacted after installation.
5. Run tests, link/reference checks, secret scans, public/private-boundary scans, obsolete-name scans, and Git-history comparisons.
6. Prove a fresh agent can continue using only Vincent and Mission Control.
7. Record final consolidation/deletion evidence, then retire the legacy repositories as previously directed.

**Acceptance:** Vincent and Mission Control preserve required project authority while Vincent remains generic and usable without Mission Control.

## Primary Workstream B — Vincent 1.0 installer and worker proof

1. Refresh newer decisions/roadmap state before every build.
2. Establish one exact authorized ISO source commit.
3. Assign the next unique monotonically increasing ISO build number.
4. Build and validate the ISO with matching build identity across image, USB, manifests, checksums, logs, reports, and installed status metadata.
5. Preserve normal interactive Debian disk partitioning; Vincent does not force a storage layout.
6. Fresh-install a disposable workstation and prove generic unassigned READY operation: networking, stable identity, self-checks, diagnostics, status, and management access.
7. Prove the dedicated least-privileged `vincent` service identity and separately controlled privileged/recovery interfaces.
8. Prove the status screen displays the original installed ISO build number.
9. Prove Debian/system maintenance and representative development-tool maintenance without reimaging.
10. Implement `VINCENT-DEC-008` in V1 if it does not materially delay the core proof: periodically check the trusted public Vincent upstream and safely update Vincent software in place. At minimum, V1 should prove update discovery and a safe in-place Vincent application update path. If this cannot be completed safely without materially delaying V1, it becomes a required V1.1 gate rather than being implemented unsafely.
11. Prove the V1 operator-selected Git connection workflow: repository URL entry, interactive authentication, local connection state, project/dependency profile, assignment input, and report/output location.
12. Prove project profiles can constrain dependency versions and that Vincent respects those constraints during installation and maintenance.
13. Execute one harmless bounded Git-assigned task with safe ownership/claiming, isolated work, validation, and report publication.
14. Repeat a clean installation and publish physical-test evidence.

**V1 acceptance:** two reproducible fresh installs reach unassigned READY without private Mission Control configuration; one worker connects to an operator-selected private Git repository, prepares its constrained task environment, completes one bounded assignment, and publishes its report. Debian/toolchain maintenance works without reimaging. Vincent self-update is included if safely achievable within V1 scope; otherwise it is explicitly carried as the first required V1.1 lifecycle feature.

## Version 1.1 lifecycle work

The following work belongs in V1.1 unless completed safely during V1:

1. Complete/strengthen periodic public-upstream Vincent self-update from `Gordonfive/vincent` if the full mechanism was deferred from V1.
2. Add robust rollback/recovery for failed Vincent application updates beyond the minimum V1 safety mechanism.
3. Define update channels/policies such as stable versus testing, staged/canary adoption, maintenance windows, and automatic versus operator-approved activation.
4. Improve update reporting so status clearly distinguishes original ISO build identity, current Vincent software version/release, Debian maintenance state, and project-tool version constraints.
5. Ensure routine Vincent application upgrades never require a new ISO except when an underlying installer/base-image change genuinely requires reinstallation.

## Later milestones

| Milestone | Outcome | Status |
|---|---|---|
| M0 | Architecture and Project DNA accepted | Complete |
| M1 | Generic worker reaches unassigned READY and completes one Git-assigned bounded task | In progress |
| M2 | Worker recovery proven | Not started |
| M3 | Universal installer proven | Prototype / in progress |
| M4 | Two-worker Git coordination proven | Not started |
| M5 | Phone-first control proven | Not started |
| M6 | Dedicated Mission Control service/backend evaluated or proven | Deferred |
| M7 | Multi-project operation proven | Not started |
| M8 | Full operation recovery proven | Not started |

## Permanent roadmap constraints

- Git is the durable technical authority; Project DNA is canonical intent.
- Human judgment controls destructive hardware actions, production actions, credential scope, major architecture, and Project DNA changes.
- Workers are replaceable and least-privileged.
- Vincent is generic by default; private project/control sources are operator-selected after installation.
- Vincent maintains Debian, its own software, runtime dependencies, and development toolchain while honoring active project version constraints.
- The public Vincent upstream is the authoritative source for Vincent software updates; a fresh ISO is not the normal application-update mechanism.
- Public Vincent content never exposes private project/fleet state or secrets.
