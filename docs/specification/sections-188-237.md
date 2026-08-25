# 188. Restore Project DNA During Recovery

Recovery is incomplete if only source code is restored.

For every managed project, Mission Control must identify and expose its Project DNA before new autonomous development begins.

A recovered environment should answer:

- what the project is;
- its purpose;
- current product philosophy;
- architectural principles;
- authority boundaries;
- prohibited actions;
- current priorities.

Workers must not begin making significant product decisions merely because repositories are technically accessible.

Intent is part of recoverable project state.

---

# 189. Define a Standard Project Manifest

Create a standard manifest describing a project to Mission Control.

Conceptually:

```
project_id
name
repository
project_dna
integration_branch
task_location
report_location
development_environment
required_capabilities
production_policy

```

Additional project-specific configuration may be referenced rather than embedded.

The manifest should allow Mission Control to discover how a project operates without hard-coded knowledge.

---

# 190. Support Multiple Repositories Per Project

Some projects may eventually span multiple repositories.

The project model should permit:

```
project
  ├── application repository
  ├── infrastructure repository
  ├── documentation repository
  └── fixture/data repository

```

Do not require multiple repositories when one is sufficient.

A task must clearly identify which repositories it is authorized to modify.

Cross-repository tasks should have explicit coordination semantics.

---

# 191. Support Multiple Projects

Mission Control must be capable of managing several projects simultaneously.

Potential examples include:

```
Ketchikan.net
OceanMail
BEMPIC
Mission Control itself

```

Each project should independently define:

- Project DNA;
- repositories;
- integration policy;
- development environment;
- task queue;
- production boundary;
- required capabilities.

Do not allow one project's assumptions to become global defaults accidentally.

---

# 192. Define Project Activation

Not every configured project needs to be actively consuming workers.

Support states conceptually similar to:

```
ACTIVE
PAUSED
MAINTENANCE
ARCHIVED

```

A paused project should retain all durable state while receiving no ordinary autonomous work.

This permits deliberate concentration of Codex capacity.

---

# 193. Define Cross-Project Priority

When multiple projects are active, the owner or ChatGPT may need to prioritize between them.

Provide an understandable project-level priority mechanism.

Task priority should still exist within each project.

Avoid creating an opaque mathematical scheduler.

Explicit owner direction must be able to override ordinary scheduling.

---

# 194. Define Capacity Allocation

Codex usage capacity may become a more significant constraint than worker hardware.

Mission Control should eventually be capable of allocating available work intelligently.

Examples:

- prioritize critical project work;
- pause low-priority projects;
- avoid spending capacity repeatedly on blocked tasks;
- assign non-Codex local tests while AI capacity is unavailable.

Do not attempt to evade service limits.

Optimize legitimate use of available capacity.

---

# 195. Distinguish AI Work from Local Work

Not every task step requires Codex.

The supervisor should eventually distinguish:

```
AI_REQUIRED

```

from:

```
LOCAL_AUTOMATION

```

Examples of local automation:

- Git synchronization;
- deterministic builds;
- unit tests;
- integration tests;
- fixture restoration;
- linting;
- environment health checks.

Do not consume Codex capacity for deterministic operations the supervisor can perform directly.

---

# 196. Minimize Unnecessary Codex Context

When invoking Codex, provide the context required to perform the task without repeatedly forcing it to rediscover the entire project.

Useful context may include:

- task;
- Project DNA references;
- repository instructions;
- relevant architecture;
- current branch;
- acceptance criteria;
- prior blocker resolution.

Do not indiscriminately inject enormous documentation sets into every invocation.

Provide discoverable canonical documentation and allow Codex to inspect additional material when required.

---

# 197. Preserve Repository-Level Agent Instructions

Projects should maintain repository-local instructions for Codex.

`AGENTS.md` or the currently supported equivalent should describe:

- repository boundaries;
- development commands;
- testing;
- forbidden operations;
- project-specific Git policy;
- important documentation.

Mission Control task instructions supplement these files rather than duplicating the entire repository handbook.

---

# 198. Design Integration Queue

Completed worker branches requiring review should enter an explicit integration state.

Possible lifecycle:

```
IMPLEMENTATION_COMPLETE
        ↓
READY_FOR_REVIEW
        ↓
REVIEWING
        ↓
CHANGES_REQUESTED
     or
APPROVED
        ↓
INTEGRATED

```

Do not treat worker completion as synonymous with integration.

---

# 199. Define Review Authority

Projects should define who or what can approve integration.

Possible policies:

```
HUMAN_ONLY
CHATGPT_REVIEW
CODEX_REVIEW_PLUS_CHATGPT
AUTOMATED_FOR_LOW_RISK

```

Initial important projects should use conservative review policies.

Automated tests may prove technical correctness but cannot always prove product correctness.

---

# 200. Support Independent Review

Where useful, review should be performed by a different Codex context or worker than the implementation.

Independent review may detect:

- misunderstood requirements;
- missing tests;
- unintended changes;
- architecture violations;
- security problems.

Do not require independent AI review for every trivial change if the cost exceeds its value.

Make review requirements risk-based.

---

# 201. Define Review Reports

Review output should be durable.

A review report should include:

```
task
implementation_commit
reviewer
findings
validation
required_changes
recommendation

```

Use severity or disposition categories that are simple and consistent.

Do not allow review feedback to exist only in transient conversation.

---

# 202. Implement Changes-Requested Flow

When review rejects an implementation:

1. preserve review findings;
2. return the task to an appropriate worker;
3. provide exact findings;
4. preserve existing branch history;
5. implement corrections;
6. rerun validation;
7. submit a new review state.

Do not create a completely new task unless the scope materially changed.

---

# 203. Define Integration Verification

After integration, verify the resulting integration branch.

A branch that individually passed tests before merging may fail after combination with other work.

Run appropriate post-integration validation.

Record:

```
integrated_commit
source_task
source_commit
integration_validation

```

Integration is not complete until the resulting authoritative branch is verified according to project policy.

---

# 204. Handle Integration Failure

If post-integration validation fails:

- stop further dependent integration where appropriate;
- preserve evidence;
- identify likely contributing changes;
- do not hide the failure by rewriting history casually;
- create a correction or rollback plan.

Rollback policy should be project-specific.

Production deployment remains a separate gate.

---

# 205. Maintain Integration Provenance

It should be possible to determine which task produced a particular integrated change.

Use references among:

- task IDs;
- commits;
- reports;
- reviews;
- integration records.

Do not require proprietary databases to reconstruct basic provenance.

Git history plus durable coordination records should provide the core evidence.

---

# 206. Design Mission Control to Develop Itself

Mission Control will eventually use Codex workers to improve Mission Control.

This creates additional risk because workers may modify the system coordinating themselves.

Treat Mission Control self-development as a special project with stricter boundaries.

A worker modifying coordinator code should not automatically deploy that new coordinator version into its own running control plane.

---

# 207. Separate Development and Running Control Plane

Maintain separation between:

```
Mission Control source under development

```

and:

```
Mission Control version currently controlling workers

```

New versions should pass tests and release gates before replacing the running version.

This prevents an experimental task from disabling the entire worker fleet.

---

# 208. Create a Platform Test Environment

Provide a way to test Mission Control changes without using the live worker fleet as the first test.

Potential mechanisms include:

- simulated workers;
- local test workers;
- containers;
- virtual machines;
- designated test hardware.

Tests should exercise protocol behavior and failure cases before platform deployment.

---

# 209. Implement Worker Simulation

Create lightweight simulated workers where useful.

A simulator can test:

- task claiming;
- heartbeats;
- leases;
- coordinator restart;
- duplicate workers;
- network delay;
- failures.

Simulation does not replace real physical-machine tests.

It provides faster deterministic testing of coordination logic.

---

# 210. Test Scale Beyond Two Workers

After two-worker correctness is proven, simulate or operate larger worker counts.

Test at least enough concurrency to expose assumptions such as:

- fixed worker names;
- single active task;
- non-atomic task claiming;
- report collisions;
- coordinator serialization.

Do not optimize for hundreds of workers unless there is an actual requirement.

---

# 211. Threat-Model the Completed Architecture

Perform a formal practical threat review before declaring the platform mature.

Consider:

- stolen worker;
- stolen USB installer;
- leaked deploy key;
- compromised worker;
- malicious repository content;
- compromised dependency;
- unauthorized task injection;
- coordinator compromise;
- accidental production credentials;
- GitHub account compromise.

Focus security effort on realistic consequences.

Disposable local operating systems reduce some risks but do not eliminate credential or supply-chain risks.

---

# 212. Protect Against Malicious Repository Instructions

Workers may eventually interact with repositories containing untrusted content.

Repository text must not automatically acquire control-plane authority merely because Codex reads it.

Distinguish:

- owner/ChatGPT task instructions;
- trusted repository instructions;
- arbitrary project content.

Do not allow arbitrary files in a repository to redefine credential policy, production authority, or coordinator security boundaries.

---

# 213. Protect Worker Credentials

Store worker credentials using appropriate filesystem permissions and operating-system protections.

Credentials should not be:

- world-readable;
- copied into worktrees;
- included in reports;
- printed into routine logs;
- exposed to project containers unnecessarily.

A worker may need broad repository access, but individual task processes should receive only what they actually require where practical.

---

# 214. Establish Credential Rotation

Document how to rotate:

- worker repository credentials;
- coordinator credentials;
- control-plane credentials;
- enrollment/bootstrap credentials.

Rotation should not require rebuilding the universal installer unless the installer's trust anchor itself changes.

Test rotation before relying on it operationally.

---

# 215. Establish Emergency Revocation

Provide a fast procedure for disabling a compromised worker.

The owner should be able to:

1. revoke its credentials;
2. prevent new task assignment;
3. mark its active tasks uncertain;
4. inspect remote changes it recently produced;
5. provision a replacement.

This procedure should be accessible without physical access to the compromised worker.

---

# 216. Verify Secret Scanning

Add appropriate secret detection to development workflows.

Use established tools rather than inventing a simplistic regex scanner where possible.

Scanning should occur before authoritative publication when practical.

Treat detected secrets as a security incident requiring rotation if they may have been exposed.

Removing a secret from the latest commit does not necessarily remove it from Git history.

---

# 217. Harden Production Boundaries

As Mission Control gains capabilities, ensure development workers cannot casually cross into production.

Project configuration should identify production systems explicitly.

Potential production operations should require separate authorization.

Do not place unrestricted production credentials on every worker merely for convenience.

Dedicated deployment mechanisms or workers may eventually be appropriate.

---

# 218. Consider a Deployment Worker Role

If autonomous deployment is introduced later, consider separating it from ordinary development workers.

A deployment worker could have:

- narrowly defined production credentials;
- no ordinary task workload;
- stronger approval requirements;
- deployment-specific validation.

Do not implement this role until there is an actual deployment requirement.

---

# 219. Establish Platform Release Process

Mission Control itself should have identifiable releases.

A release should identify:

- source commit;
- protocol versions;
- installer compatibility;
- migration requirements;
- known limitations;
- validation results.

Early releases may use simple Git tags.

Do not require elaborate release infrastructure before the platform is stable enough to benefit from it.

---

# 220. Define Release Channels

Eventually distinguish:

```
development
testing
stable

```

Workers controlling important projects should normally run stable releases.

Test workers may run newer versions.

Do not allow every push to the platform repository to automatically update the live fleet.

---

# 221. Implement Controlled Worker Upgrades

A worker upgrade should:

1. enter draining state;
2. checkpoint active work;
3. install approved platform version;
4. migrate local operational state if necessary;
5. restart supervisor;
6. run health checks;
7. re-register;
8. report version.

Failed upgrades should preserve enough information for rollback or reconstruction.

Because workers are disposable, reinstalling may sometimes be simpler than complex in-place recovery.

---

# 222. Prefer Rebuild Over Configuration Drift

When worker configuration diverges significantly, consider reprovisioning instead of indefinitely repairing it.

The universal installer and bootstrap system should make replacement inexpensive.

A fleet of reproducible machines is preferable to individually handcrafted pets.

Track platform version so drift is visible.

---

# 223. Establish Supported Hardware Baseline

After real testing, document minimum practical hardware.

Do not invent requirements before measurement.

The baseline should address:

- architecture;
- RAM;
- disk capacity;
- network;
- firmware/boot requirements.

Provide recommended profiles separately from minimum requirements.

Older SATA SSD workstations should remain supported when testing proves them adequate.

---

# 224. Establish Network Requirements

Document required outbound services and ports.

Likely dependencies include:

- GitHub;
- Codex/OpenAI services;
- Debian repositories;
- Docker/DDEV dependencies;
- project-specific services.

Workers should not require arbitrary inbound Internet exposure for normal operation.

Administrative SSH can be limited through local network, VPN, or firewall policy.

---

# 225. Design for UPS and Power Recovery

Dedicated desktop workers may benefit from UPS protection.

The platform itself should nevertheless tolerate abrupt power loss.

Configure firmware/OS behavior where practical so a dedicated worker can automatically restart after power restoration.

Do not make UPS availability a correctness requirement.

UPS improves availability; durable recovery provides correctness.

---

# 226. Implement Health Checks

Define local worker health checks for:

- filesystem space;
- Docker;
- supervisor;
- network;
- Git authentication;
- Codex authentication where testable without unnecessary consumption;
- coordinator connectivity.

Health should distinguish:

```
HEALTHY
DEGRADED
UNAVAILABLE

```

Do not mark a worker unhealthy solely because it is intentionally idle.

---

# 227. Detect Disk Pressure

Docker and development environments can consume substantial disk space.

Monitor available storage.

Before disk exhaustion, the worker may safely clean:

- obsolete temporary files;
- documented disposable caches;
- unused project containers;
- old build artifacts.

Do not automatically delete unknown worktrees or unpushed repositories.

When safe cleanup is insufficient, stop accepting disk-intensive tasks and report the condition.

---

# 228. Detect Memory Pressure

Workers, particularly 16 GB machines, should detect sustained memory pressure.

Possible responses:

- avoid launching additional DDEV environments;
- stop unused project environments;
- serialize heavy tasks;
- report degraded capacity.

Do not kill active development processes indiscriminately merely to reduce memory use.

Swap use by itself is not necessarily failure.

---

# 229. Define Local Cleanup Policy

Create explicit retention policies for:

- logs;
- worktrees;
- completed task directories;
- Docker images;
- caches;
- test artifacts.

Cleanup must distinguish reconstructable material from potentially unique unpushed work.

Completed task workspaces should only be removed after remote publication is verified.

---

# 230. Establish Backup Policy

Workers themselves should generally not require traditional full-system backup.

Authoritative valuable state belongs elsewhere.

Back up or replicate external authoritative systems according to their importance, including:

- Git repositories;
- project fixtures;
- coordinator durable state that is not reconstructable;
- enrollment authority;
- critical configuration.

Do not use worker disk backups as a substitute for reproducibility.

---

# 231. Test Loss of a Worker Disk

Physically or logically remove the first worker's local state.

Provision a replacement.

Verify that useful project state can be reconstructed from authoritative sources.

Any important missing information discovered during this test identifies an architectural violation.

Correct the authority model rather than adding an ad hoc manual backup if possible.

---

# 232. Test Loss of Installation Media

Assume every existing USB installer is lost.

Build new installation media from the platform repository and documented dependencies.

Verify the resulting media can provision a worker.

This proves the USB stick itself is not authoritative infrastructure.

---

# 233. Test New-Administrator Documentation

Have a fresh Codex session or technically competent reviewer follow the recovery documentation without relying on prior chat history.

Record ambiguities and missing assumptions.

Documentation succeeds only if another operator can actually use it.

Statements such as "configure normally" are insufficient where configuration details affect correctness.

---

# 234. Create the Canonical Project Start Procedure

Every managed repository should provide an obvious starting point.

A new coordinator should be able to begin with something equivalent to:

```
Read PROJECT_START_HERE.md

```

That document should direct it to:

- Project DNA;
- current state;
- active work;
- authority boundaries;
- required environment;
- recovery documentation.

Avoid requiring the coordinator to guess which of dozens of documents is current.

---

# 235. Create the Canonical Mission Control Start Procedure

Mission Control itself should have a corresponding canonical startup document.

It should answer:

- what Mission Control is;
- where authoritative state lives;
- how to inspect current fleet state;
- how to inspect projects;
- how to recover;
- what actions require owner approval;
- what work is currently unfinished.

A new ChatGPT coordinating thread should be able to use this document as its primary re-entry point.

---

# 236. Establish Documentation Freshness Rules

Operational documentation can become dangerous when stale.

When implementation changes:

- update affected documentation in the same task;
- validate referenced commands where practical;
- identify superseded documents;
- avoid maintaining contradictory "current" procedures.

Historical architecture decisions may remain for provenance but should be clearly distinguished from current operating instructions.

---

# 237. Establish Documentation Validation

Automate documentation checks where practical.

Examples:

- broken relative links;
- missing referenced files;
- invalid example schemas;
- obsolete path references;
- required canonical documents absent.

Do not attempt to automatically prove every prose statement correct.

Use automation for structural consistency and real acceptance tests for operational correctness.

**Pause here.**

At this point, **237 sections are complete**. The specification is close to its natural conclusion. I estimate roughly **15–25 sections remain**, primarily covering the final implementation roadmap, milestone gates, what Codex should build first versus defer, final acceptance criteria, and the handoff/start command that turns this document into an executable project rather than continuing to expand the architecture indefinitely.