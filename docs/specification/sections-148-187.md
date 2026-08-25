# 148. Define the Phone-First Control Workflow

Design routine operation around the assumption that the owner may be away from every worker and have only a phone.

The normal workflow should not require:

- SSH;
- remote desktop;
- terminal access;
- physical presence;
- manually opening Codex sessions.

Target interaction:

```
Owner
  ↓
ChatGPT
  ↓
inspect current durable state
  ↓
reason about next action
  ↓
create/update authenticated task
  ↓
worker/coordinator detects action
  ↓
Codex performs work
  ↓
results become durable
  ↓
ChatGPT reviews results
  ↓
Owner receives concise status

```

Administrative access remains available for exceptional failures.

---

# 149. Separate Conversation from Command

Natural-language conversation with ChatGPT and an actual worker command are different things.

The platform must require an explicit durable action before workers act.

For example:

```
Owner: Fix the navigation problem.

```

may cause ChatGPT to reason about the request.

The actual command becomes something like:

```
TASK-214
project: ketchikan-net
assigned_worker: worker-theme-01
objective: ...
acceptance: ...

```

Workers act on the durable task, not an ephemeral chat utterance.

This provides:

- auditability;
- recoverability;
- clear task ownership;
- protection against conversation loss;
- deterministic worker behavior.

---

# 150. Define ChatGPT Write Operations

Define the smallest set of control-plane operations ChatGPT needs.

Likely operations include:

```
create_task
update_task
cancel_task
supersede_task
assign_worker
change_priority
answer_decision
request_review
approve_integration

```

Each operation should produce a durable, auditable state change.

Do not grant an integration unrestricted shell access merely because ChatGPT needs to create tasks.

Expose narrow operations corresponding to actual coordination responsibilities.

---

# 151. Define ChatGPT Read Operations

ChatGPT should be able to inspect enough state to coordinate intelligently.

Useful read operations include:

```
list_projects
get_project_state
list_workers
get_worker_state
list_tasks
get_task
get_report
list_decisions
get_validation_results
inspect_branch_state
inspect_integration_queue

```

Avoid requiring ChatGPT to reconstruct operational state by reading arbitrary raw logs unless troubleshooting demands it.

Provide concise structured information first, with deeper evidence available when necessary.

---

# 152. Preserve Owner Confirmation Boundaries

Not every ChatGPT recommendation should immediately become an external action.

Define which actions may be performed as ordinary coordination and which require explicit owner approval.

Potential approval-required actions include:

- production deployment;
- destructive remote operation;
- credential changes;
- major Project DNA changes;
- deletion of authoritative state;
- major architecture changes;
- expenditure of external paid resources beyond defined limits.

Routine development task assignment should eventually require much less friction.

Make approval requirements project-configurable.

---

# 153. Implement a Minimal Control Interface

Implement the smallest authenticated interface required to exercise the operations defined above.

This may initially be GitHub-native.

If a custom service is required, keep it narrow.

A first API might conceptually expose:

```
GET  /workers
GET  /tasks
GET  /tasks/{id}
POST /tasks
POST /tasks/{id}/decision
POST /tasks/{id}/cancel

```

Do not implement endpoints merely because they might someday be useful.

Every interface expands the security and maintenance surface.

---

# 154. Authenticate Control-Plane Actions

Control-plane write operations require authenticated identity.

The system must distinguish:

- authorized owner;
- authorized ChatGPT integration;
- coordinator;
- workers;
- unauthenticated clients.

Do not rely on obscurity of an endpoint.

Where GitHub provides the control surface, use GitHub's authentication and authorization mechanisms.

Where a custom service exists, use an established authentication mechanism rather than inventing cryptography.

---

# 155. Audit Control-Plane Changes

Important coordination changes should leave an audit trail.

Record:

- action;
- actor;
- timestamp;
- previous state where useful;
- resulting state;
- related task/project.

Git history may naturally provide much of this for durable Git-based operations.

Do not create redundant audit databases unless required.

The owner should eventually be able to determine:

> Why did this worker start this task?

---

# 156. Implement Decision Round-Tripping

Prove the complete human-decision path.

Test sequence:

1. Worker encounters an authorized decision boundary.
2. Worker creates decision request.
3. ChatGPT can inspect the request.
4. ChatGPT explains it to the owner.
5. Owner selects an option.
6. ChatGPT records the decision through an authenticated operation.
7. Worker detects the answer.
8. Worker verifies task ownership.
9. Codex resumes with the decision.
10. Completion report references the decision.

This is a major requirement for unattended work.

---

# 157. Make Decisions Immutable Historical Records

Once acted upon, a decision should not silently change.

If the owner later changes direction, create a new decision or superseding instruction.

Preserve:

- original question;
- options;
- recommendation;
- owner's answer;
- resulting action.

This prevents later confusion about why implementation took a particular direction.

---

# 158. Design Coordinator Responsibilities

After Git-based multi-worker operation is proven, implement the coordinator only for responsibilities that genuinely benefit from central coordination.

Potential responsibilities:

- worker registry;
- task dispatch;
- leases/claims;
- worker health;
- capability matching;
- transient state;
- event routing;
- stale-task detection;
- notification routing.

The coordinator must not become the sole source of project history or intent.

---

# 159. Keep the Coordinator Replaceable

The coordinator should be reconstructable from durable sources plus currently registered workers.

Do not make a single coordinator database the only location containing:

- task definitions;
- completed reports;
- owner decisions;
- Project DNA;
- source history.

If the coordinator is destroyed, Mission Control should be able to rebuild it.

Transient leases and heartbeats may legitimately be lost and reconstructed.

---

# 160. Design Coordinator Persistence

Some coordinator state may require local persistence.

Classify every field.

For example:

```
worker registry          reconstructable
current heartbeat       ephemeral
task definition         Git authoritative
lease                    ephemeral/recoverable
completion report       Git authoritative
owner decision          durable
notification delivery   operational

```

Choose persistence technology only after the required semantics are clear.

A simple SQLite database may be entirely sufficient initially.

Do not deploy a distributed database without demonstrated need.

---

# 161. Design Coordinator Recovery

The coordinator must tolerate restart or replacement.

Recovery should approximately:

```
start
  ↓
load configuration
  ↓
inspect durable task state
  ↓
inspect worker registrations
  ↓
expire uncertain leases
  ↓
request fresh worker heartbeats
  ↓
reconcile active tasks
  ↓
resume dispatch

```

Do not assume an active task is abandoned merely because the coordinator rebooted.

Worker/task ownership protocols must handle uncertainty safely.

---

# 162. Implement Worker Registration

Workers should register with the coordinator when available.

Registration should provide:

```
worker_id
authenticated_identity
platform_version
capabilities
resource_summary
current_state

```

The coordinator must authenticate worker identity.

Registration does not replace enrollment.

Enrollment establishes trust.

Registration announces presence.

---

# 163. Implement Heartbeats Outside Git

Once a coordinator exists, move high-frequency heartbeat information out of Git.

Workers can periodically report:

```
worker_id
state
current_task
timestamp
resource_summary

```

Heartbeat frequency should balance:

- failure-detection speed;
- network traffic;
- unnecessary activity.

Seconds-level precision is unlikely to be necessary for development workers.

---

# 164. Define Worker Offline Semantics

A missing heartbeat does not automatically mean a worker's task can be reassigned immediately.

The worker may have:

- lost network access;
- rebooted;
- lost coordinator connectivity while still modifying a workspace.

Define states such as:

```
ONLINE
DEGRADED
SUSPECT
OFFLINE

```

Use lease/ownership rules to determine when reassignment is safe.

Avoid two workers continuing the same exclusive task after a temporary partition.

---

# 165. Design Task Leases

If the coordinator uses leases, specify:

- lease owner;
- lease duration;
- renewal;
- expiration;
- recovery;
- remote authoritative relationship.

A worker that loses its lease must not continue publishing exclusive task changes indefinitely.

Network partitions require conservative behavior.

Do not build lease semantics casually; they are a distributed-systems correctness boundary.

---

# 166. Prefer Safety Over Maximum Utilization

Development workers do not require millisecond-level failover.

When ownership is uncertain, waiting is preferable to duplicate conflicting implementation.

The platform should optimize for:

1. preserving authoritative work;
2. avoiding conflicting ownership;
3. recoverability;
4. useful throughput.

Maximum machine utilization is secondary.

---

# 167. Implement Capability Matching

When ChatGPT or the owner has not explicitly selected a worker, the coordinator may choose one.

Matching should consider declared task requirements.

Examples:

```
requires:
  - docker
  - ddev
  - drupal

minimum_ram_gb: 16

```

Possible later considerations:

- current load;
- cached project environment;
- historical reliability;
- expected task weight.

Keep initial selection deterministic and understandable.

---

# 168. Respect Explicit Assignments

An explicit valid worker assignment overrides ordinary automatic capability selection.

The coordinator should verify that the selected worker can satisfy hard requirements.

If not, report the incompatibility instead of silently rerouting the task unless policy explicitly permits rerouting.

This preserves ChatGPT's role as the higher-level coordinator.

---

# 169. Add Priority Scheduling

Tasks should support priority.

Start with a small understandable set, for example:

```
CRITICAL
HIGH
NORMAL
LOW

```

Do not create dozens of priority levels.

Dependencies and explicit assignment may constrain scheduling more strongly than priority.

A high-priority blocked task should not prevent unrelated runnable work unless policy requires it.

---

# 170. Add Task Dependencies

Allow tasks to declare dependencies.

For example:

```
TASK-204 depends_on:
  - TASK-201
  - TASK-203

```

A task should not become runnable until required dependencies reach acceptable states.

Do not infer complex dependencies solely from task descriptions when they can be declared explicitly.

Detect dependency cycles and report them.

---

# 171. Add Project Concurrency Rules

Projects may need limits on simultaneous work.

Examples:

- only one database-schema migration task at a time;
- many documentation tasks may run concurrently;
- theme and backend work may proceed independently;
- integration tasks may require exclusive ownership.

Allow projects or task types to declare concurrency constraints.

Avoid global serialization of all work.

Parallelism is one of the platform's intended benefits.

---

# 172. Implement Stale-Task Detection

Detect tasks that appear stuck.

Potential signals:

- active task with no worker heartbeat;
- worker alive but no task progress for an unusual duration;
- repeated identical failure;
- expired lease;
- unresolved decision;
- local commit never pushed.

Do not automatically classify long-running work as failed solely because it takes time.

Stale detection should surface investigation, not destroy work.

---

# 173. Track Useful Progress

Avoid measuring worker productivity solely by elapsed time or token consumption.

Useful progress signals may include:

- commits;
- validation milestones;
- task-state transitions;
- checkpoint reports;
- resolved blockers.

The platform should not pressure Codex into meaningless commits merely to appear active.

Progress tracking exists for recovery and coordination, not surveillance theater.

---

# 174. Implement Coordinator Notifications

Connect coordinator events to at least one practical notification channel.

The first channel should prioritize reliability and phone accessibility.

Important events include:

```
HUMAN_DECISION_REQUIRED
TASK_COMPLETED
TASK_FAILED
WORKER_OFFLINE
SECURITY_RELEVANT_FAILURE

```

Do not notify the owner for every routine heartbeat or Git fetch.

Notification policy should prevent alert fatigue.

---

# 175. Implement Notification Deduplication

Repeated polling or retries must not generate repeated identical notifications.

Track notification state sufficiently to prevent messages such as:

```
TASK-204 is blocked

```

being sent every minute.

A meaningful state change may justify another notification.

For example:

```
BLOCKED → RESUMED → BLOCKED

```

can legitimately produce a new alert.

---

# 176. Design Daily Operation

Define what normal unattended operation looks like.

Example:

```
workers boot
   ↓
supervisors start
   ↓
coordinator registers workers
   ↓
tasks become available
   ↓
workers execute
   ↓
checkpoints become durable
   ↓
completed work is reported
   ↓
workers take additional work
   ↓
Codex capacity becomes unavailable
   ↓
affected workers preserve state and wait
   ↓
capacity returns
   ↓
work resumes

```

The owner should not need to restart this cycle manually each morning.

---

# 177. Design Capacity-Reset Resumption

One of the intended operating modes is to allow workers to perform useful Codex work until usage capacity is exhausted and resume when capacity becomes available again.

Implement this only using behavior actually supported and observed from Codex.

The system should:

- preserve active work before waiting;
- avoid wasteful repeated requests;
- distinguish capacity limits from authentication failures;
- periodically re-evaluate availability where appropriate;
- revalidate task ownership before resuming;
- continue queued work after recovery.

Do not attempt to bypass or evade service usage limits.

The platform automates legitimate resumption when service becomes available.

---

# 178. Design Overnight and Unattended Operation

Workers should safely operate when no human is immediately available.

Tasks requiring human judgment should stop at a safe boundary.

Tasks not requiring human judgment may continue.

The system should therefore distinguish:

```
can_continue_unattended: true

```

from work requiring approval.

Do not allow lack of human response to cause repeated Codex invocations asking the same unresolved question.

---

# 179. Implement Maintenance Windows

Workers eventually need maintenance for:

- OS updates;
- platform updates;
- Docker cleanup;
- reboot;
- filesystem checks.

Maintenance should not interrupt active work without checkpointing.

A worker should transition through a state such as:

```
DRAINING
    ↓
MAINTENANCE
    ↓
READY

```

The coordinator should stop assigning new tasks while a worker drains.

---

# 180. Implement Graceful Worker Shutdown

Before planned shutdown or reboot:

1. stop accepting new assignments;
2. identify active task;
3. request safe checkpoint if appropriate;
4. preserve local operational state;
5. push durable progress where safe;
6. update status;
7. stop Codex;
8. stop supervisor cleanly.

Do not require elaborate shutdown behavior for a completely idle worker.

Unexpected power-loss recovery remains necessary regardless.

---

# 181. Design Worker Replacement

Replacing a worker should be routine.

Procedure:

1. mark old worker retired/revoked;
2. provision replacement from universal installer;
3. enroll new identity;
4. register capabilities;
5. reconstruct required project environments;
6. resume eligible work.

Do not copy the old worker's entire disk as the standard replacement mechanism.

Replacement should prove infrastructure reproducibility.

---

# 182. Design Worker Retirement

Retirement differs from temporary offline status.

Retiring a worker should:

- prevent new assignments;
- resolve active tasks;
- revoke credentials;
- preserve durable reports;
- retain historical worker identity for audit purposes;
- allow local disks to be erased.

Historical reports should continue referencing the retired worker ID.

Do not reuse security identities for replacement machines.

---

# 183. Design Complete Fleet Recovery

Assume every worker is destroyed simultaneously.

The platform must document how to recover.

Required external durable assets may include:

- platform Git repository;
- project Git repositories;
- Project DNA;
- project configuration;
- sanitized development fixtures;
- credential authority/enrollment capability;
- reproducible installer inputs.

Recovery should not depend on any surviving worker disk.

This is a central Mission Control acceptance scenario.

---

# 184. Design Coordinator-Loss Recovery

Assume the coordinator is destroyed while workers and GitHub remain intact.

Document reconstruction.

A replacement coordinator should be able to recover:

- project definitions;
- task definitions;
- completed reports;
- owner decisions;
- known worker identities/configuration where durably stored.

Workers should re-register.

Ephemeral heartbeat and lease information may be reconstructed conservatively.

The coordinator must not be a single point of permanent project-state loss.

---

# 185. Design ChatGPT-Thread Recovery

Assume the current ChatGPT conversation disappears completely.

A new ChatGPT thread should be able to reconstruct project direction by reading authoritative repository documentation.

Provide a canonical start document telling a new coordinating ChatGPT session what to inspect.

It should include pointers to:

- Project DNA;
- architecture;
- current project state;
- active tasks;
- worker state;
- recent reports;
- outstanding decisions;
- integration queue.

The new thread should not require the owner to retell the project's history.

---

# 186. Create the Mission Control Recovery Command

Long term, strive toward a single administrative recovery entry point.

Conceptually:

```
mission-control recover

```

The exact interface may differ.

Its purpose is to reconstruct the operational environment from authoritative state.

It may:

- verify platform installation;
- restore coordinator state;
- discover/enroll available workers;
- synchronize project definitions;
- reconstruct task state;
- identify interrupted work;
- report unresolved conditions.

Do not implement a misleading "one command" wrapper until underlying recovery mechanisms actually work independently.

The command should orchestrate proven recovery procedures, not hide fragile assumptions.

---

# 187. Define the Full Recovery Acceptance Test

The mature platform should eventually pass a destructive end-to-end recovery exercise.

Scenario:

1. Preserve only documented authoritative external state.
2. Destroy coordinator.
3. Destroy worker installations.
4. Start with compatible blank machines.
5. Recreate installation media from version-controlled inputs if necessary.
6. provision workers;
7. enroll new identities;
8. reconstruct coordinator;
9. restore project definitions;
10. reconstruct task state;
11. recreate development environments;
12. identify unfinished work;
13. resume safe tasks;
14. complete a real development assignment;
15. push and verify results.

Success means the development operation has been restored without relying on:

- old terminal sessions;
- old ChatGPT conversation history;
- undocumented local files;
- human recollection of commands.

This is the defining resilience test of Mission Control.

**Pause here. Section 188 should continue with Project DNA restoration, multi-project support, integration/review orchestration, platform self-development, security hardening, release strategy, and the final implementation/acceptance roadmap.**