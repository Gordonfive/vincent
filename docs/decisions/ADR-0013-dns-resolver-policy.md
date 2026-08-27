# ADR-0013 — DNS Resolver Policy

**Status:** Accepted  
**Decision date:** 2026-08-27 (America/Sitka)

## Context

Installer and runtime diagnostics need dependable DNS while remaining portable across networks. Development testing also showed that DNS substitution alone does not solve TLS interception or filtering problems.

## Decision

Vincent must not unnecessarily depend on a single public DNS provider.

Where explicit public resolvers are appropriate for diagnostics or fallback testing, Vincent prefers a diversified pair such as `1.1.1.1` and `9.9.9.9`. Google public DNS is not the default dependency.

Normal operation should continue to respect valid network-provided resolver configuration unless a specific recovery or diagnostic path requires otherwise.

DNS fallback must not be treated as a workaround for TLS interception, captive portals, content filtering, or other non-DNS failures.

## Rationale

This avoids unnecessary provider concentration and keeps diagnostics technically honest about the difference between name resolution and higher-layer network failures.

## Consequences

Installer/runtime diagnostics may probe more than one resolver, but must separately report DNS, routing, TLS/HTTPS, and package-source failures.
