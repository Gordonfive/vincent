# 108. Begin Failure-Injection Testing

A successful happy-path task is not sufficient to prove the worker architecture.

Before proceeding to universal installation, deliberately interrupt the first worker under controlled conditions.

Test failures individually so the resulting behavior can be attributed to a specific condition.

At minimum test:

- supervisor termination;
- Codex termination;
- worker reboot;
- temporary network loss;
- Git push failure;
- unexpected local modification;
- task cancellation while idle;
- task cancellation while active where safely testable.

Record expected behavior before each test.

Then compare actual behavior against the expectation.

---

# 109. Test Supervisor Crash Recovery

While a harmless task is active, terminate the worker supervisor unexpectedly.

Verify that:

1. useful workspace state remains intact;
2. systemd detects the terminated service;
3. restart policy behaves as designed;
4. the supervisor reconstructs task state;
5. task ownership is revalidated;
6. work is not duplicated;
7. the task either resumes safely or becomes explicitly blocked.

Do not manually repair state during the test unless recovery fails.

If manual intervention is required, treat that as a defect or documented limitation.

---

# 110. Test Codex Process Failure

Terminate the Codex process while leaving the supervisor operational.

Verify that the supervisor:

- detects the termination;
- captures the exit condition;
- preserves the workspace;
- classifies the failure;
- applies bounded retry policy;
- avoids duplicate commits;
- produces useful diagnostics.

If Codex can resume an interrupted supported session, test that mechanism.

If it cannot, document how a new Codex invocation receives sufficient task and workspace context to continue safely.

---

# 111. Test Worker Reboot During Active Work

Reboot the entire worker during a controlled active task.

Do not gracefully complete the task first.

After reboot verify:

- Debian starts normally;
- networking returns;
- required storage mounts correctly;
- Docker starts;
- supervisor starts;
- worker identity is unchanged;
- task state is reconstructed;
- remote ownership is verified;
- workspace state is inspected;
- the task resumes or escalates according to policy.

The test succeeds only if recovery does not depend on terminal history or human memory.

---

# 112. Test Unexpected Power-Loss Recovery

Where practical and safe for the disposable test machine, simulate an abrupt loss equivalent to power failure rather than a graceful reboot.

The purpose is to expose assumptions about:

- filesystem flushes;
- local state writes;
- incomplete Git operations;
- partially written status files;
- process cleanup.

After restart, verify state consistency.

Use atomic file-update patterns for critical local operational state where necessary.

The platform should prefer reconstructable state over complicated local transactional mechanisms whenever possible.

---

# 113. Test Network Interruption

Disconnect the worker from the network during a controlled task.

Test separately during:

- Codex communication;
- Git fetch;
- Git push;
- idle polling.

Verify that local work is not discarded.

When connectivity returns, the supervisor should reconcile remote state before continuing.

A failed push must remain visibly distinct from a completed remote publication.

Avoid aggressive retry loops.

---

# 114. Test Git Remote Divergence

While the worker has an active task branch, deliberately create a safe conflicting remote change in the test repository.

Verify that the worker detects divergence.

The worker must not:

- force push;
- silently overwrite the remote;
- discard its local changes;
- claim success.

If deterministic automatic reconciliation is not safe, transition to an appropriate blocked state and produce a conflict report.

---

# 115. Test Unexpected Dirty Workspace

Introduce an untracked or modified file into a worker workspace outside the normal task flow.

Then attempt to begin or resume work.

The supervisor should detect unexpected state before allowing destructive cleanup or branch replacement.

Classify files where possible as:

- expected task changes;
- known generated files;
- unknown modifications.

Unknown potentially valuable work must be preserved or escalated.

Never use `git reset --hard` or `git clean -fdx` as an unconditional recovery mechanism.

---

# 116. Test Task Cancellation

Define and test cancellation semantics.

A queued task should be cancellable without execution.

For an active task, cancellation must specify whether the worker should:

- stop immediately;
- reach a safe checkpoint;
- preserve local changes;
- commit a checkpoint;
- push a checkpoint branch;
- produce a cancellation report.

Do not destroy useful work merely because the task was cancelled.

Cancellation must be durable and distinguishable from failure.

---

# 117. Test Task Supersession

A task may become obsolete because a replacement task has been issued.

Define `SUPERSEDED` independently from `CANCELLED`.

The replacement task should reference the superseded task where appropriate.

The worker must not continue obsolete implementation after discovering authoritative supersession.

Preserve useful existing work so the replacement task or human reviewer can reuse it.

---

# 118. Test Human-Decision Blocking

Create a test assignment intentionally requiring a decision the worker is not authorized to make.

Verify that the worker:

1. recognizes the boundary;
2. preserves progress;
3. creates a decision request;
4. enters `WAITING_FOR_HUMAN`;
5. stops consuming Codex capacity unnecessarily;
6. resumes only after receiving a valid durable decision.

Test both approval and rejection/alternative selection.

---

# 119. Test Usage-Limit Behavior

When practical, test the actual behavior produced when Codex capacity is unavailable.

Do not intentionally waste large quantities of usage merely to trigger the condition if a safe simulation can validate most supervisor behavior.

Separate:

- simulated supervisor-state testing;
- actual Codex limit observation.

When a real limit occurs naturally, capture sanitized diagnostic evidence and compare it with the implemented detector.

Update detection logic based on observed behavior rather than assumptions.

---

# 120. Establish Phase 1 Recovery Acceptance

Phase 1 recovery is accepted only when the first worker can survive the tested interruptions without losing authoritative useful work or corrupting remote state.

Produce a recovery test matrix containing:

- failure condition;
- expected behavior;
- actual behavior;
- result;
- defects found;
- corrective commit;
- retest result.

Do not proceed merely because most tests pass.

Classify failures according to whether they threaten:

- local convenience;
- task recoverability;
- Git authority;
- credentials;
- external systems.

Failures threatening authoritative state must be resolved before progression.

---

# 121. Measure First-Worker Resource Use

Record representative resource consumption during:

- idle operation;
- Codex execution;
- Git operations;
- Docker operation;
- simple DDEV environment;
- test execution.

Collect:

- RAM;
- swap;
- CPU;
- disk usage;
- Docker storage;
- relevant process counts.

This is characterization, not benchmarking for its own sake.

Use the results to establish practical defaults for 16 GB and larger workers.

Do not prematurely reject lower-powered hardware based solely on theoretical recommendations.

---

# 122. Establish Resource Profiles

Create initial optional worker resource profiles.

For example:

```
lightweight
standard
heavy

```

Profiles may influence:

- maximum simultaneous tasks;
- maximum active DDEV projects;
- cleanup policy;
- task eligibility.

Do not encode rigid hardware classes unnecessarily.

Capabilities and measured resources should remain more important than marketing-era hardware labels.

A 16 GB worker should remain useful for appropriate work.

---

# 123. Prepare the Universal Installer

After the manually developed provisioning path has passed Phase 1, convert it into the reusable installation mechanism.

The universal installer must derive its configuration from version-controlled sources rather than from undocumented state on the first workstation.

Rebuild installer inputs from a clean checkout.

Do not create the "universal" image by cloning the first worker's disk.

The installer must reproduce the machine from declared configuration.

---

# 124. Make Installer Builds Reproducible

Document and automate creation of installation media.

A fresh authorized development machine should be able to build the installer using documented commands.

Record:

- Debian source/version;
- required packages;
- installer configuration;
- injected bootstrap files;
- checksums where useful;
- resulting image metadata.

Do not depend on a manually modified ISO whose changes cannot be reproduced.

---

# 125. Minimize Secrets on Installation Media

Inspect the generated installer for embedded secrets.

The installation media must not contain:

- personal GitHub tokens;
- permanent worker private keys;
- production credentials;
- unrestricted SSH private keys;
- project secrets.

If a bootstrap credential is required, document:

- its exact scope;
- lifetime;
- revocation mechanism;
- consequences of disclosure.

Prefer enrollment that generates worker identity after installation.

Assume USB media can be lost or copied.

---

# 126. Test Installer on the First Workstation

Erase the first test workstation and rebuild it using the universal installer.

This is a critical milestone.

Do not preserve hidden configuration from the previous installation.

The test should prove that the platform repository and installer contain everything required to reconstruct the worker.

After installation:

1. enroll the worker;
2. provision it;
3. verify services;
4. assign the end-to-end test task;
5. verify push/report;
6. reboot;
7. verify continued operation.

Record every manual action.

---

# 127. Eliminate Unnecessary Manual Steps

Review the universal-installer test.

For every manual action ask:

> Is human judgment actually required here?

If not, automate it.

Examples potentially suitable for automation:

- package installation;
- Docker setup;
- service enabling;
- repository checkout;
- configuration generation;
- worker software installation;
- health verification.

Actions that establish trust or authorize credentials may deliberately remain manual.

The goal is not zero human actions at any cost.

The goal is zero unnecessary human actions.

---

# 128. Define Installer Success Output

After provisioning, the worker should expose a concise status indicating whether it is ready.

Conceptual states:

```
INSTALLING
BOOTSTRAPPING
ENROLLMENT_REQUIRED
PROVISIONING
VERIFYING
READY
FAILED

```

When ready, expose at least:

```
worker_id
hostname
platform_version
network_state
enrollment_state
supervisor_state

```

Do not require scrolling through installation logs to determine whether provisioning succeeded.

---

# 129. Preserve Installation Logs

Installation and bootstrap logs should be retained long enough to diagnose provisioning failures.

Avoid placing credentials in those logs.

Where practical, make failed-installation diagnostics exportable or remotely retrievable after network configuration succeeds.

Do not make successful routine installation dependent on external log storage.

Local standard logs are sufficient initially.

---

# 130. Establish Universal Installer Acceptance

The installer is accepted when a wiped compatible test machine can reach `READY` using the documented workflow without undocumented repair.

Acceptance evidence should include:

- installer build commit;
- installer checksum;
- target hardware summary;
- installation result;
- enrollment result;
- platform version;
- end-to-end task result;
- reboot result.

Commit documentation and test evidence.

The image itself may be stored outside ordinary Git if its size makes Git inappropriate.

Git should contain everything necessary to reproduce it.

---

# 131. Select the Second Worker

Choose a second physical computer with materially different hardware.

Prefer the available Linux-capable laptop with approximately 16 GB RAM.

The second-worker test exists to prove that the installer is genuinely generic.

Record only relevant hardware differences.

Do not manually customize the installer specifically for the second machine unless the customization becomes a supported hardware-detection/configuration mechanism.

---

# 132. Provision the Second Worker

Use the same universal installer.

The second worker must:

- generate a different identity;
- receive an independent authorization;
- install the same platform;
- register its actual capabilities;
- reach `READY`;
- enter `IDLE`.

Verify that credentials belonging to worker one are not copied to worker two.

The same physical USB media may be reused.

---

# 133. Verify Independent Revocation

Test that either worker can be revoked without disabling the other.

At minimum verify the selected authentication architecture behaves as documented.

After revocation, the affected worker should fail safely.

It should not repeatedly attempt destructive or uncontrolled recovery.

Restore/re-enroll it afterward if needed.

This proves worker identity is genuinely independent.

---

# 134. Verify Heterogeneous Resource Handling

Compare the heavy worker and 16 GB worker.

Verify that both can perform basic assignments.

Then test representative heavier workloads.

The smaller worker may legitimately:

- run fewer simultaneous environments;
- experience slower builds;
- use swap;
- be ineligible for explicitly heavy tasks.

The coordinator architecture should treat this as capability variation, not worker failure.

Document practical resource thresholds based on observation.

---

# 135. Test Two Workers Simultaneously

Assign independent tasks to both workers at the same time.

Verify:

- each claims only its own task;
- both operate independently;
- both push successfully;
- reports identify the correct worker;
- local services do not interfere;
- coordinator/task state remains coherent.

Use a safe test repository before attempting parallel work on an important project.

---

# 136. Test Competing Task Claims

Create a task for which both workers are eligible and do not explicitly assign a worker.

Allow both to discover it concurrently.

Verify exactly one worker acquires ownership.

The losing worker should:

- recognize the failed claim;
- avoid starting Codex;
- avoid modifying the task workspace;
- return to task discovery.

Repeat the test enough times to expose obvious race conditions.

Do not proceed to general autonomous scheduling if duplicate execution remains possible.

---

# 137. Test Explicit Worker Assignment

Create a task explicitly assigned to one worker.

Verify:

- designated worker accepts it;
- other worker sees but does not claim it;
- coordinator does not override the assignment merely because another worker is idle or more powerful.

This preserves the architecture in which ChatGPT may choose the worker and the coordinator executes that decision.

---

# 138. Test Capability-Based Eligibility

Create tasks requiring declared capabilities.

Examples:

```
requires:
  - docker
  - ddev

```

or:

```
minimum_ram_gb: 32

```

Verify workers that do not satisfy the requirement refuse the task.

Do not rely entirely on worker self-labeling when capabilities can be verified automatically.

Capability checks should be understandable and deterministic.

---

# 139. Test Parallel Git Work

Have both workers operate against the same repository using independent task branches/worktrees.

Verify:

- no shared mutable checkout;
- no branch collision;
- independent starting commits are recorded;
- both changes are pushed;
- integration can detect whether changes conflict.

Then deliberately create a safe overlapping change to verify conflict handling.

Parallelism must not weaken Git authority.

---

# 140. Test Independent DDEV Environments

Use an appropriate test Drupal project.

Assign each worker a task requiring DDEV.

Verify each worker uses a unique DDEV project identity.

Confirm:

- containers are isolated;
- databases are independent;
- ports/routes do not collide on the same worker;
- one worker stopping its project does not affect another physical worker;
- project recreation is deterministic.

Do not depend on one shared mutable development database unless a project explicitly defines such an architecture.

---

# 141. Define Development Data Authority

Projects such as Drupal may require development database content to reproduce meaningful environments.

The platform must distinguish:

```
application source
configuration
development fixture data
production data
secrets

```

A project's reproducible development state may require an authoritative sanitized database fixture or reconstruction process.

Do not assume source code alone recreates application state.

The project, not the worker platform core, should define its development-data authority.

---

# 142. Support Sanitized Development Fixtures

Design the platform so projects can provide sanitized database fixtures.

A future project workflow may:

1. obtain an authorized production-derived database;
2. remove or replace sensitive information;
3. generate a development fixture;
4. version or otherwise publish the fixture through an appropriate controlled mechanism;
5. allow workers to recreate equivalent development environments.

Never commit unsanitized sensitive production data merely because a repository is private.

During development stages containing no sensitive information, simpler fixtures may be acceptable according to project policy.

---

# 143. Verify Cross-Worker Reproducibility

Given the same project revision and development fixture, two workers should be able to create materially equivalent development environments.

Verify important properties such as:

- application version;
- configuration;
- database fixture version;
- enabled modules/components;
- theme state;
- relevant content required for comparison.

Machine-specific details may differ.

Functional project state should not depend on which worker created it.

---

# 144. Establish Phase 2/3 Acceptance

Universal installation and multi-worker operation are accepted when:

- the same installer provisions both machines;
- identities are independent;
- enrollment works;
- revocation is independent;
- both workers execute tasks;
- simultaneous execution works;
- claiming prevents duplicate ownership;
- explicit assignment works;
- capability eligibility works;
- independent Git work works;
- DDEV isolation works where applicable;
- reboot recovery remains functional.

Publish an acceptance report and resulting platform commit.

---

# 145. Begin Remote Control-Plane Work

Only after the worker foundation is reliable should the project optimize phone-based operation.

The first control plane should expose durable operations required to:

- create a task;
- assign a worker;
- change priority;
- cancel/supersede a task;
- answer a decision request;
- inspect task state;
- inspect worker state;
- inspect completion reports.

Do not require a custom mobile application initially.

Use existing authenticated services where they satisfy the requirements.

---

# 146. Evaluate GitHub as the Initial Remote Interface

Evaluate whether GitHub itself can provide the initial phone-accessible control surface.

Potential components include:

- repository files;
- issues;
- pull requests;
- GitHub Actions;
- GitHub API;
- GitHub App.

Consider:

- ease of use from a phone;
- machine readability;
- authentication;
- audit history;
- race conditions;
- ChatGPT integration possibilities;
- worker polling complexity.

GitHub is already part of the trust and durability model, so prefer it when it adequately solves the problem.

Do not force all ephemeral runtime state into GitHub merely for architectural uniformity.

---

# 147. Define the ChatGPT Integration Boundary

Document exactly what must exist for ChatGPT to function as the practical coordination layer.

Do not assume that a ChatGPT conversation automatically has authority to modify GitHub or control workers.

The architecture should identify explicit integration capabilities required for actions such as:

```
inspect project state
inspect worker reports
create task
modify task
assign worker
record owner decision
request integration
review completion

```

Where ChatGPT has an authenticated GitHub integration capable of these operations, use that supported integration.

Where it does not, define a narrow service or interface rather than pretending direct control exists.

The desired result is:

```
Owner speaks/types to ChatGPT from phone
                ↓
         ChatGPT reasons
                ↓
    authenticated durable action
                ↓
         worker platform

```

The authentication and action boundary must be explicit and auditable.

**Pause here. Section 148 should continue with the phone-first control workflow, ChatGPT/coordinator interaction, coordinator implementation, unattended long-duration operation, and eventual Mission Control recovery model.**