# Project Start Here

Use this file to recover the Vincent / Mission Control project in a completely new ChatGPT or Codex session. Prior chat history is not required for normal recovery.

## First actions

1. Connect to and fetch both authoritative repositories:
   - `Gordonfive/vincent`
   - `Gordonfive/mission-control`
2. In Vincent, read in this order:
   - `AGENTS.md`
   - `docs/DECISIONS.md`
   - `docs/ROADMAP.md`
   - `docs/CONTINUATION_HANDOFF.md`
   - `docs/handoffs/ISO_CREATION_HANDOFF_2026-08-26.md` when continuing ISO work
3. In Mission Control, read its `AGENTS.md`, `docs/PROJECT_START_HERE.md`, roadmap/handoff documents, and current private coordination state as needed.
4. Treat Git evidence and explicit owner decisions as authoritative.
5. Inspect current branch tips before acting; `main` may intentionally lag an active validated workstream.

## Repository roles

- `Gordonfive/vincent` is PUBLIC and owns the generic Vincent worker platform, Debian ISO, installer, first boot, enrollment client, runtime, tests, public-safe documentation, and releases.
- `Gordonfive/mission-control` is PRIVATE and owns fleet authorization, enrollment approval, inventory, roles, repository scopes, assignments, private coordination, and reports.
- Historical worker-platform/bootstrap repositories are migration sources whose important histories are preserved in Vincent refs and migration evidence.

## Current ISO continuation point

Active branch:

```text
workstream/iso-decisions-reconcile
```

Current source commit at the 2026-08-26 ISO handoff:

```text
eef301e42d37073d43808b4b66090e2bdad492f5
```

Current build number:

```text
0011
```

Current decision checkpoint:

```text
2026-08-26T08:30:34-08:00
```

Before any build or flash preparation, check `docs/DECISIONS.md` for decisions newer than that checkpoint and reconcile them first.

The exact current physical-test state, known failure, untested correction, validation/build commands, `/dev/sda` lab flashing procedure, and acceptance criteria are in:

```text
docs/handoffs/ISO_CREATION_HANDOFF_2026-08-26.md
```

Draft PR #2 consolidates active ISO histories toward `main`. Do not assume `main` contains the current ISO implementation until that PR has been validated and accepted.

## Current ISO design constraints

The authoritative decision register currently requires:

- dedicated non-human `vincent` Unix service account;
- no conventional human installer username/password requirement;
- normal Debian interactive disk partitioning, with no Vincent-forced guided/LVM/whole-disk recipe;
- unique monotonically increasing build numbers;
- matching build number across ISO filename, ISO/USB media identity, manifests/checksums/evidence, installed metadata, and tty1 status screen;
- incremental decision refresh before builds.

Do not restore superseded behavior from older ISO branches.

## Safety boundaries

- Never put private fleet data or secrets in public Vincent.
- Never commit raw tokens, passwords, private keys, authentication caches, reusable enrollment credentials, or production data to either repository.
- Do not infer physical-test success from a successful image build alone.
- Destructive USB writes require verifying the target is the intended removable USB device.
- During normal physical ISO testing the owner should not need to log into the worker or execute diagnostic commands; the appliance should self-test and present photographically useful diagnostics.

## Recovery goal

A fresh project connected only to Vincent and Mission Control must be able to determine what the system is, current authoritative decisions, active branch and build, what has been tested, the latest failure/correction, authority boundaries, and exactly how to continue without relying on prior chat history.
