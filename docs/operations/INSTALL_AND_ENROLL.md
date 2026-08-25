# Install and Enroll a Disposable Worker

This procedure stages software and generates a new identity. It does not authorize the worker or start unattended operation.

## Preconditions

- Linux host with Python 3.11 or newer, Git, OpenSSH client tools, and systemd.
- A locally verified checkout of the public `Gordonfive/vincent` platform repository.
- Console or other trusted access to compare the generated fingerprint.
- No operational project credential embedded in the checkout or installer.

## Staging

Run the installer as root and provide the absolute verified checkout path:

```text
sudo ./installer/install.sh /absolute/path/to/vincent
```

The installer creates the locked `mission-control` service account, isolated state/workspace directories, a Python virtual environment, example configuration, and a disabled systemd unit. It then generates a unique Ed25519 installation identity and prints the public enrollment request.

## Initial trust

Initial trust is established only when the owner compares the enrollment request fingerprint through a trusted channel and deliberately authorizes that specific `worker_id`. Merely possessing the installer or creating a request grants no repository access.

After approval, an enrollment authority supplies narrowly scoped operational authorization outside Git. The approval record may be committed, but private keys, tokens, and Codex credentials must not be committed.

## Activation gate

Before enabling the service:

1. Replace example values in `/etc/mission-control/worker.toml`.
2. Install approved per-worker Git authorization through the selected secret-delivery mechanism.
3. Complete supported Codex authentication for the service account.
4. Run `mission-control-worker --config /etc/mission-control/worker.toml doctor`.
5. Confirm the reported worker ID and all readiness checks.
6. Enable the service only after owner approval is durable.

The current M1 unit is a readiness oneshot, not an autonomous task loop.

## Reinstallation and recovery

The installer refuses to reuse an existing identity. Do not delete evidence automatically. Decide explicitly whether this is:

- recovery of the same authorized installation, using a separately documented protected backup;
- replacement by a new identity followed by revocation of the old worker; or
- forensic preservation of an unexpected installation state.

Replacement is the default disposable-worker path.
