# Vincent Planned Features

This document records agreed feature ideas that are worth preserving but are not yet committed to a Vincent roadmap release or implementation schedule. A feature may ultimately belong in Vincent, Mission Control, or another component after architecture and scope are decided.

## Worker liveness and leased work assignments

### Status

Planned feature; unscheduled. Architecture and component ownership are not yet decided.

### Goal

Mission Control or a future coordinating system must be able to distinguish work that is actively owned and progressing from work that has been abandoned because a worker disappeared, failed, lost connectivity, crashed, or was otherwise unable to finish.

### Proposed model

- Each Vincent installation has a stable worker identity/UUID that survives reboot.
- A worker enrolls or checks in with the coordinating system.
- The coordinating system identifies the worker's available resources/capabilities and selects an appropriate assignment.
- The worker explicitly accepts the assignment and leaves durable documentation that the assignment was accepted and work is beginning.
- Workers send periodic heartbeats so the coordinating system can determine whether the worker itself is active and reachable.
- Work assignments are issued as time-bounded **leases** rather than indefinite ownership.
- An active worker renews its lease while it continues to own the assignment.
- Temporary heartbeat loss should enter a grace period rather than immediately causing reassignment, allowing for transient network or service failures.
- If the assignment lease expires without acceptable renewal/results, the work becomes eligible for reassignment to another worker.
- Reissued work receives a new lease identity/term so stale results from an expired lease cannot silently supersede newer work.
- Heartbeats describe worker liveness; leases describe work ownership. Scheduling correctness should depend on leases rather than heartbeat state alone.

### Worker boot/session identity

A per-boot or per-session ID may be useful for diagnostics. It would allow the coordinating system to distinguish a temporary connectivity interruption from a machine crash, reboot, or power interruption. It is not currently considered necessary for task-leasing correctness and should remain optional until there is a demonstrated need.

### Design inspiration

The conceptual model is similar to distributed-work systems such as BOINC/SETI@home: work is checked out for a bounded period, results are expected within that period, and abandoned/expired work can eventually be issued again.

## Multi-agent AI worker support

### Status

Long-term planned feature; unscheduled and intentionally outside the near-term roadmap.

### Goal

Vincent should eventually be an AI-worker platform rather than a platform coupled specifically to Codex. A Vincent installation should be capable of hosting different supported AI coding/automation agents while preserving a common Vincent lifecycle around installation, configuration, enrollment, diagnostics, updates, and work execution.

### Proposed model

- During first boot/provisioning, Vincent can ask which AI worker/agent the installation will use.
- Initial candidate integrations include OpenAI Codex, Google Gemini tooling, GitHub Copilot tooling, Ollama/local-model workers, and custom-built agents.
- Vincent installs the selected agent and its required prerequisites rather than requiring every possible agent stack in the base image.
- Agent-specific installation and configuration should be isolated behind a provider/adapter interface so Vincent's core does not become dependent on one vendor.
- Agent definitions should describe prerequisites, installation/update procedures, runtime requirements, authentication/enrollment requirements, capabilities, health checks, and removal/replacement procedures.
- Containerized/Docker-based agents should be supported where appropriate because container isolation can simplify dependency management and make adding or replacing agent implementations easier.
- Native/non-containerized agents must remain possible where containers are inappropriate or unsupported.
- Hardware/resource discovery may eventually influence which agents Vincent offers or recommends, particularly for local-model workers requiring significant CPU, RAM, storage, or GPU resources.
- The architecture should allow additional agent providers to be added later without rebuilding Vincent's core scheduling/enrollment concepts around each provider.

### Scope note

This feature should not drive current Codex-focused development or delay the initial Vincent releases. Current implementation may optimize for Codex while avoiding unnecessary architectural assumptions that would make later multi-agent support difficult.

## Future architecture discussions

### Define Mission Control

A dedicated future discussion is required to define what Mission Control should be before assigning this feature permanently to Vincent or Mission Control. Existing project discussions contain preliminary Mission Control concepts, but its intended scope, responsibilities, boundaries, and relationship with Vincent should be reviewed explicitly before those ideas are treated as final architecture.

### Decision records

Review the project's existing timestamped/incremental decision-note system against formal Architecture Decision Records (ADRs). Discuss advantages, disadvantages, migration cost, and whether both mechanisms have distinct useful roles before changing the current process.
