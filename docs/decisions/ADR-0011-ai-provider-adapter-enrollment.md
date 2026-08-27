# ADR-0011 — Provider-neutral AI adapters; Vincent performs provider-specific local enrollment

**Status:** Accepted  
**Decision date:** 2026-08-27T11:49:00-08:00

## Context

Vincent is currently Codex-focused, but the intended product is an AI-worker platform that can later support Gemini, Copilot, Ollama/local-model workers, and custom agents. Authentication/enrollment semantics differ across providers, and Mission Control may eventually assign an intended provider/account/project profile to a managed worker.

## Decision

Vincent isolates provider-specific installation, authentication/enrollment, capability, health, update, and runtime behavior behind an AI-provider adapter boundary.

Vincent performs provider-specific enrollment locally through the selected adapter. For human-bound accounts, supported device/interactive authorization is preferred over copying reusable credentials through Git or task text.

When supported, Vincent verifies and reports non-secret effective provider identity/account/organization/tenant/project context and authentication health. Clear mismatches must be surfaced or blocked rather than silently using an unintended identity.

Mission Control may assign the desired provider identity/profile and authentication policy for an enrolled worker, but Mission Control does not become the provider-specific credential runtime.

Reusable provider credentials are not Git state. Any future unattended delivery requires a separately protected mechanism with unique/scoped/revocable credentials; a shared fleet-wide AI credential is prohibited.

## Rationale

This allows Codex-first implementation without embedding one vendor's authentication model into Vincent's core lifecycle and preserves a clean boundary between fleet policy and local provider integration.

## Consequences

- Codex integration should migrate behind the provider interface as the architecture matures.
- Provider-specific status/health data exposed to Mission Control must be non-secret.
- Provider credentials use protected local/provider mechanisms rather than Git.
- Future provider additions should not require redesigning worker identity, task execution, or fleet enrollment semantics.
