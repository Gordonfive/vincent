# ADR-0019: CIC Station enrollment connectivity and operational policy

**Status:** Accepted  
**Decision date:** 2026-08-28

## Context

Vincent must remain a generic standalone worker while supporting optional managed enrollment into independently deployed CIC Station instances. The program must support public, NATed, private, and isolated networks without depending on a Gordonfive-operated rendezvous or relay service.

CIC Station ADR-0019 defines the cross-product enrollment locator, bootstrap, NAT, offline-network, and worker-egress policy. This ADR records the Vincent-side obligations.

## Decision

### Enrollment remains optional

A fresh Vincent installation must still be able to reach standalone READY without CIC Station. CIC Station enrollment is an explicit later transition into managed authority and does not replace standalone operation.

### Generic installer and direct CIC locator

Universal Vincent installation media must not contain fleet-specific CIC Station configuration or reusable enrollment credentials. Managed enrollment accepts a CIC Station endpoint supplied by the operator or equivalent authorized provisioning input.

Supported endpoint forms must include public DNS names, private DNS names, and routable IP addresses, including private same-subnet addresses for isolated deployments.

Vincent does not depend on a central Gordonfive pairing, registry, SSO, rendezvous, or relay service to discover CIC Station.

### Bootstrap key

Vincent accepts a CIC Station-issued one-time bootstrap key represented as four groups of four case-insensitive alphanumeric characters, for example `7K3M-P9XR-2WQF-8DNT`.

The key is only enrollment authorization. Vincent must never persist or use it as the worker's permanent credential. Successful enrollment invalidates it at CIC Station; replay, substitution, expiration, and failed-attempt handling are governed by the authenticated enrollment protocol.

A QR code may encode the same endpoint and bootstrap material as a convenience but does not alter the security model.

### Permanent worker identity

Vincent generates its asymmetric installation identity locally before enrollment and protects the private credential. During enrollment Vincent initiates the connection to the supplied CIC Station endpoint, presents the authorized bootstrap material and its public identity, and completes the proof-of-possession and server-trust flow required by the shared protocol.

After enrollment, the durable relationship is based on the worker's asymmetric identity and trusted CIC Station identity, not the bootstrap key.

### Outbound-only normal control-plane communication

Routine managed communication is initiated outbound by Vincent. A normal Vincent worker must not require inbound management port exposure, router port forwarding, or a publicly reachable worker address.

This permits workers behind ordinary NAT and CGNAT as long as they can reach CIC Station.

### Offline/private enrollment

Public Internet access is not a prerequisite for Vincent/CIC Station enrollment. If Vincent can reach CIC Station directly over a private subnet, private routed network, VPN/overlay, or equivalent operator-controlled path, enrollment and the permanent trust relationship must be able to complete without GitHub, Debian mirrors, AI-provider endpoints, or other public services.

External capabilities are diagnosed separately. A worker may be securely enrolled and healthy with respect to CIC Station while external software/provider capabilities are unavailable.

### Managed operational configuration

Once enrolled, CIC Station is authoritative for managed operational policy. Vincent must obtain and safely enforce managed settings such as connectivity mode, proxy configuration, approved software sources, update/source policy, agent/provider configuration, repository/project scopes, assignment policy, and other managed runtime configuration as the protocol evolves.

At minimum the architecture must support these network-policy concepts:

- direct Internet access;
- CIC Station-proxied/egress-gateway access;
- an external proxy/gateway configured through CIC Station policy;
- restricted/offline operation limited to CIC Station and approved internal resources.

Vincent retains only the local bootstrap/recovery state necessary to locate and authenticate CIC Station and to operate safely when CIC Station is temporarily unavailable.

### CIC Station-delivered software

Vincent must permit managed deployments in which CIC Station distributes or caches approved Vincent software, packages, agent/provider components, assignment payloads, container artifacts, or equivalent managed dependencies. This allows workers with no direct Internet access to operate through an organization-controlled CIC Station or separately configured proxy.

Vincent must not assume that every software or provider endpoint is directly reachable from the worker.

## Rationale

This preserves Vincent's standalone product boundary while providing a scalable managed-enrollment model for independent CIC Station deployments. It avoids a mandatory central service, handles worker NAT naturally, supports isolated same-subnet enrollment, and lets organizations centralize egress and software distribution without configuring every worker independently.

## Consequences

- Current code that treats enrollment as mandatory must be corrected as already tracked by issue #37.
- Managed enrollment UI/protocol work must accept endpoint plus one-time bootstrap key and support private addresses.
- Network diagnostics must distinguish CIC Station reachability from public-Internet/provider/package-source reachability.
- Normal worker operation requires no inbound management listener exposed to the network.
- Managed configuration must have a defined precedence and safe cached/recovery behavior rather than being scattered through one-off local edits.
- Vincent and CIC Station protocol compatibility remains explicitly versioned and retry-safe.

## Cross-product authority

The canonical cross-product decision is CIC Station `docs/decisions/ADR-0019-decentralized-enrollment-and-worker-egress-policy.md`. If wording differs, the two ADRs must be reconciled before implementation; neither product may silently invent a conflicting enrollment protocol.
