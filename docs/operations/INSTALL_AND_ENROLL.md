# Install and Authorize a Vincent Worker

This procedure stages Vincent and creates a local installation identity. Staging does not grant private project authority or start unattended task execution.

## Preconditions

- Debian-compatible host with the dependencies required by the selected Vincent release.
- Verified checkout or approved Vincent release payload.
- Trusted console/management access for reviewing the generated identity and diagnostics.
- No private project credential embedded in the installer or source payload.

## Staging

For a verified source checkout, the current installer entry point is:

```text
sudo ./installer/install.sh /absolute/path/to/vincent
```

The installer creates the dedicated locked `vincent` service identity, protected state/workspace directories, the Vincent environment, example configuration where applicable, and a locally generated installation identity. It must not silently authorize the worker or grant access to a private project/control repository.

Some internal service/configuration identifiers still use earlier `mission-control` implementation names. These are compatibility/implementation debt tracked separately; they do not mean a fresh Vincent installation depends on the Mission Control product.

## Generic READY state

Before private project/control configuration, Vincent should be able to:

1. complete local first-boot provisioning;
2. run self-tests and diagnostics;
3. report installer provenance and current Vincent software identity;
4. verify required local/network capabilities;
5. reach an unassigned READY state.

## Project/control authorization

When the operator assigns the worker:

1. Select the approved Git project/control source.
2. Authenticate using a unique, narrowly scoped, revocable credential appropriate to that source.
3. Verify the source/repository identity and allowed scope.
4. Load the project profile, dependency constraints, assignment and report location.
5. Complete AI-provider authentication separately; do not place provider credentials in Git.
6. Run the applicable readiness/doctor checks.
7. Enable task execution only after required authorization and checks pass.

Mission Control may provide these private control functions in a deployment, but it is not the only possible source and is not required for generic READY.

## Reinstallation and recovery

Do not silently reuse an unexpected existing installation identity. Explicitly classify the situation as:

- recovery of the same authorized installation using protected recovery material;
- replacement by a new identity followed by revocation/retirement of the old identity; or
- preservation of unexpected state for diagnosis.

Replacement with a newly generated identity is the normal disposable-worker path unless an approved recovery procedure applies.
