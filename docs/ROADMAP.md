# Vincent Roadmap

**Updated:** 2026-08-27T08:17:00-08:00

This roadmap tracks release-level outcomes. Active implementation work belongs in GitHub issues, pull requests, and milestones; accepted architecture/product choices belong in `docs/DECISIONS.md` and `docs/decisions/`.

## Version 1.0 — Reproducible generic worker

### Installer and appliance proof

- Build a reproducible Debian 13 Vincent installer with a unique immutable installer build number.
- Keep network selection, credentials, target-disk selection, partitioning, and final disk-write confirmation operator-controlled.
- Exclude the active installer medium from installation targets without preselecting any remaining disk.
- Install a dedicated least-privileged `vincent` service identity; routine operation must not depend on a conventional human login account.
- Provide local appliance-style status, self-tests, and diagnostics suitable for physical testing without requiring a shell login.
- Distinguish immutable installer provenance from the independently advancing Vincent software version/build.
- Prove two clean installations on disposable hardware and publish reproducible validation evidence.

### Generic READY state

- Boot and self-test without private Mission Control configuration.
- Maintain networking and expose actionable diagnostics for link, addressing, routing, DNS, TLS, and repository/package reachability failures.
- Support configured Wi-Fi operation when Ethernet is unavailable while protecting wireless credentials from logs and reports.
- Reach an unassigned READY state before any private project/control authorization is granted.

### Git-driven bounded work

- Let the operator select and authenticate an appropriate Git repository/control source.
- Read a project/dependency profile, assignment input, constraints, and report/output location from that selected source.
- Prepare an isolated task environment while respecting project version constraints.
- Claim one harmless bounded task safely, implement it, validate it, commit/push durable results, and publish a non-secret report.
- Keep task completion separate from review, integration, release, production, or destructive authority.

### Maintenance

- Maintain the underlying Debian installation, Vincent runtime, generic development tooling, and project dependencies within active constraints.
- Implement a minimum safe public-upstream Vincent self-update mechanism if it does not materially delay the core V1 proof.
- Routine Vincent application updates must not require reimaging the worker.

**V1 acceptance:** two reproducible clean installations reach generic unassigned READY; installer provenance and current Vincent software identity are reported separately; one worker connects to an operator-selected Git source and completes one bounded task; routine system/tool maintenance works without rebuilding the machine.

## Version 1.1 — Installer and update lifecycle

- Add a validated network-installer path that can retrieve a compatible approved Vincent release from the public Vincent release channel.
- Preserve deterministic offline installation/recovery using the installer image's bundled validated Vincent payload.
- Define installer-to-Vincent compatibility metadata and reject incompatible remote releases.
- Add stronger application-update rollback/recovery.
- Define stable/testing channels, staged adoption, maintenance windows, and automatic versus operator-approved activation policies.
- Improve lifecycle reporting for installer build, current Vincent software version/build, Debian maintenance state, and project tool constraints.

## Later milestones

| Milestone | Outcome | Status |
|---|---|---|
| M2 | Worker replacement/recovery proven without local authoritative state | Not started |
| M3 | Multi-worker Git coordination proven | Not started |
| M4 | Phone-first operation proven | Not started |
| M5 | Optional Mission Control service/backend evaluated from demonstrated requirements | Deferred |
| M6 | Multi-project operation proven | Not started |
| M7 | Full operation recovery proven after worker/control-plane loss | Not started |
| M8 | Multiple supported AI-agent providers | Planned / unscheduled |

Unscheduled concepts that are worth preserving but are not release commitments belong in `docs/PLANNED_FEATURES.md`.

## Permanent constraints

- Git is the durable technical authority; accepted decisions define current architecture.
- Human judgment controls destructive hardware actions, production actions, credential scope, and major architecture.
- Workers are replaceable and least-privileged.
- Fresh Vincent is generic and does not automatically depend on Mission Control.
- Public Vincent never contains private fleet state or reusable private credentials.
- Installer build identity and Vincent software identity are distinct lifecycle values.
- Prefer established operating-system, Git, GitHub, and packaging mechanisms before inventing custom coordination infrastructure.
