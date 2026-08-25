# 93. Phase 0 Review and Acceptance Gate

Phase 0 is an architecture gate, not merely a documentation milestone.

Before Phase 1 begins, review the architecture package against the original mission.

Verify that the proposed implementation preserves:

- Git as durable authority;
- Project DNA;
- disposable workers;
- generic provisioning;
- per-worker identity;
- remote operation;
- multiple-worker support;
- recovery after interruption;
- human authority;
- ChatGPT's coordination role;
- separation between durable and ephemeral state;
- project independence.

Resolve architectural contradictions before proceeding.

Record the accepted architecture commit.

Phase 1 must begin from that known Git state.

---

# 94. Freeze the Initial Protocol Version

Before the first real worker begins operating, assign versions to protocols that will cross component boundaries.

At minimum consider:

```
task_schema_version
worker_status_schema_version
report_schema_version
decision_schema_version
worker_protocol_version

```

Initial versions may simply be:

```
1

```

Do not create elaborate semantic-version compatibility machinery yet.

The objective is to prevent silent interpretation changes.

If a schema changes incompatibly, the worker should detect the unsupported version rather than guessing.

---

# 95. Establish the Phase 1 Test Machine

Select the first disposable workstation.

The older high-memory workstation is the preferred initial candidate.

Before modifying it, inventory:

- CPU;
- RAM;
- storage controllers;
- disks;
- network adapters;
- firmware boot mode;
- architecture;
- existing operating system;
- hardware requiring non-free firmware.

Record only information useful to reproducing installation.

Do not preserve unnecessary machine-specific assumptions in the platform.

The machine should be treated as expendable after any data that actually matters has been removed.

---

# 96. Establish the Destructive-Test Boundary

Before automated installation is permitted to erase disks, define an explicit destructive-test boundary.

The installer must make it difficult to accidentally erase a normal workstation.

During development, require a deliberate indicator identifying the machine as a disposable worker candidate.

Possible protections include:

- installer-specific boot media;
- explicit installation profile;
- expected machine enrollment state;
- disk-selection validation;
- unmistakable destructive confirmation during development.

The final unattended workflow may intentionally eliminate keyboard interaction, but only after the target-selection mechanism is proven safe.

Never infer that every disk visible to the installer may be erased.

---

# 97. Build the Debian 13 Installation Prototype

Create the first unattended Debian 13 installation prototype using supported Debian mechanisms.

The prototype should automate:

- locale;
- timezone;
- keyboard defaults;
- networking where DHCP is available;
- disk layout;
- package selection;
- bootloader installation;
- worker account creation;
- initial bootstrap installation.

Prefer a minimal base system.

Do not install a desktop environment unless testing demonstrates a requirement.

The resulting system should be suitable for headless operation.

Keep installer configuration in Git.

---

# 98. Define Worker Disk Layout

Choose a simple disk layout appropriate for disposable development workers.

Account for storage consumed by:

- Docker;
- DDEV;
- Git repositories;
- worktrees;
- Drupal files;
- Composer caches;
- Node caches;
- temporary build artifacts;
- logs.

Avoid unnecessary partition complexity.

The system should tolerate ordinary development workloads without filling the root filesystem unexpectedly.

If multiple physical SSDs are present, do not require a multi-disk layout for the platform to function.

Optional optimization for larger workers can be added later.

Document the default layout and recovery consequences.

---

# 99. Configure the Base Operating System

After installation, bootstrap the machine into a predictable worker baseline.

Configure at minimum:

- hostname strategy;
- worker service account;
- SSH server for administrative fallback;
- time synchronization;
- CA certificates;
- Git;
- required archive/download tools;
- system logging;
- automatic service startup;
- security updates according to documented policy.

Avoid interactive package configuration.

Every required change must be represented in code/configuration.

A manually corrected machine is not a completed provisioning implementation until the correction has been encoded into the bootstrap process.

---

# 100. Install the Container Toolchain

Install and verify the container environment required by development projects.

For the initial target this includes:

- Docker Engine;
- required Docker plugins;
- DDEV;
- supporting packages.

Verify actual operation rather than package presence.

Acceptance should include commands equivalent in purpose to:

```
docker version
docker info
ddev version

```

The worker service account must have the intended ability to run the container workloads required by Codex.

Document the security implications of Docker access.

For dedicated disposable workers, operational usefulness may justify broad local Docker authority.

---

# 101. Install the Development Toolchain

Install the common tools required for software development.

The baseline should include only broadly useful dependencies.

Potential examples:

- Git;
- GitHub CLI if selected by the architecture;
- curl;
- jq;
- Python;
- shell tooling;
- Node.js where required;
- PHP/Composer where required outside DDEV;
- build tools;
- browser/testing dependencies where justified.

Prefer project-local or containerized tooling when that improves reproducibility.

Do not turn the base OS into an uncontrolled collection of globally installed dependencies.

Document which tools belong to:

```
worker baseline

```

versus:

```
project environment

```

---

# 102. Install Codex

Install Codex using the supported method identified during Phase 0.

Pin or otherwise record the installed version sufficiently for reproducibility.

Configure:

- authentication mechanism;
- permission model;
- default execution environment;
- repository access expectations;
- machine-readable output where supported;
- supervisor integration.

Do not embed personal owner credentials into the installer.

Verify Codex can perform a harmless local test task noninteractively or through the selected supervisor interface.

Record actual observed behavior.

---

# 103. Implement First-Boot Identity Generation

On the first successful boot of a newly provisioned worker, generate its unique machine identity.

The process should:

1. determine that enrollment has not previously completed;
2. create required cryptographic identity;
3. assign or request a human-readable worker name;
4. generate an enrollment request;
5. persist the private identity securely on the worker;
6. expose only the public enrollment information externally.

Do not regenerate identity on every reboot.

Reinstallation should normally create a new identity unless an explicit recovery process restores the old one.

---

# 104. Implement Owner Enrollment Approval

Create the first practical owner-approval workflow.

For the prototype, simplicity is more important than eliminating every manual action.

The owner should be able to inspect:

- worker name;
- enrollment identifier;
- public key/fingerprint;
- requested permissions.

Approval should grant only the credentials/access required for the prototype.

Record:

- who/what approved enrollment;
- enrollment time;
- worker identity;
- granted scope.

Do not place approval secrets in ordinary Git history.

Design the workflow so it can later be performed comfortably from a phone.

---

# 105. Bootstrap Repository Access

After enrollment, the worker must obtain access to the repositories required for its role.

Verify actual authenticated operations:

```
fetch
clone
create branch
push authorized test branch

```

Do not test write access against important production/integration branches.

Use a dedicated bootstrap/test repository or explicitly safe test branch.

Verify that the worker cannot access repositories outside the intended authorization scope where the selected credential mechanism supports such isolation.

Record the credential mechanism without exposing the credential.

---

# 106. Install the Worker Supervisor

Install the initial worker supervisor as a managed system service.

It must start automatically after reboot.

At minimum it should be able to:

- identify the worker;
- load configuration;
- verify prerequisites;
- synchronize coordination state;
- report its state;
- detect an assigned test task;
- prepare a workspace;
- invoke the selected execution mechanism;
- capture results.

Use systemd service management.

Verify:

```
start
stop
restart
crash recovery
boot startup
log access

```

A supervisor that works only when launched manually from a shell does not satisfy Phase 1.

---

# 107. Implement the First End-to-End Test Task

Create a deliberately harmless test assignment that exercises the complete worker path.

The test should require the worker to:

1. discover the assignment remotely;
2. claim it;
3. create an isolated workspace;
4. invoke Codex;
5. make a small deterministic repository change;
6. execute defined validation;
7. commit the change;
8. push it;
9. verify the remote commit;
10. generate a completion report;
11. return to `IDLE`.

The task should not involve Drupal yet.

Use the smallest possible repository change that proves the orchestration path works.

The important test is not the complexity of the coding task.

The important test is:

```
remote instruction
    ↓
autonomous worker execution
    ↓
independently validated result
    ↓
durable Git publication
    ↓
durable report

```

**Pause here. Section 108 should begin failure injection and reboot/recovery testing of the first worker before proceeding to the universal installer and second worker.**