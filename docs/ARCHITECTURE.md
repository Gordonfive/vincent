# Architecture

## Components

| Component | Repository | Responsibility |
|---|---|---|
| Vincent | `Gordonfive/vincent` | Public installer, enrollment client, worker runtime, AI-provider adapters, health and reporting |
| Mission Control | `Gordonfive/mission-control` | Private fleet authorization, policy, assignments, AI identity-profile assignment, and fleet reports |
| Project repositories | Project-owned | Product DNA, source, project rules, tasks, tests, and reports |

## Worker lifecycle

1. Build a reproducible Vincent ISO.
2. Install Debian without embedded credentials.
3. Generate a stable worker identifier and unique keypair locally.
4. Produce a public enrollment request.
5. Await explicit owner approval.
6. Receive narrowly scoped repository access.
7. Receive an AI provider identity profile when managed by Mission Control, or operator-selected provider configuration when standalone.
8. Perform provider-specific enrollment locally through the relevant Vincent adapter; prefer supported device/interactive authorization for human-bound accounts and keep reusable credentials out of Git.
9. Verify/report non-secret provider identity, scope, and authentication health; block or surface mismatches rather than silently using an unintended account/project.
10. Fetch Mission Control policy and a bounded assignment.
11. Read the assigned project's authority chain.
12. Claim, execute, test, publish, report, and stop.
13. Permit suspension or revocation without rebuilding the fleet.

## AI provider boundary

Mission Control controls the desired provider identity/profile and policy. Vincent owns provider-specific installation, enrollment, credential-health checks, and runtime integration. Provider adapters must accommodate Codex first and later Gemini, Copilot, Ollama/local-model, and custom agents without coupling Vincent's core worker lifecycle to one vendor.

Provider credentials are not Git state. Any future unattended credential delivery must use a separately protected secret mechanism and unique, scoped, revocable credentials.

## VS Code

VS Code or VSCodium may be installed as an optional human interface. It may expose worker status, logs, tests, and project workspaces. Mission Control must not depend on VS Code, and a headless Vincent worker must retain full functionality.
