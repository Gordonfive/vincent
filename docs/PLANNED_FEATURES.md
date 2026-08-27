# Vincent Planned Features

This document records agreed feature ideas that are worth preserving but are not yet committed to a Vincent roadmap release or implementation schedule. A feature may ultimately belong in Vincent, Mission Control, or another component after architecture and scope are decided.

## Mission Control product architecture

### Status

Architecture direction accepted; implementation deferred until the Vincent worker foundation is sufficiently mature.

### Product definition

Mission Control will be a **self-hostable server application with a web interface and authenticated API** for managing fleets of Vincent workers. It is not planned as a desktop application and is not intended to exist only as a centrally hosted Gordonfive website.

Vincent remains the independently functional worker platform. A Vincent system must be able to boot, diagnose itself, maintain Debian and Vincent, update from its trusted public upstream, and remain healthy without Mission Control. Mission Control becomes relevant when a Vincent installation is enrolled into a managed fleet.

Conceptually:

- **Vincent:** what this worker can do.
- **Mission Control:** what this worker may do, what it should do, and what it is doing now.

### Planned Mission Control responsibilities

- worker enrollment, durable fleet identity, approval, revocation, and trust state;
- worker inventory, health, versions, capabilities, hardware/resources, installed agent providers, and last contact;
- roles, authorization policy, repository/project scopes, and least-privileged access;
- assignment creation, dispatch, claiming, leases, renewal, expiration, and reassignment;
- fleet status and operational reporting;
- structured task results and audit history;
- human approval gates for destructive, production, credential-expanding, release, and other sensitive actions;
- fleet policy such as minimum Vincent versions, update channels, staged adoption, or temporary pins without replacing Vincent's own update mechanism;
- assignment of AI provider identity profiles describing the desired provider plus account/organization/project context and authorization policy, while Vincent performs provider-specific enrollment;
- eventual selection of appropriate worker and AI-agent combinations based on assignment requirements and worker capabilities.

Mission Control should not become a general-purpose remote shell or replacement for SSH/Linux administration. Normal worker communication should be initiated outbound by Vincent over an authenticated network protocol so workers can operate behind NAT and ordinary firewalls without requiring inbound management ports.

### Deployment model

The primary product is self-hosted and browser-administered. Expected deployments include a local server/VM/NAS, a VPS, or a containerized deployment where appropriate. A future hosted Mission Control service may be offered for users who do not want to operate the control plane themselves, but self-hosting remains a first-class architecture.

### Public/private repository direction

The current `Gordonfive/mission-control` repository remains private while it contains our private planning, coordination, fleet state, and infrastructure metadata. If Mission Control becomes a distributable Vincent product, the reusable Mission Control application source should ultimately be public/open alongside Vincent. Our real deployment state, assignments, authorization data, infrastructure metadata, and other private operational material must then live separately from the public application source.

Mission Control application source and Mission Control deployment/fleet state must be treated as separate concerns even before that repository split occurs.

### Initial implementation strategy

Early fleet coordination may remain Git-backed while workflows and data structures are proven. Data models should nevertheless be designed so worker identity, enrollment, capabilities, assignments, leases, authorization, results, and audit records can migrate cleanly to a service/API and database later. Do not build a server merely to reproduce workflows that Git can adequately prove during early Vincent development.

## Worker liveness and leased work assignments

### Status

Planned feature; unscheduled. Mission Control is now the intended coordinating component, although protocol and implementation details remain undecided.

### Goal

Mission Control must be able to distinguish work that is actively owned and progressing from work that has been abandoned because a worker disappeared, failed, lost connectivity, crashed, or was otherwise unable to finish.

### Proposed model

- Each Vincent installation has a stable worker identity/UUID that survives reboot.
- A worker enrolls or checks in with Mission Control.
- Mission Control identifies the worker's available resources/capabilities and selects an appropriate assignment.
- The worker explicitly accepts the assignment and leaves durable documentation that the assignment was accepted and work is beginning.
- Workers send periodic heartbeats so Mission Control can determine whether the worker itself is active and reachable.
- Work assignments are issued as time-bounded **leases** rather than indefinite ownership.
- An active worker renews its lease while it continues to own the assignment.
- Temporary heartbeat loss should enter a grace period rather than immediately causing reassignment, allowing for transient network or service failures.
- If the assignment lease expires without acceptable renewal/results, the work becomes eligible for reassignment to another worker.
- Reissued work receives a new lease identity/term so stale results from an expired lease cannot silently supersede newer work.
- Heartbeats describe worker liveness; leases describe work ownership. Scheduling correctness should depend on leases rather than heartbeat state alone.

### Worker boot/session identity

A per-boot or per-session ID may be useful for diagnostics. It would allow Mission Control to distinguish a temporary connectivity interruption from a machine crash, reboot, or power interruption. It is not currently considered necessary for task-leasing correctness and should remain optional until there is a demonstrated need.

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
- Mission Control may assign an enrolled worker an AI identity profile defining the provider and intended account, organization, tenant, project, or equivalent context. Vincent performs the supported provider-specific authorization flow locally and reports only non-secret identity/scope metadata and health state.
- For Codex, supported ChatGPT/device authorization is the preferred initial human enrollment path where available. Future adapters may use OAuth/device authorization, SSO/browser authorization, scoped API/service credentials, or no remote credentials for local-model agents.
- If the provider cannot automatically select or enforce the intended account/project, Vincent should verify the resulting context where possible and surface mismatch/blocked state rather than silently continuing with an unintended identity.
- Authentication material must remain outside Git. Future unattended enrollment should use a separately protected secret backend/broker or one-time delivery mechanism and issue unique, scoped, revocable credentials rather than shared fleet-wide secrets.
- Containerized/Docker-based agents should be supported where appropriate because container isolation can simplify dependency management and make adding or replacing agent implementations easier.
- Native/non-containerized agents must remain possible where containers are inappropriate or unsupported.
- Hardware/resource discovery may eventually influence which agents Vincent offers or recommends, particularly for local-model workers requiring significant CPU, RAM, storage, or GPU resources.
- Mission Control may eventually select or recommend worker/agent combinations according to assignment requirements and reported capabilities.
- The architecture should allow additional agent providers to be added later without rebuilding Vincent's core scheduling/enrollment concepts around each provider.

### Scope note

This feature should not drive current Codex-focused development or delay the initial Vincent releases. Current implementation may optimize for Codex while avoiding unnecessary architectural assumptions that would make later multi-agent support difficult.

## Future architecture discussions

### Mission Control protocol and service design

Mission Control's product role is now defined at a high level. Future architecture work must define the Vincent-to-Mission-Control protocol, authentication and enrollment model, service/API boundaries, database model, web UI, deployment packaging, and migration from early Git-backed coordination.

### Decision records

Review the project's existing timestamped/incremental decision-note system against formal Architecture Decision Records (ADRs). Discuss advantages, disadvantages, migration cost, and whether both mechanisms have distinct useful roles before changing the current process.
