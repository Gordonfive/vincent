# ADR-0009 — Runtime wired/Wi-Fi resilience and layered diagnostics

**Status:** Accepted  
**Decision date:** 2026-08-26T12:42:00-08:00

## Context

Physical testing showed that workers may be installed over Ethernet and later deployed without a cable, and that installer/runtime failures need evidence that distinguishes link, DNS, routing, TLS, mirror and repository/provider problems.

## Decision

Vincent workers must enumerate available wired/wireless interfaces and remain operational over usable Wi-Fi when a healthy Ethernet path disappears.

When both are healthy, wired Ethernet is preferred by default. If Ethernet disappears, Vincent first tries a previously configured working Wi-Fi profile. If none is usable, a local console workflow must scan/list SSIDs, permit operator selection, and securely accept the passphrase without requiring a human login account.

Vincent must provide layered non-secret diagnostics capable of distinguishing interface/link, Wi-Fi association/authentication, addressing/DHCP, routing, DNS, HTTP(S)/TLS, Debian package-source, Git/repository, and provider-specific reachability failures.

## Rationale

A dedicated worker should not permanently depend on the installation interface, and troubleshooting should not require guesswork or exposing credentials.

## Consequences

- Wi-Fi credentials remain in protected system network configuration and never in Git/log/report/status output.
- Network management requiring privilege uses narrow root-owned mechanisms; the `vincent` service account does not receive unrestricted network administration.
- Physical acceptance includes Ethernet removal and continued operation through Wi-Fi.
- Installer development may include targeted preflight evidence for Debian mirror/DNS/interception diagnostics.
