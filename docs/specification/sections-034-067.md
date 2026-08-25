# 34. Documentation Requirement

Documentation is part of the implementation.

Codex must maintain sufficient documentation that another Codex instance, ChatGPT thread, human administrator, or freshly provisioned worker can understand the platform without depending on previous chat history.

At minimum, documentation must describe:

- architecture;
- installation;
- bootstrap process;
- credential and authorization model;
- worker lifecycle;
- task protocol;
- Git workflow;
- worker registration;
- configuration;
- recovery;
- troubleshooting;
- security boundaries;
- coordinator behavior when implemented;
- current limitations;
- outstanding work.

Repository documentation is durable memory.

Chat history is not.

Important architectural decisions made during implementation must therefore be recorded in Git rather than existing only in Codex or ChatGPT conversations.

---

# 35. Project DNA

The platform repository must contain a canonical description of the project's intent, not merely its implementation.

This document or small set of documents should answer:

- What are we building?
- Why are we building it?
- What problems are we deliberately solving?
- What are we deliberately not solving?
- How do we make architectural decisions?
- What principles override implementation convenience?
- What is the current product philosophy?
- What does success look like?

Call this concept **Project DNA**.

Project DNA exists so that restoring a project restores not only its code but also its intent.

A new ChatGPT thread, Codex worker, contributor, or future maintainer should be able to read Project DNA and understand the reasoning that produced the system.

Project DNA should change deliberately rather than automatically.

Implementation agents may propose changes, but fundamental changes in mission, philosophy, authority, or product direction require owner approval.

---

# 36. Separation of Authority

The platform should explicitly distinguish several forms of authority.

## Owner

The owner has final authority over:

- product direction;
- priorities;
- production actions;
- security decisions;
- major architectural changes;
- Project DNA;
- acceptance of significant tradeoffs.

## ChatGPT

ChatGPT acts as the primary planning and orchestration intelligence.

It may:

- interpret owner intent;
- decompose objectives into tasks;
- decide which capabilities are required;
- assign or recommend workers;
- review reports;
- request corrections;
- coordinate integration;
- identify conflicts;
- maintain project direction.

ChatGPT does not become the durable source of truth.

Its decisions that matter to continuing work must be written into the project's durable coordination system.

## Coordinator

The coordinator is an execution and synchronization mechanism.

It should:

- discover instructions;
- identify workers;
- dispatch approved assignments;
- track operational state;
- detect completion/failure;
- surface results.

The coordinator should not independently invent product priorities merely because it has scheduling capability.

## Codex Workers

Workers execute bounded development assignments.

Workers may make ordinary engineering decisions necessary to complete those assignments, but they do not redefine the project's mission or product direction.

## Git

Git is the durable technical source of truth.

The architecture should make these boundaries explicit.

---

# 37. ChatGPT-to-Coordinator Instruction Flow

A major long-term objective is to avoid requiring the coordinator itself to decide which worker should receive a task when ChatGPT has already made that decision.

Preferred conceptual flow:

```
Owner
  ↓
ChatGPT
  ↓
durable instruction
  ↓
Git / coordination interface
  ↓
Coordinator notices change
  ↓
designated worker
  ↓
Codex execution

```

For example, ChatGPT may create an instruction conceptually equivalent to:

```
task: KTN-204
assigned_worker: worker-theme-01
objective: ...
acceptance_criteria: ...

```

The coordinator should recognize that a new instruction exists and activate the specified worker.

It should not unnecessarily reconsider ChatGPT's worker assignment.

Capability-based automatic assignment can exist for tasks where no worker was explicitly designated.

This distinction should remain part of the architecture.

---

# 38. Persistent Work and Session Recovery

Codex sessions are transient.

The system must assume:

- Codex can terminate;
- ChatGPT conversations can end;
- machines can reboot;
- network connectivity can disappear;
- token/capacity limits can interrupt work;
- processes can crash.

A task must therefore contain enough durable information to reconstruct what should happen next.

Workers should checkpoint useful progress through Git and status records.

After restart, the platform should be able to determine whether a task is:

- not started;
- claimed;
- in progress;
- interrupted;
- blocked;
- awaiting human input;
- completed;
- failed;
- superseded.

Recovery must not depend on remembering what appeared in a terminal before reboot.

---

# 39. Usage-Limit Handling

Codex capacity and usage limits are expected operational constraints.

The platform should detect whatever usage-limit signals the supported Codex interface exposes.

When work cannot continue because of a usage limit:

1. Preserve current work.
2. Commit/push useful safe checkpoints where appropriate.
3. Record the task state.
4. Record why execution stopped.
5. Avoid repeatedly hammering an unavailable service.
6. Wait according to supported behavior.
7. Resume when capacity becomes available if this can be done reliably and within supported interfaces.

The system must distinguish usage exhaustion from:

- build failure;
- network failure;
- authentication failure;
- Codex failure;
- test failure;
- human-decision requirement.

Do not disguise one state as another.

---

# 40. Resource Awareness

Workers should expose basic resource information so scheduling can eventually account for hardware differences.

Useful information includes:

- logical CPU count;
- total RAM;
- available RAM;
- disk capacity;
- free disk;
- architecture;
- Docker availability;
- DDEV availability;
- worker load;
- active DDEV environments.

Resource awareness should initially be informational.

Do not build an elaborate resource scheduler until actual usage demonstrates a need.

A future coordinator may prefer heavier workers for resource-intensive tasks while sending documentation or lightweight work to smaller laptops.

---

# 41. Resource Conservation

Workers should not waste local resources merely because they are dedicated machines.

In particular:

- stop unused DDEV environments;
- remove abandoned containers when safe;
- avoid running duplicate services unnecessarily;
- periodically identify obsolete worktrees;
- monitor disk consumption;
- avoid uncontrolled Docker image accumulation;
- preserve caches when they materially reduce repeated work and storage remains adequate.

For a 16 GB worker, only the environments required for active work may need to remain running.

The heavy workstation may support greater concurrency.

Policies should be configurable rather than based on one hardware assumption.

---

# 42. Network Failure

Workers must tolerate temporary loss of Internet connectivity.

If GitHub or Codex becomes unavailable:

- do not discard local work;
- record the condition;
- retry conservatively;
- avoid producing duplicate assignments;
- resume synchronization when connectivity returns.

A task should not be marked successfully completed until required remote state has actually been published.

For example:

```
commit succeeded
push failed

```

is not equivalent to:

```
task completed

```

The report must preserve that distinction.

---

# 43. Git Failure Handling

Every Git operation affecting authoritative state should be checked.

Workers must detect conditions including:

- fetch failure;
- authentication failure;
- non-fast-forward push;
- merge conflict;
- dirty unexpected working tree;
- branch mismatch;
- detached HEAD where inappropriate;
- missing upstream;
- remote branch changed during work.

Workers must not automatically resolve ambiguous conflicts by destroying another worker's changes.

When safe automatic reconciliation is impossible, the task should become blocked and be escalated.

---

# 44. Secret Handling

The platform must actively prevent secrets from entering normal Git history.

Examples include:

- private SSH keys;
- GitHub tokens;
- API secrets;
- production passwords;
- private certificates;
- unrestricted bootstrap credentials.

Configuration files should separate secret references from ordinary configuration.

Before commits are pushed, reasonable automated secret detection should be considered.

Worker logs and reports must also avoid casually printing secrets.

The fact that the repository is private does not make committing secrets acceptable.

---

# 45. Bootstrap Credential Problem

The architecture must explicitly document the bootstrap trust problem:

> A completely untrusted machine cannot retrieve private credentials without first possessing or obtaining some trusted identity.

Do not pretend this problem can be eliminated.

Instead, minimize the initial trust anchor.

The first implementation should evaluate practical options such as:

- one-time enrollment token;
- owner approval of a newly generated public key;
- narrowly scoped bootstrap credential;
- GitHub-based authorization;
- another simple enrollment service.

Preferred characteristics:

- universal installer contains no powerful permanent secret;
- worker generates unique credentials;
- owner can approve enrollment remotely;
- bootstrap authorization can expire;
- compromised bootstrap material cannot grant broad permanent access.

The simplest secure mechanism that satisfies these requirements should be preferred.

---

# 46. Destructive Operations

Because workers are disposable, local destructive operations can have relatively broad permission.

However, destructive operations against external systems require stronger controls.

Examples requiring explicit policy include:

- deleting remote branches;
- force pushing;
- deleting repositories;
- modifying production databases;
- destroying cloud resources;
- modifying DNS;
- deploying to production;
- rotating shared credentials;
- deleting backups.

The platform should classify operations according to blast radius rather than treating all shell commands equally.

---

# 47. Production Boundary

Development autonomy does not imply production autonomy.

Initial workers must not automatically deploy to production merely because tests pass.

Production deployment should remain behind an explicit gate until the owner deliberately changes that policy.

A worker may prepare a deployable artifact and report:

```
READY_FOR_DEPLOYMENT

```

without actually deploying it.

Production authority should be separately documented for each project.

---

# 48. Project Isolation

The worker platform must be reusable across projects.

Potential projects include:

- Ketchikan.net;
- OceanMail;
- BEMPIC;
- future open-source projects;
- internal infrastructure projects.

Do not hard-code Ketchikan.net assumptions into the platform core.

Project-specific configuration belongs in project definitions or project repositories.

The orchestration system coordinates software development.

It is not a Ketchikan.net-specific tool.

---

# 49. Worker Specialization

Workers may eventually have persistent specialties, for example:

```
frontend
backend
infrastructure
QA
documentation
integration

```

However, specialization should primarily describe capability and assignment policy.

The architecture should not require a particular physical computer forever to be "the frontend worker."

A destroyed frontend worker should be replaceable by another compatible worker.

Identity and role must therefore remain conceptually separate.

---

# 50. Worker Naming

Create predictable human-readable worker identifiers.

Names should remain stable enough for reporting but must not encode irreplaceable state.

Example:

```
worker-heavy-01
worker-general-01
worker-general-02

```

The coordinator may additionally track:

- hardware UUID or generated machine ID;
- enrollment ID;
- current role;
- capabilities;
- last-seen time.

Do not rely solely on hostname for security identity.

---

# 51. Logging

Worker services must produce useful logs.

Logs should identify:

- timestamp;
- worker;
- task;
- action;
- result;
- error condition.

Prefer structured logging where it provides clear value.

Logs should be locally inspectable through standard Linux mechanisms such as `journalctl`.

Important durable outcomes should also be reflected in Git/status reports rather than existing only in local system logs.

Avoid uncontrolled log growth.

---

# 52. Service Management

Persistent worker components should use normal Debian service management.

Prefer `systemd` for:

- worker supervisor;
- polling/coordination agent;
- health reporting;
- other persistent local services.

Services should:

- start automatically;
- restart after ordinary crashes when safe;
- expose useful status;
- log through standard mechanisms;
- avoid infinite rapid restart loops.

Use timers instead of cron when systemd timers provide materially better lifecycle and logging behavior.

---

# 53. Updates

The platform itself will evolve.

Workers need a controlled method for receiving platform updates.

Potential sequence:

```
fetch platform repository
detect approved version
validate configuration
install/update components
restart affected services
report resulting version

```

Do not allow every worker to blindly execute arbitrary newly pushed infrastructure code without considering the trust implications.

During early development, owner-controlled branches/tags may provide sufficient approval.

Later, signed releases or stronger release controls can be evaluated.

---

# 54. Versioning

The worker platform should identify its installed version.

At minimum record:

- repository commit;
- configuration version;
- protocol/schema version where necessary.

Reports should make it possible to determine which platform revision produced them.

Protocol changes must account for workers that have not updated yet.

Do not introduce complex compatibility machinery until multiple versions actually need to coexist.

---

# 55. Testing Philosophy

The platform itself must be tested.

Testing should cover increasingly realistic levels:

## Unit

Parsing, state transitions, configuration, task selection.

## Integration

Git synchronization, task claiming, status updates, worker supervisor.

## Rebuild

Fresh Debian installation and automatic provisioning.

## Multi-worker

Two or more workers operating simultaneously.

## Failure

Network interruption, Codex interruption, worker reboot, failed push, conflicting task.

## Destructive recovery

Erase a worker and rebuild it.

The destructive recovery test is particularly important because disposability is a core architectural claim.

---

# 56. Acceptance Standard

Do not declare a feature complete merely because its code exists.

Completion requires evidence.

Examples:

- command output;
- automated test;
- clean rebuild;
- actual worker enrollment;
- actual task execution;
- actual Git push;
- actual recovery after reboot.

Reports should distinguish:

```
IMPLEMENTED

```

from:

```
VERIFIED

```

A feature that has not been tested in the intended environment is not fully verified.

---

# 57. Human-Readable Failure

When automation fails, it should explain:

- what operation failed;
- which worker failed;
- which task was affected;
- what was expected;
- what actually happened;
- whether work was preserved;
- whether retry is safe;
- what human decision, if any, is required.

Avoid errors that consist solely of an exit code with no operational context.

---

# 58. No Silent Success

Critical operations must verify their result.

Examples:

A successful `git commit` does not prove the push succeeded.

A successful container start does not prove Drupal works.

A successful package installation does not prove the service started.

A successful Codex process exit does not necessarily prove task acceptance criteria passed.

Verification should correspond to the actual intended outcome.

---

# 59. Idempotency

Provisioning and maintenance operations should be idempotent wherever practical.

Running bootstrap twice should not:

- create duplicate users;
- corrupt configuration;
- duplicate repository checkouts;
- generate unnecessary new identities;
- start duplicate supervisors;
- destroy useful state.

Where an operation cannot safely be repeated, explicitly detect and document that condition.

---

# 60. Rebuild Test as a Release Gate

Eventually, major platform releases should pass a clean-machine test.

Conceptually:

```
blank compatible machine
    ↓
universal installer
    ↓
enrollment
    ↓
automated provisioning
    ↓
assigned test task
    ↓
successful Codex work
    ↓
commit/push/report

```

If this sequence fails, the platform's central promise is broken.

---

# 61. Initial User Experience

The first implementation does not need a polished GUI.

A successful early experience could be:

1. Boot machine from USB.
2. Debian installs automatically.
3. Machine reboots.
4. Worker displays enrollment information.
5. Owner approves enrollment.
6. Provisioning finishes automatically.
7. Worker announces `IDLE`.
8. Owner assigns task remotely.
9. Worker changes to `WORKING`.
10. Worker completes work.
11. Git receives commits/report.
12. Owner receives completion status.

Optimize this path before adding visual polish.

---

# 62. Future Dashboard

A dashboard may eventually show:

| WorkerStateProjectTaskResourcesLast Activity |         |               |         |       |       |
| -------------------------------------------- | ------- | ------------- | ------- | ----- | ----- |
| heavy-01                                     | WORKING | Ketchikan.net | KTN-204 | 64 GB | now   |
| general-01                                   | TESTING | Ketchikan.net | KTN-205 | 16 GB | now   |
| general-02                                   | IDLE    | —             | —       | 16 GB | 2 min |

The dashboard is a convenience layer.

It must not become the sole location containing task state.

---

# 63. Future Event-Driven Coordination

Initial Git polling is acceptable.

Once the basic architecture is proven, evaluate event-driven mechanisms such as:

- GitHub webhooks;
- GitHub Apps;
- coordinator API;
- message queue.

Do not replace simple polling merely because event-driven architecture sounds more sophisticated.

Change when there is a demonstrated operational benefit.

---

# 64. Future Worker Pool

Long term, workers should form a pool.

ChatGPT or another authorized planning layer could say conceptually:

```
task requires:
  docker
  ddev
  drupal
  ram >= 32GB

```

The coordinator could then identify an eligible idle worker.

Explicit worker assignment should remain possible.

This enables both:

- deliberate specialization;
- automatic load distribution.

---

# 65. Future Statelessness Goal

The strongest form of the architecture is:

> Nothing uniquely valuable exists on a worker.

A worker may contain temporary:

- repositories;
- databases;
- caches;
- build artifacts;
- logs;
- credentials tied to that worker.

But anything required to reconstruct meaningful project state must exist elsewhere.

This includes database fixtures or development datasets when those are necessary to reproduce a development environment.

Sensitive datasets must eventually have appropriate sanitization and secret-handling policies.

---

# 66. Relationship to Mission Control

This worker platform should be designed as the foundation of a broader **Mission Control** system.

Mission Control's purpose is to coordinate software development.

It does not replace developers or human judgment.

Conceptually:

```
ChatGPT / Owner
       ↓
  Mission Control
       ↓
  Coordinator
   ↙    ↓    ↘
Worker Worker Worker
   \     |     /
         Git

```

Mission Control should eventually make an entire development operation recoverable after:

- workstation reboot;
- worker destruction;
- laptop replacement;
- Codex restart;
- ChatGPT restart.

The goal is not merely restoring processes.

The goal is restoring the development operation and its intent.

---

# 67. Definition of Success

The project has succeeded when the owner can take a compatible spare computer, erase it, turn it into an authorized Codex worker with the universal installer, assign it meaningful development work remotely, and receive durable verified results without sitting at that computer.

The larger Mission Control vision succeeds when multiple such workers can cooperate across multiple software projects while:

- Git preserves durable state;
- Project DNA preserves intent;
- ChatGPT provides planning and coordination;
- Codex performs implementation;
- Mission Control handles repetitive orchestration;
- humans retain final judgment.

---

