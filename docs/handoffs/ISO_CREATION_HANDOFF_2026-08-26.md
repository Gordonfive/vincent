# Vincent ISO Creation Handoff

**Updated:** 2026-08-26T09:37:00-08:00  
**Authoritative repository:** `Gordonfive/vincent`  
**Active branch:** `workstream/iso-decisions-reconcile`  
**Current source commit:** `eef301e42d37073d43808b4b66090e2bdad492f5`  
**Current ISO build number:** `0011`  
**Decision checkpoint:** `2026-08-26T08:30:34-08:00`

This document is the continuation point for a fresh ChatGPT project thread working specifically on Vincent ISO creation and physical installation testing. Git is authoritative; chat history is not required if this document and the required project documents are read first.

## Required startup sequence

Before making changes or issuing a build:

1. Fetch `Gordonfive/vincent` and all branches/tags.
2. Read `AGENTS.md`.
3. Read `docs/PROJECT_START_HERE.md`.
4. Read `docs/DECISIONS.md` and refresh any decisions newer than the decision checkpoint above.
5. Read `docs/ROADMAP.md` if its last-updated timestamp is newer than the last-known roadmap checkpoint.
6. Read this handoff.
7. Verify that `workstream/iso-decisions-reconcile` has not advanced beyond the source commit recorded above; if it has, inspect the newer commits before proceeding.
8. Do not build from an older ISO branch merely because it contains previously tested code.

## Current branch-consolidation state

The active ISO work was consolidated onto `workstream/iso-decisions-reconcile` from current `main`. Historical ISO, migration, and audit histories remain preserved, but obsolete behavior was not blindly merged.

Draft PR #2 exists for consolidation into `main`. Do not merge it until the current physical ISO work is validated. `main` may therefore lag the active ISO implementation.

The branch contains the useful physical-test work from the earlier ISO/self-test branch plus current decisions from `main`.

## Current authoritative product decisions affecting ISO work

The current accepted decisions in `docs/DECISIONS.md` include:

- Runtime automation uses the dedicated non-human Unix account `vincent`.
- Installation must not require creation of a conventional human login account or human username/password.
- Root is reserved for bootstrap/system operations and must not become a routine remote-login account.
- Vincent must not force guided partitioning, LVM, whole-disk use, or a fixed recipe. Disk partitioning remains in the normal Debian installer workflow.
- Every ISO build has a unique monotonically increasing build number.
- The build number must agree across ISO filename, ISO/USB media identity, manifest, checksum/evidence, and installed worker metadata.
- The tty1 status dashboard must prominently display the installed build number.
- Before every build, refresh the decision register for decisions newer than the last-known checkpoint.

Do not reintroduce the older forced-LVM or human-account behavior.

## Current build identity

Current build number:

```text
0011
```

Expected artifact naming/identity for this sequence:

```text
vincent-debian-13.6.0-amd64-build-0011.iso
VINCENT_B0011
```

The branch tip may advance while keeping build number `0011` during iterative correction of this physical-test series. If the owner directs a new build number, update `installer/debian13/BUILD_NUMBER` and ensure all propagated identifiers remain consistent.

## Current installer behavior

The intended current behavior is:

- Debian 13 amd64 installer.
- No arbitrary human username/password creation.
- Disk partitioning remains normal Debian interactive partitioning.
- Destructive disk selection/confirmation remains operator-controlled.
- First boot derives a stable hostname in the form `vincent-worker-NNNNNN` without lifecycle words such as `unenrolled`.
- Runtime source is fetched from public `https://github.com/Gordonfive/vincent.git` at the exact commit embedded in the ISO.
- Network bootstrap waits/retries route, DNS, HTTPS, and Git fetch rather than immediately failing on transient readiness.
- tty1 is a persistent Vincent dashboard/status display.
- tty2 (`Alt+F2`) is an optional non-root interactive Codex console once Codex is installed; `Alt+F1` returns to the dashboard.
- The worker self-tests without requiring a local human login or manual shell commands.

## Physical-test operating rule

The owner does not want to log into the worker or run diagnostic commands on it during normal ISO testing. Physical test evidence should come from the self-test/dashboard and photographs.

When a physical test fails, improve the appliance's own diagnostics rather than asking the owner to troubleshoot interactively unless a later explicit exception is made.

The dashboard should retain critical information at the top and display useful live work output beneath it. A photograph should capture enough state to identify the build, source commit, network state, current task, last error, worker identity, and useful command output.

## Current physical-test result — build 0011

Build `0011`, source commit `dc7291aa2af294c179abe445e9889d15c3123e1c`, successfully reached the Vincent dashboard and displayed:

- `BUILD: 0011`
- stable `vincent-worker-977750` hostname
- worker ID and fingerprint
- source commit
- IP/default route
- `GITHUB DNS: pass`
- live toolchain output

The physical run failed during bootstrap after Docker root diagnostics. The terminal error was:

```text
Could not get home directory for current user. Is it set? err=$HOME is not defined
```

This demonstrated that build-number propagation and the live dashboard were functioning, but a service-account execution path still lacked the correct login/home context.

## Current untested correction

Commit:

```text
eef301e42d37073d43808b4b66090e2bdad492f5
```

changes `service_run()` in `bootstrap/provision-worker-baseline.sh` to use:

```text
runuser -u vincent --login -- env ...
```

while still explicitly supplying `HOME`, `USER`, `LOGNAME`, XDG directories, and PATH. The purpose is to provide a proper login-group context, including the newly added `docker` supplementary group, while retaining the deterministic Vincent service environment.

This correction has **not yet been validated or physically tested** at the time of this handoff.

## Immediate next gate

Validate the exact current source commit before rebuilding:

```bash
cd ~/code/vincent

git fetch origin workstream/iso-decisions-reconcile
git checkout --detach eef301e42d37073d43808b4b66090e2bdad492f5

printf 'HEAD=%s\n' "$(git rev-parse HEAD)"
printf 'BUILD_NUMBER='
cat installer/debian13/BUILD_NUMBER

TS="$(date +%Y%m%d-%H%M%S)"
set -o pipefail

sh scripts/validate.sh 2>&1 | tee "logs/validate-${TS}.log"
status=${PIPESTATUS[0]}
echo "VALIDATE_EXIT_STATUS=${status}" | tee -a "logs/validate-${TS}.log"
test "$status" -eq 0
```

Expected build number is `0011`. Do not proceed to image creation unless validation exits `0`.

## Build/inspection procedure after validation

Keep large output visible and save it with `tee`.

```bash
cd ~/code/vincent

mkdir -p dist/archive
mv dist/vincent-debian-*.iso* dist/archive/ 2>/dev/null || true

TS="$(date +%Y%m%d-%H%M%S)"
set -o pipefail

sh installer/debian13/build-image.sh \
  installer/debian13/cache/debian-13.6.0-amd64-netinst.iso \
  2>&1 | tee "logs/build-image-${TS}.log"

status=${PIPESTATUS[0]}
echo "BUILD_EXIT_STATUS=${status}" | tee -a "logs/build-image-${TS}.log"
test "$status" -eq 0

ISO="dist/vincent-debian-13.6.0-amd64-build-0011.iso"
TS="$(date +%Y%m%d-%H%M%S)"

sh installer/debian13/inspect-image.sh "$ISO" \
  2>&1 | tee "logs/inspect-image-${TS}.log"

status=${PIPESTATUS[0]}
echo "INSPECT_EXIT_STATUS=${status}" | tee -a "logs/inspect-image-${TS}.log"
test "$status" -eq 0

sha256sum "$ISO"
cat "${ISO}.manifest.json"
```

Confirm the manifest records the exact source commit, `build_number: 0011`, `volume_id: VINCENT_B0011`, `service_account: vincent`, interactive Debian partitioning, no human login account, public-Git exact-commit runtime source, persistent console status, tty2 non-root Codex console, and no embedded secrets.

## USB flashing workflow

The owner's local Vincent checkout is `~/code/vincent/`.

For current lab work the owner swaps removable USB drives that enumerate as `/dev/sda`. Commands may target `/dev/sda` directly, but must retain an automatic guard verifying that `/dev/sda` is a removable USB whole disk and is not mounted before destructive writes.

The owner has explicitly preferred this `/dev/sda` workflow over requiring a per-device `/dev/disk/by-id` string for each swapped lab USB.

Use byte-for-byte verification after the write. Logs should include build number `0011`.

## Important historical lessons

Do not regress these fixes:

- Earlier Debian installer behavior kept asking for a username/password even with `passwd/make-user=false`. The account strategy was changed so no human account is required and root is locked before first boot.
- Earlier installers forced guided LVM/atomic partitioning; this is now superseded by the accepted decision requiring normal Debian interactive partitioning.
- Earlier first boot attempted to use a USB payload as runtime authority. Current runtime authority is the exact public Git commit; USB embeds bootstrap/evidence needed to start safely.
- Earlier bootstrap failed because DNS/GitHub was not ready. Network readiness/retry and dashboard diagnostics were added.
- Earlier service-account tool checks used identities/environments without valid HOME/XDG context. All Vincent service execution paths must use the dedicated `vincent` environment consistently.
- Do not use `nobody` for Codex or tools that expect a valid home directory.
- Generated local `*.egg-info` files must not cause migration-boundary validation failures; validation should evaluate tracked repository content rather than untracked local build products.

## Branch and merge policy for this work

Treat `workstream/iso-decisions-reconcile` as the active ISO development branch until physical validation is complete and PR #2 is explicitly accepted for integration.

Do not resurrect or independently develop on older branches such as `workstream/iso-self-test-console` or old `migration/ws2-*` branches. They are historical evidence/provenance unless a specific missing change must be recovered.

Before merging to `main`:

- current exact tip passes `scripts/validate.sh`;
- ISO build and inspection pass;
- manifest/build-number consistency passes;
- secret/obsolete-name checks pass;
- a physical install reaches the intended self-test/dashboard state;
- the owner accepts the resulting state.

## Definition of success for the next physical test

At minimum, the next test should prove:

- build `0011` is visible on the worker dashboard;
- source commit matches the ISO manifest;
- no human login is required;
- normal Debian partitioning remains available;
- networking reaches GitHub with retry behavior if needed;
- exact public Git commit is installed;
- `vincent` service-account toolchain setup completes without HOME/group errors;
- Codex installs and validates under the Vincent service identity;
- unattended self-test completes or, if it fails, the dashboard presents a photographically useful specific error;
- tty2 interactive Codex console becomes available after Codex installation.

## Reporting discipline

Every material change should be committed and pushed before another physical image is built. Record the exact commit and build number used for every physical test. Update this handoff whenever the current failure, branch tip, build number, or accepted decision checkpoint changes materially.
