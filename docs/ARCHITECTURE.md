# Architecture

## Components

| Component | Repository | Responsibility |
|---|---|---|
| Vincent | `Gordonfive/vincent` | Public installer, enrollment client, worker runtime, health and reporting |
| Mission Control | `Gordonfive/mission-control` | Private fleet authorization, policy, assignments, and fleet reports |
| Project repositories | Project-owned | Product DNA, source, project rules, tasks, tests, and reports |

## Worker lifecycle

1. Build a reproducible Vincent ISO.
2. Install Debian without embedded credentials.
3. Generate a stable worker identifier and unique keypair locally.
4. Produce a public enrollment request.
5. Await explicit owner approval.
6. Receive narrowly scoped repository access.
7. Fetch Mission Control policy and a bounded assignment.
8. Read the assigned project's authority chain.
9. Claim, execute, test, publish, report, and stop.
10. Permit suspension or revocation without rebuilding the fleet.

## VS Code

VS Code or VSCodium may be installed as an optional human interface. It may expose worker status, logs, tests, and project workspaces. Mission Control must not depend on VS Code, and a headless Vincent worker must retain full functionality.
