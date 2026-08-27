# Vincent and Mission Control Roadmap

**Roadmap updated:** 2026-08-27T08:26:00-08:00

This roadmap describes remaining work and milestones. Detailed decisions are in `docs/DECISIONS.md`; agreed but unscheduled ideas are in `docs/PLANNED_FEATURES.md`; historical validation evidence belongs in `docs/reports/`; continuation state belongs in `docs/CONTINUATION_HANDOFF.md`.

Agents retain the newest roadmap and decision timestamps incorporated and refresh only when those authoritative timestamps advance.

## Repository roles

| Repository | Role |
|---|---|
| `Gordonfive/vincent` | Public generic Vincent worker platform and trusted upstream source for Vincent software/releases: installer, ISO tooling, first boot, self-checks, update logic, connection client, runtime, public documentation, tests, and releases. |
| `Gordonfive/mission-control` | Currently private project/control repository and future Mission Control control-plane implementation area. Mission Control is planned as a self-hostable server application with web UI and authenticated API for enrollment, fleet state, authorization, assignments, leases, approvals, and reporting. Fresh Vincent remains independently functional and does not require Mission Control. |

Mission Control's reusable application source is intended to become public if/when it becomes a distributable Vincent product. Our private deployment/fleet state must remain separate from public application source.

## Current physical-development strategy

The large workstation is the first persistent development worker. Bring its existing Vincent installation fully online as a usable worker as soon as practical, then use it together with ChatGPT/GitHub to begin Mission Control development.

The old laptop is the disposable physical-test target for ongoing Vincent and installer development. Repeated installer builds, networking changes, first-boot changes, destructive reinstall tests, failure-path tests, and worker-replacement experiments should preferentially use the laptop so the large workstation remains available for useful work.

Do not reinstall the large workstation merely to keep installer testing symmetric with the laptop. Reinstall it later only when a specific acceptance test requires proving that a working worker can be destroyed and reconstructed from durable state, or when another test genuinely requires clean-machine reproduction on that hardware.

This creates two explicit roles:

- **Large workstation:** persistent first worker, Mission Control development worker, real bounded-work test subject, and later recovery/impermanence acceptance target.
- **Old laptop:** expendable Vincent/installer test machine for frequent clean installs and destructive physical testing.

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

1. Bring the large workstation online first as the initial persistent Vincent worker without waiting for every remaining installer test.
2. Verify its networking, stable identity, self-checks, diagnostics, status, management access, Git access, development tooling, and bounded-work capability.
3. Use that workstation for real Vincent/Mission Control development while installer work continues independently on the laptop.
4. Refresh newer decisions/roadmap state before every installer build.
5. Establish one exact authorized ISO source commit for each physical test cycle.
6. Assign the next unique monotonically increasing **installer build number**.
7. Build and validate the ISO with matching installer-build identity across ISO filename/metadata, USB label, installer manifests/checksums, logs, reports, and durable installation provenance.
8. Preserve normal interactive Debian disk partitioning; Vincent does not force a storage layout.
9. Repeatedly fresh-install the laptop and prove generic unassigned READY operation: networking, stable identity, self-checks, diagnostics, status, and management access.
10. Prove the dedicated least-privileged `vincent` service identity and separately controlled privileged/recovery interfaces.
11. Prove the status screen clearly distinguishes the immutable original **installer build number** from the current **Vincent software version/build**.
12. Prove Debian/system maintenance and representative development-tool maintenance without reimaging.
13. Implement safe public-upstream Vincent self-update in V1 if it does not materially delay the core proof. Updating Vincent changes only the software identity, never installer provenance.
14. Prove the V1 operator-selected Git connection workflow: repository URL entry, interactive authentication, local connection state, project/dependency profile, assignment input, and report/output location.
15. Prove project profiles can constrain dependency versions and that Vincent respects those constraints during installation and maintenance.
16. Execute harmless bounded Git-assigned work on the large workstation and publish results/reports.
17. Continue clean-install reproducibility testing on the laptop and publish physical-test evidence recording both installer and current Vincent software identities.
18. At the worker-recovery/impermanence milestone, deliberately reinstall or otherwise destroy the large workstation's local worker state and prove that required durable project state permits the worker to be recreated without loss of authoritative work.

**V1 acceptance:** the large workstation operates as a useful persistent Vincent worker while the laptop demonstrates reproducible clean installation. At least one worker connects to an operator-selected private Git repository, prepares its constrained task environment, completes bounded work, and publishes its report. Debian/toolchain maintenance works without reimaging. Installer-build provenance remains immutable while Vincent software can advance independently through in-place update.

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

## Mission Control product track

Mission Control is planned as a self-hostable web control plane, not a desktop application or an exclusively Gordonfive-hosted website. Initial Git-backed coordination may continue while the workflow is proven. The eventual service should provide a browser UI, authenticated API, application service, and persistent data store.

Planned progression:

1. Use the large workstation as the first real managed-worker development subject while Mission Control starts as a Git-backed coordination model.
2. Define stable data models for worker identity, enrollment/trust, capabilities, assignments, leases, authorization scopes, approvals, results, and audit records.
3. Define the authenticated outbound Vincent-to-Mission-Control protocol; normal fleet operation should not require inbound worker management ports.
4. Prove enrollment, revocation, worker inventory/capability reporting, assignment leasing, structured results, and fleet status with two or more workers.
5. Implement the self-hostable Mission Control service/API and database once the proven workflow justifies replacing Git-backed operational state.
6. Implement a responsive browser interface suitable for desktop and phone-first fleet control.
7. Package Mission Control for straightforward self-hosting on Linux servers/VMs/VPSs and, where appropriate, containers/NAS environments.
8. Separate reusable/public Mission Control application source from Gordonfive's private deployment configuration and fleet operational state before public distribution.
9. Evaluate an optional hosted Mission Control service without weakening self-hosting as a first-class deployment model.

Mission Control is not a general-purpose remote shell and does not replace SSH or normal Linux administration. Vincent remains capable of booting, self-diagnosing, maintaining itself, and updating from its trusted public upstream without Mission Control.

## Later milestones

| Milestone | Outcome | Status |
|---|---|---|
| M0 | Architecture and Project DNA accepted | Complete |
| M1 | Large workstation online as persistent Vincent worker and completing bounded work | In progress |
| M2 | Laptop clean-install/recovery cycle proven; later persistent-worker impermanence/rebuild proven on large workstation | Not started |
| M3 | Universal installer proven through repeated laptop testing | Prototype / in progress |
| M4 | Two-worker Git coordination and assignment leasing proven | Not started |
| M5 | Phone-first Mission Control interface/control proven | Not started |
| M6 | Self-hostable Mission Control service/API/backend proven | Planned |
| M7 | Multi-project operation proven | Not started |
| M8 | Full operation recovery proven | Not started |

## Permanent roadmap constraints

- Git is the durable technical authority; Project DNA is canonical intent.
- Human judgment controls destructive hardware actions, production actions, credential scope, major architecture, and Project DNA changes.
- Workers are replaceable and least-privileged.
- A machine being replaceable does not require needlessly destroying a useful worker during routine development; destructive recovery testing occurs at an explicit acceptance gate.
- Vincent is generic by default; private project/control sources are operator-selected after installation unless the operator explicitly enrolls the worker into Mission Control.
- Vincent remains independently capable of boot, diagnostics, maintenance, and trusted-upstream updates without Mission Control.
- Mission Control governs managed-fleet enrollment, authorization, assignments, leases, policy, approvals, and operational reporting; it does not become a generic remote shell.
- Vincent maintains Debian, its own software, runtime dependencies, and development toolchain while honoring active project version constraints.
- The public Vincent upstream is the authoritative source for Vincent software updates; a fresh ISO is not the normal application-update mechanism.
- Installer build identity and Vincent software identity are distinct lifecycle values and must never be conflated.
- Public Vincent content never exposes private project/fleet state or secrets.
- Public Mission Control application source and private deployment/fleet state must remain separate concerns.
