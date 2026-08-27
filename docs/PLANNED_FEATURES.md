# Vincent Planned Features

This document preserves product ideas that are worth retaining but are not committed to a release or implementation schedule. Once scheduled, a feature should move to a milestone/issue and the applicable roadmap release; once rejected, remove it after any useful rationale is captured in a decision record.

## Worker liveness and leased work assignments

**Status:** Planned; unscheduled. Final component ownership remains open.

### Goal

A future coordinating system should distinguish work that is actively owned and progressing from work abandoned because a worker disappeared, failed, lost connectivity, or otherwise stopped completing the assignment.

### Proposed model

- Each Vincent installation has a stable worker identity that survives reboot.
- Workers may send periodic heartbeats for liveness/health reporting.
- Work assignments use time-bounded leases rather than indefinite ownership.
- An active worker renews its lease while it continues to own the assignment.
- Temporary heartbeat loss enters a grace period rather than causing immediate reassignment.
- An expired assignment becomes eligible for reassignment.
- Reissued work receives a new lease identity/term so stale results cannot silently supersede newer work.
- Heartbeats describe worker liveness; leases describe work ownership. Scheduling correctness should depend on leases rather than heartbeat state alone.

A per-boot/session identifier may later improve diagnostics by distinguishing transient link loss from reboot or replacement, but it is not currently required for lease correctness.

### Scope

This concept may ultimately belong in Mission Control or another coordinator rather than the Vincent core. It must not make a fresh Vincent installation dependent on a coordinator merely to reach READY.

## Multi-agent AI worker support

**Status:** Long-term planned feature; unscheduled.

### Goal

Vincent should eventually support multiple AI coding/automation agent providers while preserving a common Vincent lifecycle for installation, configuration, diagnostics, updates, task execution, and reporting.

### Proposed model

- Provision only the operator-selected agent/provider and its prerequisites rather than every possible stack.
- Candidate integrations may include Codex, Gemini tooling, GitHub Copilot tooling, Ollama/local-model workers, and custom providers.
- Isolate provider-specific installation, authentication, capability detection, execution, health checks, updating, and removal behind a provider interface.
- Support containerized providers where appropriate without requiring containers for all providers.
- Let hardware/resource discovery influence provider availability when local models require particular CPU, RAM, storage, or GPU capabilities.
- Keep Vincent task/reporting and safety semantics independent of one AI vendor where practical.

### Scope

Current implementation may optimize for Codex. This future feature should influence interface boundaries but must not delay the initial Vincent release.

## Backlog rule

Do not use this file as an active task tracker. When work becomes actionable, create a GitHub issue with acceptance criteria and associate it with the appropriate milestone/release. Consequential implementation choices should be recorded in ADRs/decision records.
