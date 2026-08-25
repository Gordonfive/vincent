# 238. Stop Architecture Expansion at the Appropriate Point

The specification must eventually transition from design to implementation.

Do not continue inventing subsystems merely because additional automation is conceivable.

New platform features should require one of:

- an existing requirement;
- a demonstrated operational problem;
- a recovery deficiency;
- a security requirement;
- a meaningful reduction in recurring human coordination.

The initial platform should remain understandable by one owner and maintainable with Codex assistance.

Complexity is a cost.

---

# 239. Establish the Implementation Order

Unless testing reveals a dependency requiring adjustment, implement in this order:

```
1. Project DNA and repository foundation
2. Protocol definitions
3. Codex interface validation
4. Worker supervisor prototype
5. First physical worker
6. Failure/recovery testing
7. Universal installer
8. Second heterogeneous worker
9. Parallel task coordination
10. Phone-accessible control plane
11. Coordinator
12. Multi-project support
13. Mission Control self-hosting
14. Full destructive recovery

```

Do not implement later layers merely to avoid completing difficult validation of earlier layers.

---

# 240. Define Milestone Gates

Each major phase must have an explicit acceptance gate.

Suggested milestones:

```
M0 — Architecture accepted
M1 — First autonomous worker
M2 — Recovery proven
M3 — Universal installer proven
M4 — Two-worker coordination proven
M5 — Phone-first control proven
M6 — Coordinator proven
M7 — Multi-project operation proven
M8 — Full Mission Control recovery proven

```

A milestone is complete only when its acceptance evidence is committed and pushed.

---

# 241. Maintain an Implementation Roadmap

Create a durable roadmap showing:

- milestone;
- work item;
- status;
- dependencies;
- acceptance criteria;
- relevant commits/reports.

The roadmap should describe current implementation reality rather than becoming a speculative feature wish list.

Keep future ideas separately when necessary.

A new coordinating session should be able to determine the next unfinished implementation step quickly.

---

# 242. Keep Work Items Small Enough to Recover

Implementation tasks should normally represent coherent units that can be:

- assigned;
- understood;
- validated;
- reviewed;
- checkpointed;
- resumed.

Avoid enormous assignments such as:

> Build Mission Control.

Prefer bounded work such as:

> Implement and test worker task-state parsing according to protocol version 1.

The coordinator may group related tasks into milestones without making individual tasks unmanageably large.

---

# 243. Prioritize Foundational Correctness

During early implementation, prioritize:

1. Git correctness;
2. recovery;
3. task ownership;
4. credential boundaries;
5. deterministic provisioning;
6. observability;
7. convenience.

A polished phone interface built on unreliable task ownership is not progress toward the mission.

The platform's value depends on trusting it while unattended.

---

# 244. Prefer Proven Components

Before implementing a custom component, determine whether a maintained standard tool already solves the problem.

Use standard:

- Git;
- systemd;
- SSH;
- Debian provisioning;
- Docker;
- GitHub authentication;
- structured serialization;
- operating-system logging.

Custom code should primarily connect these components and encode Mission Control-specific behavior.

Do not recreate general infrastructure unnecessarily.

---

# 245. Avoid Premature Cloud Dependence

The platform may use cloud services where they provide real value, particularly:

- GitHub;
- Codex/OpenAI;
- notifications;
- optional control-plane hosting.

However, the worker architecture should not require a large cloud infrastructure deployment merely to coordinate a few local computers.

Start with the smallest external footprint that satisfies remote operation.

A future hosted coordinator can be introduced when justified.

---

# 246. Preserve Linux-First Design

The primary worker platform is Linux-first.

Debian 13 is the initial reference operating system.

Do not compromise the core architecture merely to achieve immediate Windows compatibility.

Future support for:

- Ubuntu;
- other Debian-derived distributions;
- Windows;
- macOS;

may be evaluated later.

Cross-platform abstractions should only be introduced when another platform is actually being supported.

---

# 247. Preserve Open-Source Suitability

The platform should be designed so its generic implementation can be open sourced.

Do not embed:

- private project secrets;
- owner-specific credentials;
- private infrastructure assumptions;
- Ketchikan.net-specific logic;

into the reusable core.

Private configuration can live separately.

The generic platform should eventually be usable by another developer with their own GitHub account, projects, and workers.

---

# 248. Separate Generic Platform from Owner Configuration

Maintain a clear boundary between reusable software and installation-specific configuration.

Conceptually:

```
Mission Control platform
          +
owner/fleet configuration
          +
project configuration

```

The platform repository may contain safe examples and schemas.

Sensitive owner-specific configuration should use an appropriate private mechanism.

Do not require forking platform source merely to add another worker or project.

---

# 249. Document Licensing Before Public Release

Before publishing the platform as open source:

- choose an appropriate license;
- verify dependencies are compatible;
- remove private configuration;
- inspect Git history for secrets;
- document installation requirements.

Do not delay prototype development solely to settle every public-release detail.

Licensing becomes a gate before public release, not before experimentation.

---

# 250. Define Minimum Viable Mission Control

The minimum viable system is achieved when:

- one generic Linux worker can be provisioned reproducibly;
- it can enroll securely;
- it can receive a remote task;
- Codex can execute the task;
- deterministic validation can run;
- useful work is committed and pushed;
- completion is reported;
- interruption can be recovered;
- a second worker can operate independently;
- the owner can assign work remotely without SSH.

A custom dashboard is not required.

A sophisticated scheduler is not required.

Production deployment automation is not required.

---

# 251. Define Mission Control 1.0

Mission Control 1.0 should additionally demonstrate:

- multiple workers;
- multiple projects;
- capability-based and explicit assignment;
- durable decisions;
- integration/review workflow;
- coordinator recovery;
- worker replacement;
- reproducible installer;
- documented security boundaries;
- phone-first operation;
- complete recovery documentation;
- successful destructive recovery test.

Version 1.0 should represent an operationally trustworthy development system, not merely a prototype with many features.

---

# 252. Define What 1.0 Does Not Promise

Mission Control 1.0 does not need to promise:

- zero human decisions;
- infinite autonomous operation;
- autonomous production changes;
- support for every operating system;
- support for every source-control provider;
- massive worker fleets;
- local AI inference;
- perfect recovery from compromised external authorities;
- elimination of Codex service limits.

State limitations explicitly.

Reliable bounded automation is preferable to exaggerated autonomy claims.

---

# 253. Establish the Owner's Emergency Stop

The owner must always have a straightforward method to stop autonomous work.

The stop mechanism should be capable of preventing:

- new task assignment;
- new Codex invocation;
- integration;
- deployment actions.

An emergency stop should not destroy existing work.

Workers should checkpoint or preserve state where possible.

The stop mechanism must not depend exclusively on reaching each physical worker.

---

# 254. Establish Safe Global Pause

Mission Control should support a durable global state conceptually equivalent to:

```
RUNNING
PAUSED

```

When paused:

- no new ordinary tasks begin;
- active work follows documented pause/checkpoint policy;
- workers remain observable;
- recovery/administrative operations remain possible.

This provides a simple control when the owner wants the entire AI workforce to stop without shutting down machines.

---

# 255. Preserve Human Judgment as a Permanent Principle

Mission Control exists to remove repetitive coordination, not to remove human authority.

Automation should increasingly handle:

- synchronization;
- provisioning;
- task dispatch;
- testing;
- reporting;
- recovery;
- routine integration where authorized.

Humans remain responsible for decisions involving:

- product purpose;
- major priorities;
- acceptable risk;
- consequential external actions;
- significant changes in project philosophy.

The system should make human judgment more effective by reducing operational noise.

---

# 256. Final System Principle

The central design rule is:

> **Git restores the work. Project DNA restores the intent. Mission Control restores the operation.**

A worker is replaceable.

A coordinator is replaceable.

A workstation is replaceable.

A Codex session is replaceable.

A ChatGPT thread is replaceable.

The durable system must preserve enough authoritative information that replacing any of these does not require reconstructing the project from memory.

---

# 257. First Codex Execution Directive

When this specification is first handed to Codex, Codex must **not attempt to implement Sections 1–256 in one operation**.

Treat this document as the product and architecture specification.

Begin with Phase 0 only.

The first implementation cycle is:

1. Read the complete specification.
2. Identify contradictions, technically obsolete assumptions, and unresolved decisions.
3. Verify current Codex and GitHub capabilities against official documentation where necessary.
4. Establish the platform repository.
5. Create Project DNA.
6. Create the architecture package required by Section 92.
7. Create the implementation roadmap.
8. Commit and push all Phase 0 work.
9. Produce a Phase 0 report.
10. Stop for architectural review.

Do not provision or erase physical hardware during this first assignment.

---

# 258. Required First Codex Report

At the end of the first assignment, report:

```
repository
branch
starting_commit
ending_commit
files_created
architecture_decisions
assumptions_verified
assumptions_rejected
unresolved_questions
security_decisions
proposed_phase_1_plan
validation_performed
push_status

```

Explicitly identify any part of this specification that current technology makes impractical or unnecessary.

Do not silently reinterpret the specification to fit implementation preferences.

Recommend changes where appropriate.

---

# 259. Initial Human Review

After Codex completes Phase 0, the owner and ChatGPT should review:

- whether the architecture still matches the mission;
- whether Codex discovered better supported mechanisms;
- whether credential enrollment is practical;
- whether the task protocol is unnecessarily complex;
- whether Git is being used appropriately;
- whether the coordinator is being introduced too early;
- whether recovery remains central;
- whether the proposed Phase 1 test is safe.

Revise the specification or Project DNA when justified.

Then explicitly authorize Phase 1.

---

# 260. Final Build Instruction

Build this platform incrementally.

At every stage:

```
design
  ↓
implement
  ↓
test
  ↓
deliberately break
  ↓
recover
  ↓
document
  ↓
commit
  ↓
push
  ↓
review
  ↓
continue

```

Do not optimize for the appearance of autonomy.

Optimize for a system the owner can actually trust enough to leave running unattended.

The ultimate test is simple:

> The owner should be able to leave the building with only a phone, continue directing software development through ChatGPT, allow remote Codex workers to perform the implementation, and return later knowing that useful work, decisions, failures, and recovery state have all been preserved durably.

When that is possible without depending on a particular workstation, terminal session, Codex instance, ChatGPT thread, or human memory, Mission Control has achieved its purpose.

**End of specification.**