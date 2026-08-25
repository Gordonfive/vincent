# 68. Instructions to the First Codex

You are beginning implementation of the Codex Autonomous Worker Platform described in this specification.

Do **not** immediately attempt to build the entire system.

Your first responsibility is to turn this specification into a technically grounded implementation project.

Perform Phase 0 first.

The initial objective is to establish the architecture, repository, protocols, security model, and implementation sequence necessary to build the first disposable worker safely and reproducibly.

Do not begin implementing later phases merely because they appear straightforward.

---

# 69. Establish the Platform Repository

Create or prepare a dedicated repository for the platform.

Suggested name:

```
codex-worker-platform
```

Do not place this infrastructure inside Ketchikan.net, OceanMail, BEMPIC, or another application repository.

Establish an initial structure similar to:

```
/
├── AGENTS.md
├── README.md
├── docs/
│   ├── architecture/
│   ├── project-dna/
│   ├── protocols/
│   ├── security/
│   ├── operations/
│   └── decisions/
├── installer/
├── bootstrap/
├── worker/
├── coordinator/
├── config/
├── scripts/
├── tests/
└── examples/
```

This is a suggested structure, not an immutable requirement.

Codex may improve it when there is a concrete technical reason.

Document significant deviations.

---

# 70. Preserve Project DNA

Create canonical Project DNA documentation before substantial implementation begins.

It must preserve at least:

- project mission;
- owner/ChatGPT/Codex/coordinator/Git authority model;
- disposable-worker philosophy;
- Git-as-authority requirement;
- remote/phone-first management objective;
- universal-installer objective;
- human-judgment requirement;
- automation philosophy;
- security boundaries;
- relationship to Mission Control.

Do not reduce Project DNA to a generic README.

It exists specifically to preserve **why the platform exists and how decisions should be made**.

Implementation documentation may change frequently.

Project DNA should change deliberately.

---

# 71. Inspect Current Codex Capabilities

Before designing the Codex supervisor, determine the actual supported Codex interfaces available at implementation time.

Do not design against assumptions from previous conversations.

Investigate and document:

- Codex CLI capabilities;
- noninteractive execution;
- authentication;
- session persistence;
- resumability;
- exit behavior;
- permission controls;
- sandbox controls;
- output formats;
- machine-readable output if available;
- usage-limit behavior;
- error signaling;
- ability to resume interrupted tasks;
- supported configuration mechanisms.

Prefer official supported interfaces.

Do not build automation based on terminal keystroke injection if a proper programmatic interface exists.

Produce a technical report containing findings and their architectural consequences.

---

# 72. Design the Worker Protocol

Define the first version of the worker/task protocol before building the worker daemon.

The protocol must describe at minimum:

- worker identity;
- worker capabilities;
- worker status;
- task identity;
- task assignment;
- task claiming;
- task state transitions;
- completion;
- failure;
- blocking;
- human-decision requests;
- recovery after interruption.

Define valid task states.

For example:

```
QUEUED
CLAIMING
ACTIVE
BLOCKED
WAITING_FOR_HUMAN
USAGE_LIMITED
COMPLETED
FAILED
CANCELLED
SUPERSEDED
```

Determine which component is authorized to perform each transition.

The protocol should be simple enough to inspect manually in Git.

Version the protocol from the beginning.

---

# 73. Solve Task Claiming Before Parallel Execution

The system must have a deterministic method preventing two workers from unknowingly executing the same exclusive task.

Analyze the race conditions created by Git polling.

The design must address cases such as:

1. Two workers fetch simultaneously.
2. Both see the same queued task.
3. Both attempt to claim it.
4. One claim succeeds.
5. The other must detect that it lost ownership and stop.

Do not rely solely on:

```
if file exists, assume task is free
```

because multiple workers can observe the same state concurrently.

Possible mechanisms may involve:

- atomic remote Git updates;
- task-specific branches;
- compare-and-swap behavior;
- GitHub API operations;
- coordinator-mediated leases.

Choose the simplest mechanism that provides correct ownership semantics.

Document the reasoning and failure behavior before implementing parallel workers.

---

# 74. Design Worker Enrollment

Design the universal worker enrollment procedure.

Required properties:

- installer is generic;
- permanent owner credentials are not embedded;
- worker generates unique identity;
- owner can inspect the identity;
- owner explicitly authorizes enrollment;
- authorization can preferably be performed remotely;
- each worker can later be independently revoked;
- reinstalling a worker does not accidentally impersonate the previous installation unless deliberately restored.

Document the complete trust chain:

```
installer
   ↓
new machine
   ↓
generated identity
   ↓
enrollment request
   ↓
owner approval
   ↓
authorized worker
   ↓
operational credentials
```

Explicitly identify which step establishes initial trust.

Do not hide the bootstrap problem behind vague references to "fetching credentials."

---

# 75. Evaluate GitHub Authentication Options

Evaluate current GitHub mechanisms for the worker platform.

At minimum compare:

- deploy keys;
- GitHub Apps;
- fine-grained personal access tokens where relevant;
- SSH-based repository access;
- GitHub API authentication.

Evaluate each against:

- per-worker identity;
- multiple repository access;
- write access;
- revocation;
- credential rotation;
- unattended operation;
- bootstrap complexity;
- least privilege;
- scalability to multiple projects;
- compatibility with a universal installer.

Deploy keys may be sufficient for the prototype, but do not assume they remain the best mechanism once one worker needs controlled access to many repositories.

Recommend an initial mechanism and a likely migration path.

Do not place secrets in the repository.

---

# 76. Design the Worker Supervisor

Specify the local worker supervisor.

The supervisor should eventually be responsible for:

- startup after boot;
- worker registration;
- Git synchronization;
- task discovery;
- task claiming;
- workspace preparation;
- Codex invocation;
- status tracking;
- validation execution;
- Git commit/push workflow;
- report generation;
- failure handling;
- waiting/retry behavior.

Prefer a conventional Linux service.

Expected architecture should likely resemble:

```
systemd
   ↓
worker supervisor
   ↓
task state machine
   ↓
workspace manager
   ↓
Codex
   ↓
validation
   ↓
Git/reporting
```

Do not create one giant shell script containing the entire platform.

Shell scripts are appropriate for straightforward provisioning and system operations.

Use a maintainable implementation language for stateful orchestration if the complexity warrants it.

Document the language/runtime choice and reasoning.

---

# 77. Design Workspace Isolation

Define how one worker safely handles repositories and tasks.

Each active task should have a predictable workspace.

For example:

```
/srv/codex/
    platform/
    projects/
    worktrees/
    state/
    logs/
```

Exact paths may differ.

The design must prevent:

- one task contaminating another;
- one worker accidentally using another worker's DDEV project name;
- stale branches being mistaken for current work;
- dirty worktrees silently entering new assignments;
- untracked files being lost without reporting.

For Drupal/DDEV projects, derive unique local project identifiers from stable worker/task information.

Example concept:

```
<project>-<worker>-<task>
```

The workspace manager must verify repository state before Codex begins work.

Unexpected dirty state should be treated as recoverable evidence, not automatically deleted.

Stop here after completing Sections 68–77. The next specification segment should begin with **Section 78: Design Durable Worker State and Recovery**.
