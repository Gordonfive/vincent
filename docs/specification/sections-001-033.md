# Codex Autonomous Worker Platform

## 1. Mission

Build a reusable platform that turns ordinary computers into dedicated, largely autonomous Codex development workers.

The system should allow the owner to:

- Provision a new worker from a universal Debian installation USB.
- Treat worker machines as disposable infrastructure.
- Run Codex continuously for extended development sessions.
- Assign different workers independent development tasks.
- Coordinate workers primarily through Git.
- Manage priorities and instructions remotely, including from a phone.
- Allow ChatGPT to serve as the high-level planning, coordination, review, and decision layer.
- Preserve completed work, instructions, reports, and project state outside individual workers.
- Recover from destruction or failure of a worker simply by rebuilding it.
- Gradually automate recurring human intervention.

The long-term objective is a small fleet of AI development workers that behaves more like a persistent engineering team than individual interactive Codex sessions.

---

# 2. Core Principles

## Git is authoritative

Durable development state must live in Git whenever practical.

This includes:

- source code;
- infrastructure code;
- worker configuration;
- task assignments;
- worker reports;
- project documentation;
- architecture decisions;
- installation/bootstrap code;
- coordination protocols.

A worker's local filesystem must never be the only location containing valuable completed work.

Workers should commit and push useful work frequently enough that destruction of a worker does not cause significant project loss.

## Workers are disposable

Assume any worker can be erased without warning.

Recovery should consist approximately of:

1. Boot universal installer.
2. Install Debian.
3. Generate worker identity.
4. Authorize worker.
5. Fetch configuration.
6. Install required software.
7. Fetch assigned repositories.
8. Resume work.

Do not design around preserving a particular workstation indefinitely.

## Local execution first

Development grunt work should occur locally on workers whenever practical:

- DDEV;
- Docker;
- Composer;
- Drupal;
- builds;
- tests;
- linting;
- static analysis;
- local databases;
- browser testing;
- integration testing.

Cloud AI inference may remain remote. The worker hardware exists primarily to provide Codex with a persistent development environment and execute its tools.

## Human attention is expensive

Every repetitive manual action should eventually be considered for automation.

The platform should progressively reduce requirements for the owner to:

- sit at a workstation;
- watch terminals;
- restart Codex;
- check whether work finished;
- copy status between workers;
- manually synchronize repositories;
- repeatedly provide identical permissions;
- determine which worker should perform a task.

Human intervention should concentrate on decisions that actually require human judgment.

---

# 3. Initial Hardware Model

Do not require expensive specialized hardware.

Suitable workers may include:

- old workstations;
- spare laptops;
- desktops;
- machines with 16 GB RAM;
- larger workers with 32–64+ GB RAM.

GPU capability is not a platform requirement.

A powerful GPU should not be assumed because Codex model inference occurs remotely unless a future component explicitly introduces local AI inference.

Important local resources are approximately:

1. RAM
2. storage performance
3. CPU
4. network reliability

SATA SSDs are acceptable.

NVMe is preferable but not required.

A 16 GB laptop should remain a supported worker class, although simultaneous Docker/DDEV environments may need to be limited.

A larger 32–64 GB workstation can operate as a heavy worker capable of running more simultaneous containers, builds, tests, or independent workspaces.

---

# 4. Operating System

Initial target:

**Debian 13**

Workers should preferably be dedicated systems rather than general-purpose personal workstations.

The platform should support headless operation.

Normal operation must not require a monitor, keyboard, or mouse.

SSH may exist for maintenance and emergency access, but SSH should not be the primary user interface for assigning routine work.

---

# 5. Universal Installation USB

Create a reproducible Debian installation mechanism capable of turning an arbitrary compatible computer into a Codex worker.

Use Debian's supported unattended installation/provisioning mechanisms where practical.

The installer should automate as much as reasonably possible, including:

- disk partitioning;
- Debian installation;
- networking;
- package installation;
- creation of the worker service account;
- Git;
- GitHub CLI where useful;
- Docker;
- DDEV;
- development dependencies;
- Codex installation;
- worker bootstrap software;
- worker supervisor;
- system services;
- automatic startup;
- logging.

The same USB image should be usable for multiple workers.

Do **not** create a separate permanent installer image for every machine unless technically necessary.

---

# 6. Worker Identity

The universal installer must not contain the permanent identity of a particular worker.

During first boot/provisioning, the worker should generate its own identity.

At minimum, investigate generating a unique SSH keypair.

For example:

```
worker-01
worker-02
worker-heavy-01

```

The exact naming mechanism can evolve.

The system should provide an easy method for the owner to authorize a newly created worker from another device, ideally a phone.

The worker should display or otherwise expose:

- worker identifier;
- public key;
- fingerprint;
- authorization request.

Once approved, the worker becomes an authorized participant in the platform.

---

# 7. Credential Architecture

Do not embed the owner's personal GitHub credentials in the universal USB image.

Do not store unrestricted long-lived credentials in Git.

Separate:

**bootstrap identity**

from:

**operational authorization**

The initial implementation should investigate GitHub deploy keys for repository-specific access.

A deploy key consists of:

- a private SSH key stored by the worker;
- the corresponding public key registered with a GitHub repository.

This permits repository access without granting the worker the owner's entire GitHub identity.

Where practical:

- each worker should have its own identity;
- credentials should be independently revocable;
- compromise/destruction of one worker should not require rotating every worker;
- privileges should be sufficient for autonomous work but not unnecessarily account-wide.

Longer term, evaluate GitHub Apps and short-lived credentials if they materially improve the system.

Do not overengineer credential infrastructure during the first prototype.

---

# 8. Infrastructure Repository

Create a dedicated repository for the worker platform itself.

Do not bury the worker infrastructure inside the Ketchikan.net Drupal application repository.

A possible repository name is:

```
codex-worker-platform

```

The repository should contain infrastructure such as:

```
README.md
AGENTS.md
docs/
installer/
bootstrap/
worker/
coordinator/
services/
scripts/
config/
examples/
tests/

```

The exact structure should be selected during implementation and documented.

Git must remain authoritative for the platform.

---

# 9. Worker Configuration

After authorization, a worker should fetch its configuration from Git or another controlled configuration source.

Configuration should describe capabilities rather than requiring every worker to be identical.

Example capabilities might include:

```
docker
ddev
drupal
php
node
browser-testing
heavy-build
general-development

```

Potential machine information:

```
worker_id
hostname
architecture
cpu_count
ram
storage
capabilities
assigned_role

```

Do not store secrets directly in ordinary configuration files committed to Git.

---

# 10. Git-Based Task Coordination

The first production-quality coordination mechanism should deliberately remain simple.

Workers should be capable of polling Git for new instructions.

Conceptual cycle:

```
synchronize
    ↓
inspect assignment
    ↓
determine whether new work exists
    ↓
execute Codex task
    ↓
test
    ↓
commit useful work
    ↓
push
    ↓
write report/status
    ↓
synchronize
    ↓
wait

```

The polling interval should be configurable.

A simple timer or service is acceptable initially.

Do not build a complex distributed queue before proving that Git-based coordination is insufficient.

---

# 11. Task Files

Develop a machine-readable but human-friendly task format.

A task should be capable of specifying:

- task ID;
- project;
- repository;
- branch/worktree strategy;
- worker or required capability;
- objective;
- constraints;
- acceptance criteria;
- dependencies;
- forbidden actions;
- completion behavior.

Example concept:

```
tasks/
    queued/
    active/
    blocked/
    completed/

```

Exact implementation is left to engineering evaluation.

The protocol must prevent two workers from accidentally believing they exclusively own the same mutable work.

Task ownership/claiming therefore needs explicit semantics.

---

# 12. Worker Reports

Workers must report what they did.

Reports should include at least:

- worker ID;
- task ID;
- start state;
- branch;
- relevant starting commit;
- changes made;
- tests performed;
- test results;
- resulting commits;
- push status;
- unresolved problems;
- questions requiring human decisions;
- final state.

Reports should be durable and accessible remotely.

A completed task should not merely disappear from the queue.

---

# 13. Codex Execution

The platform should provide a supervisor around Codex rather than relying indefinitely on manually opened interactive terminals.

Investigate the officially supported Codex interfaces available at implementation time and use supported automation mechanisms rather than brittle terminal keystroke automation whenever possible.

The supervisor eventually needs to distinguish:

```
IDLE
STARTING
WORKING
TESTING
BLOCKED
WAITING_FOR_HUMAN
COMPLETED
FAILED
USAGE_LIMITED

```

Do not assume Codex can automatically resume after every possible usage-limit condition. Determine actual supported behavior and document it.

Where supported and permitted, the platform should resume queued work after capacity becomes available.

---

# 14. Remote Management

The owner should not need to SSH into workers during normal operation.

Primary interaction should eventually be possible from a phone.

The desired workflow is:

```
Owner
  ↓
ChatGPT
  ↓
project/task instructions
  ↓
Git/coordinator
  ↓
workers
  ↓
commits + reports + questions
  ↓
ChatGPT
  ↓
Owner

```

SSH remains an administrative fallback.

---

# 15. ChatGPT's Role

ChatGPT should function as the high-level coordinator.

Its responsibilities may include:

- translating owner objectives into implementation tasks;
- determining task priority;
- preparing worker instructions;
- reviewing worker reports;
- examining Git state;
- identifying dependencies;
- detecting conflicts;
- recommending which worker should handle work;
- determining whether acceptance criteria were satisfied;
- preparing follow-up assignments;
- presenting questions requiring owner decisions.

The platform must not assume ChatGPT has direct interactive control over a workstation unless an actual supported interface exists.

Git, GitHub APIs, services, or another explicit integration layer should bridge that gap.

---

# 16. Phone-First Operation

The platform should be designed so that routine coordination can eventually happen entirely from the ChatGPT mobile application or another simple mobile interface.

Desired example:

Owner tells ChatGPT:

> Have the theme worker finish the navigation and have the backend worker begin the events ingestion system.

The coordination layer should eventually translate that into durable assignments.

Workers should discover those assignments without the owner connecting to either computer.

Results should return through Git/status infrastructure so ChatGPT can inspect them.

Questions that require human decisions should be surfaced remotely.

---

# 17. Notifications

Workers should eventually support notifications for important events.

Examples:

- task completed;
- task failed;
- human decision required;
- credentials expired;
- worker offline;
- tests failing;
- usage/capacity limit encountered;
- worker resumed;
- deployment verification failed.

Notification transport should be modular.

Possible transports can be evaluated later rather than hard-coded into the initial architecture.

Local audible completion notifications may also be useful when the owner is physically near the worker.

---

# 18. Multiple Workers

The architecture must assume multiple simultaneous workers.

Example:

```
worker-heavy-01
    Drupal/backend/integration

worker-02
    theme/frontend

worker-03
    tests/QA/documentation

```

Each worker should preferably have an independent:

- checkout/worktree;
- DDEV project;
- containers;
- branch/task;
- status.

Workers must not share a mutable Drupal working directory.

They may work against the same Git repository using coordinated branches.

---

# 19. Independent Local Drupal Environments

For the Ketchikan.net project specifically, different workers may need independent Drupal installations.

This allows the owner to inspect, for example:

- theme progress independently;
- functional/backend progress independently;
- integration progress independently.

DDEV projects must therefore use unique project names and avoid port/container/database collisions.

Do not design worker coordination around one shared Drupal installation.

---

# 20. Branch and Integration Strategy

Git coordination must explicitly address parallel workers.

A reasonable starting model is:

```
authoritative integration branch
         ↑
    reviewed work
      ↑       ↑
 worker A   worker B
   branch     branch

```

Workers should not blindly push competing changes directly into the same branch.

The platform should eventually support:

- task branches;
- clean worktrees;
- synchronization before work;
- conflict detection;
- review/integration gates;
- reporting resulting commit hashes.

Exact policy can be adapted to each project.

---

# 21. Worker Lifecycle

Target lifecycle:

## Provision

Universal USB installs Debian and worker software.

## Identify

Worker generates unique identity.

## Authorize

Owner approves the identity.

## Configure

Worker obtains authorized configuration.

## Register

Worker announces its capabilities.

## Idle

Worker waits for work.

## Claim

Worker safely claims an eligible task.

## Execute

Codex performs the assignment.

## Validate

Worker executes required tests.

## Publish

Worker commits and pushes durable results.

## Report

Worker publishes status/report.

## Continue

Worker checks for another assignment.

## Recover

Following failure/reinstallation, the worker reconstructs state from authoritative external sources.

---

# 22. Safety Model

These machines are intended to be dedicated disposable Codex workers.

Therefore, it is acceptable for Codex to have broad authority on the dedicated worker when necessary for effective autonomous operation.

The objective is not to protect the disposable OS installation from Codex.

The important boundaries are external.

Codex must not accidentally:

- modify unrelated production systems;
- modify repositories outside its authorization;
- leak credentials;
- commit secrets;
- overwrite another worker's work;
- deploy to production without authorization;
- destroy authoritative remote state.

A worker destroying its own local OS is an inconvenience.

A worker destroying authoritative external state is a platform failure.

Design protections accordingly.

---

# 23. Reproducibility

Manual changes to a worker should be considered technical debt.

If a change is necessary to make a worker function correctly, encode that change into:

- installer;
- bootstrap scripts;
- configuration management;
- platform documentation;

so the next rebuild includes it automatically.

The test of the platform is not:

> Does this worker work?

It is:

> Can we destroy this worker, reinstall it, and automatically recreate a working replacement?

---

# 24. Observability

Provide simple methods to determine:

- which workers exist;
- whether they are online;
- current task;
- current repository;
- current branch;
- last activity;
- last successful push;
- task state;
- Codex state;
- errors;
- available capabilities.

Start with Git-based status if appropriate.

A web dashboard can come later.

---

# 25. Phase 0 — Architecture Prototype

Codex should begin by creating the infrastructure repository and documenting the proposed implementation.

Deliverables:

- repository structure;
- architecture document;
- threat/credential model;
- worker lifecycle;
- task schema;
- worker status schema;
- branch/claiming protocol;
- bootstrap design;
- Debian unattended installation strategy;
- Codex automation-interface investigation;
- minimal proof-of-concept plan.

Do not begin with a sophisticated dashboard.

Do not begin with Kubernetes.

Do not begin with a custom distributed scheduler.

Prove the basic worker loop first.

---

# 26. Phase 1 — First Disposable Worker

Use the older high-memory workstation as the initial test bed.

Goal:

> Completely erase the machine and reconstruct a functional Codex worker using the documented process.

Acceptance criteria:

- Debian 13 installed;
- network functional;
- Git functional;
- Docker functional;
- DDEV functional;
- Codex functional;
- worker identity generated;
- authorization mechanism demonstrated;
- private repository access demonstrated;
- worker software automatically starts;
- worker can receive a test assignment;
- Codex can execute it;
- worker can commit/push results;
- worker produces a completion report.

---

# 27. Phase 2 — Universal Installer

Create the reusable installation USB/image.

Acceptance test:

1. Wipe test workstation.
2. Boot installer.
3. Perform unattended installation.
4. Complete worker authorization.
5. Allow provisioning to finish.
6. Assign test task remotely.
7. Verify completion without locally configuring the machine by hand.

Document every unavoidable manual action.

Then determine whether that action can be eliminated.

---

# 28. Phase 3 — Second Worker

Provision another computer using the same installer.

Preferably use a lower-resource laptop with approximately 16 GB RAM.

Prove that:

- one installer supports heterogeneous hardware;
- workers receive unique identities;
- both can access required repositories;
- each has independent workspaces;
- both can work simultaneously;
- task claiming prevents duplication;
- their DDEV environments do not interfere;
- their commits can be integrated cleanly.

---

# 29. Phase 4 — Remote Coordination

Implement the first phone-friendly coordination workflow.

Initially, GitHub may itself serve as the control plane.

Possible mechanisms include:

- task files;
- issues;
- pull requests;
- GitHub API;
- GitHub App.

Choose the simplest mechanism that provides reliable operation.

The owner should be able to create/change work remotely without connecting directly to workers.

---

# 30. Phase 5 — Coordinator

Only after multiple workers are proven should a coordinator be introduced.

Coordinator responsibilities may include:

- worker registry;
- capability matching;
- task assignment;
- dependency tracking;
- conflict prevention;
- health checking;
- stale-task detection;
- human-question routing;
- status summaries.

Keep Git authoritative for durable development artifacts even if the coordinator maintains transient operational state.

---

# 31. Phase 6 — Self-Improving Operations

Track repeated human interventions.

Examples:

```
"I have manually restarted this three times."

"I repeatedly have to tell workers to fetch before starting."

"I repeatedly copy completion reports into ChatGPT."

```

These should become platform improvement candidates.

The system should progressively automate recurring operational work.

---

# 32. Explicit Non-Goals for Initial Implementation

Do not initially build:

- Kubernetes cluster;
- complex distributed database;
- custom AI model;
- local LLM infrastructure;
- elaborate web dashboard;
- centralized secrets platform unless actually needed;
- custom replacement for Git;
- complex scheduler;
- fully autonomous production deployment.

Prefer boring, understandable components.

---

# 33. Initial Technology Bias

Prefer established tools where they solve the problem adequately:

- Debian 13
- systemd
- Git
- GitHub
- SSH keys/deploy keys
- Docker
- DDEV
- shell/Python where appropriate
- supported Codex automation interfaces

A new custom service should require justification.

---

