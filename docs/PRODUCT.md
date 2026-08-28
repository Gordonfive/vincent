# Vincent Product Definition

## Product

**Vincent** is a Linux-first platform for provisioning and operating reproducible AI development workers on ordinary computers.

The name Vincent is not an acronym. `Vincent` is used in prose and product names; lowercase `vincent` is appropriate for commands, packages, service accounts, paths, configuration keys, and similar technical identifiers.

## Purpose

Vincent reduces the amount of repetitive human administration required to turn spare computers into useful development workers. It provides a repeatable appliance-like worker environment that can be installed, diagnosed, maintained, updated, connected to projects, assigned bounded work, validated, and replaced without trapping authoritative project state on one machine.

Vincent is designed to support a small fleet first, using understandable components and conservative correctness rules. It should scale only when demonstrated needs justify additional complexity.

## Primary users

Vincent is intended for operators who want dedicated or mostly dedicated machines to execute development work through supported AI coding/automation agents while preserving normal software-engineering controls around Git, testing, security, and review.

The initial reference operator is technically capable and comfortable with Linux/Git, but normal worker operation should not require continuously watching terminals or administrating every worker interactively.

## Core goals

Vincent should:

- turn compatible commodity hardware into a reproducible development worker;
- use Debian 13 as the initial reference operating system and remain Linux-first;
- support headless and unattended operation after the operator has completed required trust/destructive choices;
- make the worker replaceable by keeping durable project work outside the worker and making local state reconstructable wherever practical;
- preserve Git as the durable authority for source and project artifacts;
- provide safe, explicit boundaries around credentials, destructive actions, production access, and authoritative external state;
- support heterogeneous workers with different CPU, RAM, storage, network, and AI-agent capabilities;
- provide clear self-tests, diagnostics, health/status reporting, and human-readable failure states;
- maintain Debian, Vincent, runtime dependencies, and development tooling while respecting active project constraints;
- update Vincent through a trusted public release channel without requiring routine reimaging;
- support a generic standalone READY state before any private project or fleet authority is granted;
- support an operator-selected Git/project source for initial standalone workflows;
- integrate with CIC Station when explicitly enrolled into a managed fleet;
- use an AI-provider adapter boundary so Codex can be supported first without making the worker architecture permanently vendor-specific;
- support provider-specific local enrollment/authentication and report non-secret effective identity/health where possible;
- remain suitable for public/open-source distribution without owner-specific private state embedded in the reusable core.

## Non-goals

Vincent is not:

- CIC Station or a fleet-wide scheduler/control plane;
- a general-purpose remote administration shell;
- a replacement for SSH/Linux administration when administration is actually required;
- an autonomous production-deployment authority by default;
- a system for storing fleet secrets or private operational state in the public repository;
- dependent on one project, one Git repository, one physical workstation, or one AI provider;
- required to support every operating system in early releases;
- required to provide local AI inference or GPU acceleration;
- required to eliminate human decisions involving product purpose, credentials, destructive actions, production, or significant risk;
- designed to maximize machine utilization at the expense of correctness, recoverability, or task ownership.

## Product boundaries

### Vincent owns

- the worker installer and installation provenance;
- local worker runtime and service management;
- local identity generation and worker health;
- project/environment preparation and bounded execution;
- workspace isolation and Git safety checks;
- deterministic local validation/reporting;
- local networking recovery and diagnostics;
- Debian/toolchain/Vincent maintenance;
- trusted Vincent software updates;
- AI-provider adapter installation, enrollment integration, and credential-health checks;
- the Vincent side of an authenticated CIC Station protocol.

### CIC Station owns

CIC Station is a separate product for managed fleets. It owns concepts such as enrollment approval/trust, fleet inventory, authorization policy, roles/scopes, assignment dispatch/leasing, liveness, AI identity-profile policy, approvals, fleet reporting, fleet policy, and operator-facing fleet control.

A fresh Vincent worker must not require CIC Station to boot, diagnose itself, maintain itself, update Vincent, or reach an unassigned READY state.

### Project repositories own

Each assigned project remains authoritative for its own source, requirements, repository instructions, tests, dependencies/version constraints, production policy, and durable project artifacts. Vincent must not silently weaken project constraints merely because it has local administrative capability.

## Guiding principles

### Durable work over local convenience

A worker may be powerful locally, but loss of a worker must not imply loss of authoritative project work. Valuable completed work and decisions are externalized through Git/project systems and structured results.

### Human attention is expensive; human judgment is not disposable

Automate repetitive synchronization, provisioning, testing, reporting, maintenance, and recovery. Preserve explicit human authority for consequential decisions.

### Correctness before utilization

When task ownership, credentials, Git state, or remote authority are ambiguous, stop or block rather than guessing. Waiting is preferable to duplicate/conflicting work.

### Proven components before custom infrastructure

Prefer standard Debian, systemd, Git, SSH, Docker/container tooling, established authentication mechanisms, structured serialization, and operating-system logging. Add custom infrastructure only for Vincent-specific behavior that standard components do not already provide.

### Reproducibility over handcrafted machines

Manual repair is development evidence, not the desired final state. Necessary changes should be encoded in installer/bootstrap/runtime configuration so replacement machines can reproduce supported behavior.

### Evidence over declarations

A capability is not verified merely because code exists. Acceptance requires evidence appropriate to the capability: automated tests, image inspection, physical installation, real Git publication, recovery tests, network failover, or other outcome-level validation.

## Product maturity and release philosophy

Vincent uses independent Semantic Versioning. Pre-1.0 releases use `0.x.y`; `1.0.0` is reserved for the first release that satisfies the accepted Vincent 1.0 requirements and physical/operational acceptance criteria.

Installer build numbers are a separate monotonically increasing provenance identity. They identify the installation media/build used to create a worker and remain immutable even when Vincent software later updates in place.

## Licensing

Vincent is licensed under the Mozilla Public License 2.0 (MPL-2.0).

External contributions are intentionally not accepted yet. Contribution policy will be revisited at Vincent 1.0 or later.
