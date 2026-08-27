# Security

Vincent is public software and must be safe to download without authentication.

## Never commit

- passwords, tokens, cookies, private keys, or authentication caches;
- personal GitHub credentials or reusable enrollment secrets;
- AI-provider API keys, device/session credentials, service-account credentials, or reusable provider authentication material;
- production data or private project content;
- fixed worker identities;
- private hostnames, addresses, or infrastructure credentials.

## Enrollment

Installation grants no private access. First boot generates a unique local keypair and produces an enrollment request containing only the public key, fingerprint, worker identifier, and non-secret capability information. The owner must explicitly approve the worker and grant a unique, scoped, revocable credential.

No universal fleet key is permitted.

## AI provider enrollment

Mission Control may assign an enrolled worker an AI provider identity profile describing the intended provider and account, organization, tenant, project, or equivalent context. Vincent performs the provider-specific enrollment locally and reports only non-secret effective identity/scope and health information.

Prefer interactive/device authorization for human-bound accounts when supported so reusable credentials are not embedded in installers or transmitted through Git. If unattended enrollment is later required, use a separately protected secret broker/backend or one-time delivery mechanism with authenticated transport and unique, least-privileged, revocable worker/provider credentials.

Shared fleet-wide AI-provider credentials are prohibited. Raw provider credentials, tokens, cookies, API keys, private keys, and authentication caches never belong in either Git repository.

## Reporting

Logs and reports must redact credentials and avoid environment dumps. Git conflicts, authorization failures, provider-identity mismatches, and integrity failures must be reported and must not be destructively auto-resolved.
