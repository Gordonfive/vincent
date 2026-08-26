# Vincent Decision Register

**Register updated:** 2026-08-26T13:22:00-08:00

This register records owner-approved product and architecture decisions that affect Vincent's design or operation.

The roadmap describes what remains to be accomplished. Architecture and specification documents describe the resulting system. This register explains consequential choices and why they were made.

## Decision lifecycle and authority

- `Accepted` — current decision.
- `Superseded` — retained for history but replaced by another decision.
- `Withdrawn` — deliberately abandoned without a direct replacement.
- `Proposed` — under consideration and not authoritative.

Every decision must carry a full timestamp in ISO 8601 format including UTC offset, for example `2026-08-26T07:50:00-08:00`. A date alone is insufficient.

When two accepted decisions genuinely conflict and neither explicitly supersedes the other, the decision with the later authoritative timestamp controls. Explicit `Supersedes`/`Superseded by` relationships should still be recorded whenever a conflict is known. If timestamps are identical or ordering remains ambiguous, do not guess: require owner clarification and record the resolving decision with a new timestamp.

The timestamp represents when the owner made or explicitly approved the decision, not when a worker happened to edit the file. Git commit timestamps provide additional provenance but do not replace the decision timestamp.

Do not delete an accepted decision merely because the design later changes. Mark it `Superseded` and identify its replacement. Git history remains useful, but the current document must also make the decision chain understandable without reconstructing old commits.

Detailed ADRs may live under `docs/decisions/`. This file is the human-readable index and concise decision history. New ADRs and decision records must follow the same timestamp and conflict-resolution rule.

## Incremental refresh rule

Agents should retain the timestamp of the newest authoritative decision they have already incorporated. Before any build, release, flash-preparation step, or other consequential execution, ChatGPT or Codex must refresh the decision register and ingest every decision newer than that remembered timestamp.

Agents do **not** need to re-read older decisions that are already known and whose authoritative timestamps are at or before the agent's recorded decision checkpoint. If the agent has no trustworthy checkpoint, it must read the full current decision set once and establish one.

A build must not proceed from stale decision knowledge. If a newer decision changes build requirements, architecture, safety gates, account behavior, naming, credentials, installer behavior, or acceptance criteria, the build instructions and source must be reconciled first.

## VINCENT-DEC-001 — Worker Unix identity

**Timestamp:** 2026-08-26T07:50:00-08:00  
**Status:** Accepted

### Decision

Vincent workers use a dedicated local `vincent` Unix service account for automation. Vincent does not run as `nobody`, and installation does not require creation of a conventional human login account.

The `vincent` account is created automatically, is non-human, does not permit normal password login, and receives only required filesystem permissions, groups, capabilities, and privileged interfaces. It does not receive unrestricted sudo.

Root is reserved for installer/bootstrap and narrowly controlled system operations. Normal remote root login is disabled. Human administrative/recovery access is separate and optional, provisioned deliberately when required.

### Rationale

A dedicated service identity provides predictable ownership, least-privilege isolation, useful auditing, and clean systemd/service integration. `nobody` is a shared catch-all identity and provides poor ownership and audit semantics. A normal human account would unnecessarily couple unattended appliance operation to interactive credentials.

### Consequences

- The Debian installer must support unattended installation without prompting for an arbitrary human username/password.
- Runtime files and repositories requiring persistent ownership belong to `vincent` or another explicitly documented system identity.
- Privileged operations must use narrow root-owned helpers/systemd interfaces rather than broad sudo authority.
- Interactive troubleshooting must not require converting `vincent` into a normal privileged login account.
- Recovery/admin authentication requires a separately designed mechanism.

### Supersedes

Earlier implementation assumptions that a normal installer-created user such as `gitboy` or another human account is required for routine worker operation.

## VINCENT-DEC-002 — Incremental decision refresh before builds

**Timestamp:** 2026-08-26T08:10:43-08:00  
**Status:** Accepted

### Decision

Before every build, ChatGPT or Codex must check the authoritative decision register for decisions newer than its last-known decision timestamp and incorporate those changes before execution. Previously known decisions do not need to be re-read unless the agent lacks a trustworthy decision checkpoint or a newer decision indicates that earlier material must be revisited.

The roadmap must carry a full last-updated timestamp so an agent can determine whether its roadmap knowledge is stale and refresh only when necessary.

### Rationale

This preserves authoritative owner decisions at build time while avoiding repeated re-reading of unchanged project history. It also gives long-lived agents, new sessions, and concurrent workers an inexpensive freshness check before consequential operations.

### Consequences

- Build workflows need an explicit decision-refresh gate before build execution.
- Agents should record the newest incorporated decision timestamp in their work logs/handoffs when practical.
- `docs/ROADMAP.md` must expose an ISO 8601 last-updated timestamp with UTC offset.
- If the roadmap timestamp is newer than an agent's known roadmap checkpoint, the roadmap must be refreshed before continuing roadmap-directed work.

## VINCENT-DEC-003 — Installer disk partitioning remains interactive

**Timestamp:** 2026-08-26T08:12:25-08:00  
**Status:** Accepted

### Decision

Remove Vincent-specific installer code that automatically selects guided partitioning with LVM. Disk configuration must be chosen during installation through the normal Debian installer partitioning workflow and defaults rather than being forced by Vincent automation.

Vincent may provide documentation or recommendations, but it must not preselect guided partitioning, LVM, whole-disk use, a partition recipe, or an equivalent destructive disk-layout choice on behalf of the installer operator.

### Rationale

Disk layout is hardware- and deployment-specific and is sufficiently destructive that the normal installer should present the available choices to the operator. Keeping partition selection interactive also avoids baking one storage policy into a reusable Vincent image.

### Consequences

- Remove any active preseed, installer configuration, scripts, or build logic that force guided partitioning or LVM.
- ISO validation must confirm that the normal Debian disk-partitioning choice remains available during installation.
- Physical-install acceptance must no longer require a specific whole-disk or LVM layout unless a later decision explicitly reintroduces one.
- Destructive device-selection and flashing authorization gates remain separate and unchanged.

### Supersedes

Earlier requirements or implementation assumptions that Vincent automatically selects whole-disk guided partitioning with LVM or a fixed partitioning recipe.

## VINCENT-DEC-004 — Build numbers identify images and USB media

**Timestamp:** 2026-08-26T08:20:01-08:00  
**Status:** Accepted

### Decision

Every Vincent ISO build must have a build number. The same build number must be visible in the generated image filename and in the label/identity applied to USB installation media written from that image.

The build number is part of the artifact identity and must remain consistent across the ISO filename, ISO/volume metadata where supported, USB media label/identity, build manifest, checksum records, and validation reports for that build.

### Rationale

A visible build number makes it possible to identify physical media and image files unambiguously, correlate them with validation evidence, and avoid accidentally testing or installing an obsolete image.

### Consequences

- Build tooling must allocate or receive a build number before image creation.
- ISO filenames must include the build number.
- Flashing procedures must ensure the written USB is identifiable by the same build number, using filesystem/volume metadata or another durable machine-readable media label supported by the image format.
- Build manifests, checksums, logs, and physical-test reports must record the build number.
- Validation must fail if artifact identifiers disagree about the build number.
- The precise numbering format and allocation mechanism may be implemented separately, but build numbers must be unique and monotonically increasing within the Vincent ISO build sequence.

## VINCENT-DEC-005 — Worker status displays installed build number

**Timestamp:** 2026-08-26T08:30:34-08:00  
**Status:** Accepted

### Decision

The Vincent worker status screen must display the installed Vincent build number in a clearly visible location.

The displayed build number must come from the installed build metadata and must match the build number associated with the ISO/image from which that worker was installed.

### Rationale

Displaying the build number on the worker itself makes physical and remote troubleshooting easier and allows operators to immediately correlate a running worker with its source image, USB media, manifests, checksums, and validation evidence.

### Consequences

- The build number must survive installation as durable local metadata.
- The Vincent status screen must render that value.
- Validation must confirm the displayed worker build number matches the installed build metadata.
- Physical-test reports must record and verify the build number shown on the worker status screen.

## VINCENT-DEC-006 — Vincent V1 is control-source agnostic and uses operator-selected Git

**Timestamp:** 2026-08-26T13:22:00-08:00  
**Status:** Accepted

### Decision

A freshly installed Vincent worker must not know about or depend on `Gordonfive/mission-control` by default. Vincent is a generic worker appliance that boots into a self-contained unassigned state, can run local health/self-checks, and can obtain Vincent software updates independently of any project control repository.

When the operator is ready to assign the worker, Vincent presents a connection/enrollment workflow. The architecture may later support multiple control sources such as ChatGPT, a Git repository, or a dedicated Mission Control server. Version 1 implements the simplest control source: an operator-supplied Git repository URL.

For a private Git repository, Vincent must guide the human through authentication using a supported interactive mechanism such as account login/device authorization, a narrowly scoped connection key/token, OTP-backed authorization, or another credential flow appropriate to the Git host. No private repository credential is baked into the ISO.

After authorization, Vincent reads project-specific instructions from the connected repository. Those instructions may include a project profile or dependency 'shopping list' describing software and configuration needed for that workload, such as DDEV, Drupal, language runtimes, or other tools not required by generic Vincent.

The V1 Git control contract must include at minimum:

- an assignment input that tells the worker what work to perform; and
- a report/output location where the worker records the result of that work.

Additional files or directories may be defined as needed for project configuration, dependency profiles, state, validation evidence, locking/claiming, or coordination.

### Rationale

Keeping Vincent unaware of a specific private control repository preserves its value as a reusable generic worker and prevents project-specific/private configuration from leaking into the public image. A Git-backed V1 provides durable coordination using infrastructure already available without requiring a separate server application before the worker concept is proven.

### Consequences

- Remove any default/bootstrap assumption that Vincent automatically contacts `Gordonfive/mission-control` or any other project-specific private repository.
- Generic Vincent must remain useful before assignment: boot, networking, self-checks, diagnostics, status display, and Vincent update checks must work without enrollment.
- Project-specific packages such as DDEV or Drupal tooling are not generic-image requirements unless separately justified; they may be installed after connection according to the selected repository's project profile.
- The Git repository URL and authentication state become part of local worker enrollment/configuration after the operator explicitly connects the worker.
- Repository credentials must be scoped as narrowly as practical and stored using an appropriate protected local mechanism.
- The Git assignment/report protocol must be documented and made safe for retry, concurrent workers, and interrupted execution before multi-worker operation is considered proven.
- A future dedicated Mission Control server is deferred. If implemented later, it is another control-source/enrollment backend rather than something every Vincent worker inherently knows about.

### Supersedes

Earlier assumptions that a fresh Vincent worker inherently knows about Mission Control, automatically enrolls with `Gordonfive/mission-control`, or requires private Mission Control repository access to reach READY.

## Existing detailed decisions

- `docs/decisions/ADR-0001-CODEX-EXEC.md` — existing Codex execution ADR. Retain as a detailed ADR; reconcile/index its decision here when that architecture is next reviewed.
- `docs/decisions/WORKSTREAM_1_ACCEPTANCE.md` — acceptance evidence rather than a general architecture decision; retain as durable workstream evidence.
