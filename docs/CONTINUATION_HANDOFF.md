# Continuation Handoff

**Updated:** 2026-08-26T09:37:00-08:00

Git is the durable source of truth. Chat history is disposable.

## Current immediate work

The active task is Vincent ISO creation and physical installation testing.

For the exact current state, read:

- `docs/handoffs/ISO_CREATION_HANDOFF_2026-08-26.md`
- `docs/DECISIONS.md`
- `docs/ROADMAP.md`
- `docs/PROJECT_START_HERE.md`
- `AGENTS.md`

The active ISO branch is:

```text
workstream/iso-decisions-reconcile
```

Current source tip at this handoff:

```text
eef301e42d37073d43808b4b66090e2bdad492f5
```

Current build number:

```text
0011
```

Decision checkpoint:

```text
2026-08-26T08:30:34-08:00
```

Before any build, refresh `docs/DECISIONS.md` for newer accepted decisions.

## Repository roles

- `Gordonfive/vincent` — public worker platform, ISO, installer, first boot, runtime, tests, public-safe docs and releases.
- `Gordonfive/mission-control` — private fleet/control-plane state, authorization, assignments and private coordination.

Do not copy private Mission Control state or secrets into public Vincent.

## ISO workstream status

ISO work from older branches has been consolidated onto `workstream/iso-decisions-reconcile`. Draft PR #2 targets `main` but must not be merged until the current physical-test path is validated and accepted.

Current accepted design includes:

- non-human `vincent` Unix service identity;
- no conventional human installer account/password;
- normal Debian interactive partitioning; Vincent does not force LVM or a partition recipe;
- exact public-Git commit bootstrap with network retries;
- tty1 self-test/status dashboard;
- tty2 optional non-root Codex console;
- monotonically increasing build numbers propagated through ISO/media/manifest/installed worker status.

The latest physical build `0011` successfully displayed build number, source commit, network state, worker identity and live output, but failed in the service-account toolchain stage with a HOME/login-context error. Commit `eef301e42d37073d43808b4b66090e2bdad492f5` is the current untested correction.

See `docs/handoffs/ISO_CREATION_HANDOFF_2026-08-26.md` for the exact failure, correction, validation/build commands, `/dev/sda` lab flashing workflow, and physical-test acceptance criteria.

## Operating rules

- Git wins over chat summaries.
- Fetch before deciding what is current.
- Do not build from stale decisions.
- Large commands should display progress and save complete timestamped logs with `tee`.
- Preserve and print explicit exit status.
- The owner should not need to log into the worker or run manual diagnostic commands during normal physical testing; improve the self-test/dashboard instead.
- Record exact source commit and build number for every physical test.
