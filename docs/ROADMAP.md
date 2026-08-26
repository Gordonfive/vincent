# Vincent and Mission Control Roadmap

**Roadmap updated:** 2026-08-26T13:40:00-08:00

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
3. Assign the next unique monotonically increasing **installer build number**.
4. Build and validate the ISO with matching installer-build identity across ISO filename/metadata, USB label, installer manifests/checksums, logs, reports, and durable installation provenance.
5. Preserve normal interactive Debian disk partitioning; Vincent does not force a storage layout.
6. Fresh-install a disposable workstation and prove generic unassigned READY operation: networking, stable identity, self-checks, diagnostics, status, and management access.
7. Prove the dedicated least-privileged `vincent` service identity and separately controlled privileged/recovery interfaces.
8. Prove the status screen clearly distinguishes the immutable original **installer build number** from the current **Vincent software version/build**.
9. Prove Debian/system maintenance and representative development-tool maintenance without reimaging.
10. Implement safe public-upstream Vincent self-update in V1 if it does not materially delay the core proof. Updating Vincent changes only the software identity, never installer provenance.
11. Prove the V1 operator-selected Git connection workflow: repository URL entry, interactive authentication, local connection state, project/dependency profile, assignment input, and report/output location.
12. Prove project profiles can constrain dependency versions and that Vincent respects those constraints during installation and maintenance.
13. Execute one harmless bounded Git-assigned task with safe ownership/claiming, isolated work, validation, and report publication.
14. Repeat a clean installation and publish physical-test evidence recording both installer and current Vincent software identities.

**V1 acceptance:** two reproducible fresh installs reach unassigned READY without private Mission Control configuration; one worker connects to an operator-selected private Git repository, prepares its constrained task environment, completes one bounded assignment, and publishes its report. Debian/toolchain maintenance works without reimaging. Installer-build provenance remains immutable while Vincent software can advance independently through in-place update.

## Version 1.1 lifecycle and installer work

1. Complete/strengthen public-upstream Vincent self-update if the full mechanism was deferred from V1.
2. Implement the proposed `VINCENT-DEC-010` network-installer path: when online, an installer may fetch and validate the current compatible approved Vincent release from the public upstream instead of being limited to its bundled Vincent version.
3. Preserve an offline installation/recovery path using the installer image's bundled validated Vincent payload.
4. Define installer-to-Vincent compatibility metadata so an old installer never installs a newer incompatible Vincent release.
5. Add deterministic fallback from failed/incompatible network retrieval to the bundled payload.
6. Add robust rollback/recovery for failed Vincent application updates beyond the minimum V1 safety mechanism.
7. Define update channels/policies such as stable versus testing, staged/canary adoption, maintenance windows, and automatic versus operator-approved activation.
8. Improve status/reporting so original installer build, current Vincent software version/build, Debian maintenance state, and project-tool constraints are distinct.
9. Ensure routine Vincent application upgrades never require a new ISO except when an underlying installer/base-image compatibility change genuinely requires a newer installer.

**V1.1 network-installer objective:** a compatible older USB installer remains useful: online installation obtains the current approved Vincent release; offline installation uses its bundled release; both produce a worker whose immutable installer provenance and current Vincent software identity are accurately reported.

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
- Installer build identity and Vincent software identity are distinct lifecycle values and must never be conflated.
- Public Vincent content never exposes private project/fleet state or secrets.
