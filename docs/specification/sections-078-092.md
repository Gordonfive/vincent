# 78. Design Durable Worker State and Recovery

Define which state is:

- authoritative in Git;
- transient on the worker;
- reconstructable;
- secret;
- machine-specific.

The worker must survive:

- reboot;
- supervisor restart;
- Codex termination;
- network interruption;
- unexpected power loss.

After restart, the supervisor must determine what it was doing without relying on terminal history or human memory.

Local operational state may be stored in a simple durable format or database when appropriate, but it must not become the sole source of valuable project state.

Document recovery behavior for every task state.

---

# 79. Define Checkpoint Policy

Codex work may run for extended periods.

Define when useful progress should become durable.

Possible checkpoints include:

- before risky changes;
- after a coherent implementation milestone;
- before lengthy tests;
- before waiting for human input;
- when a usage limit is encountered;
- before supervisor-controlled shutdown;
- at task completion.

Do not require meaningless commits merely to satisfy a timer.

Commits should represent coherent recoverable work whenever practical.

The platform must distinguish:

```
local progress
committed progress
pushed progress
integrated progress
```

Only pushed state is safely independent of the worker.

---

# 80. Design Reboot Recovery

Create an explicit reboot-recovery sequence.

Conceptually:

```
boot
  ↓
systemd starts supervisor
  ↓
validate worker identity
  ↓
inspect local state
  ↓
fetch authoritative remote state
  ↓
reconcile task ownership
  ↓
inspect workspace
  ↓
determine safe continuation
  ↓
resume or escalate
```

The worker must not blindly restart a Codex task merely because an `ACTIVE` marker exists locally.

It must verify that:

- the task still exists;
- the task has not been cancelled;
- ownership remains valid;
- another worker has not superseded it;
- the remote branch has not changed unexpectedly.

Recovery behavior must be deterministic and documented.

---

# 81. Design Codex Interruption Recovery

Determine what happens when Codex itself terminates unexpectedly while the worker supervisor remains operational.

The supervisor should capture:

- Codex exit status;
- available structured error information;
- current task;
- workspace state;
- Git state;
- validation state.

The supervisor should classify the interruption before deciding whether to retry.

Examples:

```
TRANSIENT_CODEX_FAILURE
AUTHENTICATION_FAILURE
USAGE_LIMIT
TASK_FAILURE
UNKNOWN_FAILURE
```

Do not automatically restart indefinitely.

Implement bounded retries where appropriate.

Repeated unexplained failures should transition the task to a blocked or failed state and produce a report.

---

# 82. Design Usage-Limit Recovery

Investigate how current Codex tooling reports usage exhaustion or temporary capacity restrictions.

Where detectable, represent this separately from task failure.

Conceptual behavior:

```
Codex reaches usage limit
       ↓
supervisor detects condition
       ↓
preserve workspace
       ↓
push safe checkpoint if appropriate
       ↓
task → USAGE_LIMITED
       ↓
wait
       ↓
capacity becomes available
       ↓
verify ownership/state
       ↓
resume
```

Do not assume token-reset timing can be derived reliably unless the supported interface explicitly provides it.

If automatic detection of renewed capacity is not supported, design a conservative retry mechanism.

---

# 83. Design Git Synchronization Rules

Define exact synchronization behavior.

Before starting work, a worker should normally:

1. verify repository identity;
2. verify expected remote;
3. fetch;
4. verify base branch;
5. verify task branch/worktree;
6. detect unexpected local modifications;
7. determine whether remote work changed;
8. establish a known starting commit.

Before publishing work:

1. fetch again;
2. detect remote changes;
3. run required validation;
4. commit;
5. push;
6. verify remote commit;
7. record resulting commit hash.

Do not use destructive Git commands as routine conflict resolution.

Force pushes should be prohibited by default.

---

# 84. Define Integration Ownership

Worker task completion and project integration are separate concepts.

A worker may complete a branch without having authority to merge it into the project's authoritative integration branch.

Define project-configurable integration policies.

Possible modes:

```
WORKER_PUSH_ONLY

COORDINATOR_INTEGRATES

CHATGPT_REVIEW_THEN_INTEGRATE

HUMAN_APPROVAL_REQUIRED
```

The initial platform should support conservative integration.

Do not assume every project wants autonomous merging.

For important projects, ChatGPT or the owner may remain the integration authority.

---

# 85. Design Validation Contracts

Tasks should specify how completion is validated.

Acceptance criteria should be executable whenever practical.

Examples:

```
git diff --check
unit tests
integration tests
composer validation
Drupal status checks
DDEV health checks
HTTP assertions
browser tests
```

The worker should record:

- validation command;
- exit status;
- relevant result;
- timestamp.

Codex saying "tests pass" is not sufficient evidence if the supervisor can execute and verify those tests itself.

Separate:

```
Codex implementation
```

from:

```
independent task validation
```

where practical.

---

# 86. Design Task Completion Reports

Define a standard completion report schema.

At minimum include:

```
task_id
worker_id
project
repository
branch
starting_commit
ending_commit
status
started_at
completed_at
changes_summary
validation
push_status
unresolved_items
human_decisions
platform_version
```

Reports should be both machine-readable and reasonably understandable by humans.

Consider a structured format plus generated Markdown if useful.

Do not duplicate large command logs directly into reports.

Store or reference detailed logs separately when necessary.

---

# 87. Design Blocked-Task Reports

A blocked task should explain exactly why it cannot continue.

Examples:

```
NEEDS_OWNER_DECISION
MERGE_CONFLICT
MISSING_CREDENTIAL
PRODUCTION_PERMISSION_REQUIRED
TEST_ENVIRONMENT_FAILURE
EXTERNAL_DEPENDENCY
AMBIGUOUS_REQUIREMENT
```

The report should contain:

- what Codex attempted;
- current preserved state;
- why automatic continuation is unsafe;
- available options;
- exact question requiring resolution.

A blocked worker should not consume Codex capacity repeatedly reconsidering an unchanged problem.

---

# 88. Design Human Decision Requests

Human questions should eventually be routable to the owner without requiring direct worker access.

Define a durable decision-request object.

Conceptual example:

```
decision_id: DEC-001
task_id: KTN-204
worker_id: worker-heavy-01
question: >
  Two incompatible migration approaches are available.
options:
  - A
  - B
recommendation: A
blocking: true
```

A response should itself become durable.

This allows ChatGPT to explain the decision request to the owner, obtain a decision, and write that decision back into the coordination system.

The worker can then continue.

---

# 89. Define Notification Events

Create a small event vocabulary.

Initial events might include:

```
WORKER_ONLINE
WORKER_OFFLINE
TASK_STARTED
TASK_COMPLETED
TASK_FAILED
TASK_BLOCKED
HUMAN_DECISION_REQUIRED
USAGE_LIMITED
TASK_RESUMED
```

Do not initially implement every possible notification transport.

First create a clean event interface.

Then notification adapters can later send events through appropriate channels.

Important state must remain queryable even if a notification is lost.

Notifications are alerts, not authoritative state.

---

# 90. Design Worker Heartbeats

The coordinator eventually needs to distinguish an idle worker from a dead worker.

Define a lightweight heartbeat mechanism.

A heartbeat may contain:

```
worker_id
timestamp
supervisor_version
state
current_task
resource_summary
```

Do not generate Git commits every few seconds merely to represent heartbeats.

High-frequency ephemeral state belongs in an operational mechanism better suited to it.

During the Git-only prototype, use a deliberately low-frequency mechanism or defer real-time presence detection until the coordinator exists.

Document this boundary explicitly.

---

# 91. Separate Durable and Ephemeral Coordination

Do not force Git to solve every distributed-systems problem.

Git is appropriate for durable information such as:

- task definitions;
- project configuration;
- reports;
- decisions;
- Project DNA;
- implementation history.

Git may be inappropriate for high-frequency information such as:

- second-by-second heartbeat;
- live CPU usage;
- process IDs;
- streaming logs;
- rapidly renewed leases.

Design the system so a future coordinator can maintain ephemeral operational state without displacing Git as the durable development authority.

This separation is fundamental to Mission Control.

---

# 92. Produce the Phase 0 Architecture Package

Before beginning Phase 1 implementation, Codex must produce a reviewable Phase 0 architecture package.

It should include at least:

```
README.md
AGENTS.md
docs/project-dna/
docs/architecture/
docs/security/
docs/protocols/
docs/operations/
```

The package must document:

- system architecture;
- authority model;
- worker lifecycle;
- Codex interface findings;
- enrollment model;
- authentication recommendation;
- task protocol;
- claiming protocol;
- worker state machine;
- Git workflow;
- workspace isolation;
- recovery behavior;
- validation model;
- reporting model;
- durable versus ephemeral state;
- Phase 1 implementation plan.

Commit and push the Phase 0 package.

Do not begin destructive testing of the first workstation until this architecture has been reviewed and accepted.

**Pause here. Section 93 should begin the Phase 0 review and acceptance gate, followed by the transition into building the first real disposable worker.**
