# Security

Vincent is intended for public/open-source distribution and must be safe to release and download without authentication. Development currently remains private under ADR-0014 until the explicit public-release gate is approved.

## Never commit

- passwords, tokens, cookies, private keys, or authentication caches;
- personal GitHub credentials or reusable enrollment secrets;
- production data or private project content;
- fixed worker identities;
- private hostnames, addresses, or infrastructure credentials.

## Enrollment

Installation grants no private access. First boot generates a unique local keypair and produces an enrollment request containing only the public key, fingerprint, worker identifier, and non-secret capability information. The owner must explicitly approve the worker and grant a unique, scoped, revocable credential.

No universal fleet key is permitted.

## Reporting

Logs and reports must redact credentials and avoid environment dumps. Git conflicts, authorization failures, and integrity failures must be reported and must not be destructively auto-resolved.
