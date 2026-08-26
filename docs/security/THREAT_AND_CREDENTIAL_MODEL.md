# Threat and Credential Model

## Assets

- Authoritative Git history and repositories
- Project DNA and decisions
- Worker and coordinator credentials
- Enrollment authority
- Sanitized fixtures and project configuration
- Production systems and credentials

## Primary threats

- Lost or stolen installer media or worker
- Leaked deploy key, token, Codex auth cache, or reusable local password
- Compromised worker or dependency
- Unauthorized task injection
- Malicious repository instructions attempting to redefine authority
- Accidental force-push, branch deletion, production action, or secret publication
- Coordinator compromise or loss

## Boundaries

- The universal installer contains no permanent owner credential or worker private identity.
- Installation does not create a human local login account or owner-chosen password.
- Root is locked before first boot and must remain unusable for local password login.
- The locked `mission-control` system account is the worker execution identity; it is not a human login account and uses `/usr/sbin/nologin`.
- Tools that require user state run with explicit service-account `HOME`, `USER`, `LOGNAME`, and XDG paths rather than relying on an interactive login environment.
- tty1 is a status/dashboard surface and tty2 may host a constrained Codex console; neither is a general shell/login surface.
- Each installation generates a new worker identity.
- Enrollment explicitly binds that public identity to approved scope.
- Workers receive no production credentials by default.
- Project content cannot override owner/control-plane authority.
- External destructive actions require separate policy and approval.

## Initial GitHub recommendation

Use a unique SSH identity per prototype worker and repository-scoped write access only to safe platform/test repositories. Deploy keys are simple for a one-repository prototype but scale poorly across many repositories. The likely migration is a GitHub App that issues short-lived, narrowly scoped installation tokens and supports multi-repository access and independent revocation.

Fine-grained personal access tokens are not preferred as permanent worker identities because they remain tied to a person and are broader than necessary. Never embed any of these credentials in installer media or Git.

## Codex authentication

Official documentation currently supports ChatGPT login, device-code login for headless systems, API-key login, enterprise access tokens, and workload identity in applicable environments. Phase 1 must select based on the owner's account/workspace capabilities. Copying `auth.json` is a documented fallback but creates a reusable secret and is not the preferred enrollment design.

Codex authentication state belongs to the worker service identity, not to a human local Linux account. Any interactive Codex console must still run as the locked `mission-control` account and must not imply a reusable local-login credential.

## Revocation

Revocation must disable one worker without disabling others, prevent new assignments, mark active ownership uncertain, and trigger review of recent remote changes.
