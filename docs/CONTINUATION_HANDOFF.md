# Continuation Handoff — Vincent ISO Gate

Date: 2026-08-26 (America/Sitka)

## Completed migration

- Worker implementation and public-safe documentation are integrated on `migration/integrate-worker-platform`.
- Complete native histories are preserved under `legacy/codex-worker-platform/*` and `legacy/GitBoy/*`.
- Vincent `main` remains unchanged.
- Legacy repositories remain intact and may not be deleted until the Vincent ISO passes owner acceptance.

## Workstream 2 current state

Physical ISO testing is active on `workstream/iso-self-test-console`.

Decisions made during physical testing are authoritative for the continuing ISO work:

- Vincent is an appliance, not a general-purpose local-login Linux host.
- Installation must not create a human login account or ask the owner for a username/password.
- Root is locked before first boot.
- Runtime work uses the locked `mission-control` system account with explicit HOME/USER/LOGNAME/XDG environment when required by tools.
- tty1 is the persistent Vincent dashboard with fixed critical information, current task/error, self-test results, and live work output.
- tty2 is an optional interactive Codex console running as `mission-control`; it is not a root shell or local login surface.
- Normal first boot fetches and verifies the exact ISO-pinned Vincent commit from the public `Gordonfive/vincent` repository. The embedded archive is recovery/evidence material only.
- First boot must retry route, DNS, HTTPS, and Git readiness instead of treating transient network startup as a permanent failure.
- Manual physical-disk selection and final destructive confirmation remain intentional installer gates. Guided whole-disk LVM, `vincent-vg`, and the atomic recipe are automatic defaults.
- The worker must self-test and present enough information on the console for photographic evidence; local diagnostic commands are not an acceptance requirement.

See `decisions/ADR-0002-APPLIANCE-ACCOUNTS-AND-CONSOLE.md` and `ROADMAP.md`.

## Latest implementation gate

The latest implementation work on the ISO branch fixes service-account HOME/XDG handling and improves the dashboard failure state. Before building another ISO, validate the exact current branch tip with `scripts/validate.sh`, then build and inspect from that exact commit.

## Workstream 2 boundary

Do not merge Vincent `main`, publish a release, delete legacy repositories, or grant production/project access as part of physical ISO iteration. Destructive media writes remain explicitly authorized and guarded so `/dev/sda` is accepted only when it is actually a whole removable USB disk with no mounted filesystems.

## Acceptance target

Two reproducible fresh installs must reach READY without hand-entered repair commands, without a human local-login credential, and without embedded secrets. One scoped harmless real task must then complete through claim, isolated work, validation, commit, push, and non-secret reporting.
