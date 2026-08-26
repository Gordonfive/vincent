# ADR-0002: Appliance Accounts and Local Console Model

Status: Accepted during Workstream 2 physical ISO testing

## Decision

Vincent workers are appliances, not general-purpose interactive Linux hosts.

- Do not create a human login account during installation.
- Do not require the owner to choose a username or password.
- Root must not be usable for local login after installation.
- Keep one locked system service account, `mission-control`, with home `/var/lib/mission-control` and shell `/usr/sbin/nologin`.
- Run Vincent and Codex worker activity under that least-privileged service account with explicit `HOME`, `USER`, `LOGNAME`, and XDG paths when tools require a user environment.
- Do not use `nobody` as a general execution identity for tools that require a home directory or persistent user state.
- tty1 is the persistent Vincent dashboard, not a login prompt.
- tty2 is an optional interactive Codex console, launched as `mission-control`, not root.
- Local console access must not expose a shell or require a local login account.
- SSH and other remote authority are provisioned through Vincent/Mission Control enrollment and scoped authorization, not a shared local password.

## Debian installer implementation constraint

Debian Installer can force `passwd/make-user=true` when `passwd/root-login=false`. To avoid the human-account prompt while preserving the final no-login policy, the installer may temporarily satisfy Debian's account state machine with an unusable preseeded root credential, keep `passwd/make-user=false`, and explicitly lock root in `late_command` before first boot.

Acceptance requires the installed system to prove both:

- no human UID-range login accounts exist; and
- the root password is locked.

## Rationale

The worker is intended to be self-provisioning, remotely managed, replaceable, and least-privileged. Human local accounts and reusable passwords add state, recovery burden, and credential risk without providing required product capability.
