# ADR-0016 — Rootless container runtime for routine worker execution

**Status:** Accepted  
**Decision date:** 2026-08-27 (America/Sitka)

## Context

The dedicated `vincent` service account is intended to be least-privileged. Membership in the host Docker group grants practical root-equivalent authority through the Docker daemon socket, which conflicts with that boundary.

Vincent still needs a broadly useful local container runtime for project work.

## Decision

Routine Vincent worker containers use **rootless Podman** under the locked `vincent` service identity.

The worker must not receive membership in the host `docker` group or routine access to a root-owned container daemon socket. Rootless container prerequisites such as subordinate UID/GID ranges and rootless storage/network helpers are provisioned explicitly.

Root-required container operations, if ever required by a project or device-specific workflow, are outside routine worker authority and require a separately designed narrow privileged interface or explicit operator action.

## Rationale

Rootless Podman preserves the normal container-development workflow while keeping ordinary container processes inside the worker user's privilege boundary instead of delegating unrestricted host-root authority through a daemon socket.

## Consequences

- The generic Vincent baseline installs and validates rootless Podman rather than granting Docker-group membership.
- Project tooling should use OCI/container behavior that works with Podman/rootless operation where practical.
- Tests must verify the `vincent` account has no Docker-group membership and can run a representative rootless container.
- Rootless limitations involving devices, low ports, unusual filesystems, networking, image UID mappings, or project-specific Docker assumptions must be surfaced as explicit compatibility failures rather than bypassed silently.
- **Revisit criterion:** if real Vincent workloads demonstrate material incompatibility or unacceptable operational cost from rootless Podman, reopen the container-runtime architecture decision. Any replacement must preserve the least-privilege requirement; simply restoring unrestricted Docker-group access is not an acceptable fallback without a new explicit security decision.

## Relationship

This decision strengthens ADR-0002 and VIN-REQ-0017; it does not replace the dedicated `vincent` service identity.
