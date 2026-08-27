# Architecture

## Components

| Component | Repository/source | Responsibility |
|---|---|---|
| Vincent | `Gordonfive/vincent` | Public installer, first boot, worker runtime, self-tests, diagnostics, updates, Git connection/execution, health, and reporting |
| Project/control repository | Operator-selected Git source | Project profile, dependency constraints, assignment input, project rules, tests, and report/output location |
| Mission Control | `Gordonfive/mission-control` | Optional private fleet enrollment, authorization, inventory, scopes, assignments, and fleet reporting |

Mission Control is not a boot-time or READY-state dependency. Vincent must remain useful with an operator-selected project/control repository and no dedicated Mission Control service.

## Worker lifecycle

1. Build and validate a reproducible Vincent installer.
2. Install Debian without embedded private credentials or permanent worker identity.
3. Create the dedicated least-privileged `vincent` service identity and generate installation identity locally.
4. Run self-tests and diagnostics and reach an unassigned READY state.
5. Allow the operator to select and authenticate an appropriate Git project/control source.
6. Load the selected source's project profile, dependency constraints, assignment, and authority boundaries.
7. Prepare an isolated workspace and required constrained tooling.
8. Safely claim a bounded task when claiming is required.
9. Execute, validate, commit, push, and publish a report.
10. Stop at the assignment boundary; completion does not imply integration, release, production, or destructive authority.
11. Maintain Debian, Vincent, and the permitted toolchain without requiring routine reimaging.

## Authority boundary

Public Vincent defines generic safety and runtime behavior. Private project/control sources may narrow scope or add task-specific requirements but cannot weaken Vincent, host, credential, or owner security boundaries.

## Human interface

Vincent must be fully operable headlessly. Local status/diagnostic consoles are part of the appliance interface. VS Code or VSCodium may be installed as an optional development interface, but core worker operation must not depend on either.
