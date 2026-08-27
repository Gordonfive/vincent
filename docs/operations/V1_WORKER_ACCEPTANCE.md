# Vincent V1 Worker Acceptance

This document defines the release-level physical worker proof. Exact build/test commands belong in the current installer workstream documentation and must match the source under test.

## Preconditions

- One exact reviewed source commit and installer build number.
- Repository validation and image validation pass.
- Exact removable-media target identified and authorized before flashing.
- Disposable installation target hardware.
- No private credential, permanent identity, or reusable enrollment secret embedded in installer media.

## Installation proof

1. Boot the validated installer on disposable hardware.
2. Confirm normal interactive network selection and credential entry.
3. Confirm the active installer medium is not offered as an installation target.
4. Confirm target-disk selection, partitioning method/layout, and final disk-write confirmation remain operator-controlled.
5. Complete installation without requiring a conventional human runtime account.
6. Confirm the dedicated least-privileged `vincent` service identity and separately controlled administrative/recovery path.
7. Confirm installer build provenance is retained and displayed separately from current Vincent software version/build.

## READY proof

1. Boot with no private Mission Control configuration.
2. Run automatic/local self-tests and expose results through the appliance status/diagnostic interface.
3. Verify interface, addressing, route, DNS, TLS/HTTPS, and required package/repository reachability diagnostics.
4. Verify healthy Ethernet operation.
5. When Wi-Fi hardware is available, remove Ethernet and prove operation over a protected configured Wi-Fi profile or the local SSID/passphrase workflow.
6. Reach an unassigned READY state without private project authority.

## Bounded-task proof

1. Operator selects and authenticates an approved Git project/control repository.
2. Vincent loads the project profile, dependency constraints, task, acceptance criteria, and report/output location.
3. Vincent creates an isolated workspace and installs only permitted/constrained task dependencies.
4. Claim the task using the selected source's approved ownership mechanism.
5. Execute the task through the configured AI-agent provider.
6. Run independent validation required by the project/task.
7. Commit and push useful results; verify the remote state.
8. Publish a non-secret completion/failure report.
9. Stop at the task boundary. Do not infer integration, release, production, or destructive authority from task completion.

## Maintenance proof

- Apply representative Debian maintenance without reimaging.
- Update/maintain Vincent through its approved public release mechanism when available.
- Maintain representative development tooling while honoring active project version constraints.
- Confirm application/tool updates do not alter immutable installer provenance.

## Reproducibility

Repeat a clean installation on disposable hardware. V1 acceptance requires two clean installations that reach READY without hand-entered repair steps.

## Evidence

The acceptance record should identify:

- source commit;
- installer build number;
- image checksum;
- target hardware class;
- current Vincent software version/build;
- tests and physical checks performed;
- deviations/failures;
- resulting task/report commits where applicable.

A successful image build alone is not physical acceptance.
