# Vincent Architecture

Vincent is the worker-side product. Mission Control is a separate optional fleet control plane. Project repositories remain authoritative for project-specific source, requirements, instructions, tests, constraints, and durable project artifacts.

See [`PRODUCT.md`](PRODUCT.md), [`REQUIREMENTS.md`](REQUIREMENTS.md), and the [`decisions/`](decisions/) ADRs for normative product/decision context.

## System boundary

| Component | Responsibility |
|---|---|
| **Vincent installer** | Reproducible Debian-based installation media, installer safety, build provenance, first-boot payload |
| **Vincent local runtime** | Worker identity, service lifecycle, status, diagnostics, networking recovery, project/workspace preparation, bounded execution, validation/reporting, maintenance, updates |
| **AI-provider adapter** | Provider-specific installation, enrollment/authentication integration, identity/health checks, runtime invocation |
| **Project/control source** | Project requirements, repository instructions, dependency constraints, bounded assignment input, result/report destination |
| **Mission Control client boundary** | Authenticated outbound managed-fleet protocol when explicitly enrolled |
| **Mission Control** | Separate control plane for fleet trust, inventory, authorization, assignments/leases, approvals, fleet policy, AI identity profiles and operational reporting |

Vincent's local runtime must not expose internal names that imply it is itself Mission Control. `Mission Control` is reserved for the separate control-plane product/integration surface.

## Standalone lifecycle

A fresh/standalone worker follows this lifecycle:

1. Boot reproducible Vincent installer media.
2. Operator selects network configuration and target storage/partitioning through the normal installer interaction boundary.
3. Installer excludes its own active media from installation targets.
4. Debian/Vincent are installed without reusable private credentials or permanent fleet identity.
5. First boot establishes local worker identity and the dedicated `vincent` service account/runtime.
6. Self-tests, network/health checks and diagnostics run.
7. Worker reaches **READY / unassigned** without Mission Control.
8. Operator selects/authenticates an allowed project/Git/control source and an AI provider as required by the workflow.
9. Vincent reads project constraints, prepares an isolated task environment, executes bounded work through the selected provider, validates results, publishes durable work/results, and returns to an idle/ready state.

## Managed-fleet lifecycle

When the operator explicitly enrolls Vincent into Mission Control:

1. Vincent presents/generates a worker identity/enrollment request.
2. Mission Control/operator approves trust and scope.
3. Vincent establishes authenticated outbound control-plane communication.
4. Vincent reports non-secret worker inventory/capabilities/health/version data.
5. Mission Control may assign a bounded task/lease, repository/project scope, and desired AI-provider identity/profile policy.
6. Vincent performs any provider-specific local enrollment through its adapter and verifies non-secret effective identity/scope where supported.
7. Vincent executes only work whose current lease/authorization/project constraints are valid.
8. Structured state/results/approval requests return to Mission Control while source/project artifacts remain in their project authorities.
9. Revocation, lease loss or authority mismatch causes stop/block behavior rather than silent continuation.

Normal fleet operation is outbound from the worker and does not require a general inbound remote-shell interface.

## Durable versus local/ephemeral state

### Durable outside the worker

- project source and authoritative Git history;
- project requirements/instructions;
- accepted ADRs/product requirements;
- published task results/reports;
- Mission Control managed-fleet trust/authorization/assignment/audit state where applicable;
- release artifacts/metadata;
- required development fixtures through the project's chosen authoritative mechanism.

### Durable local but reconstructable/replaceable

- worker private identity and protected local credentials;
- configured Wi-Fi profiles;
- installed Debian/Vincent/tooling state;
- workspace/checkpoint state needed for safe interruption recovery;
- local logs/diagnostic evidence before export.

### Ephemeral

- running process IDs;
- current CPU/memory/load samples;
- live provider process/session state;
- transient retries/heartbeats/leases as defined by the controlling system.

Loss of a worker must not imply loss of authoritative project work.

## Privilege boundary

The `vincent` service identity is the normal automation principal. It is locked/non-human and does not receive unrestricted sudo.

Privileged system operations use narrow root-owned helpers/systemd services/interfaces. Human administrative/recovery access is separate. Project processes/containers should receive only the credentials/capabilities they actually require where practical.

## Installer safety boundary

Vincent automates safe appliance defaults but not deployment-specific/destructive choices. Installer validation therefore checks both positive behavior (required payload/guards) and negative behavior (no forced target/partitioning, no embedded reusable identity/secrets).

Installer build provenance is immutable and independent from the current Vincent software SemVer version.

## Networking

Vincent enumerates wired/wireless interfaces and prefers healthy Ethernet by default. It can reuse/configure protected Wi-Fi without exposing passphrases in Git/log/status/report output.

Layered diagnostics distinguish link/association, addressing, routing, DNS, HTTP(S)/TLS, package source, repository and provider failures. Installer-specific preflight evidence may additionally capture non-secret resolver/interception/package-source diagnostics used during physical validation.

## AI-provider boundary

The core worker lifecycle is provider-neutral. Provider adapters describe/install/invoke the provider and implement provider-specific authentication/enrollment and health/identity checks.

Codex is the initial implementation target, but the interface must permit future Gemini, Copilot, Ollama/local-model and custom-agent providers without redesigning worker identity/task/recovery concepts.

Mission Control may select an intended provider/account/project profile; Vincent remains responsible for actual provider-specific local enrollment/runtime behavior.

Provider credentials are never normal Git state and shared fleet-wide AI credentials are prohibited.

## Update and version boundary

Vincent software uses Semantic Versioning and updates from validated public Vincent release artifacts/metadata. The installer build number remains immutable provenance.

Vincent also maintains Debian/runtime/development tooling subject to active project constraints. Fleet policy may later influence timing/channels, but local application of updates remains a Vincent responsibility.

## Optional human interfaces

VS Code/VSCodium or other interfaces may be installed for human convenience, but Vincent and Mission Control architecture must not depend on them. A headless worker retains full supported worker functionality.
