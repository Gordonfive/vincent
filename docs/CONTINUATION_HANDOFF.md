# Continuation Handoff — Project Reset

Date: 2026-08-25 (America/Sitka)

Purpose: allow the current ChatGPT project to be deleted without losing operational continuity.

## Mission

VINCENT — Verified Intelligent Networked Codex Execution Node Technology — is the reusable, replaceable worker platform. Mission Control is the private coordination/control plane. Git is the durable source of truth; chat is disposable.

## Immediate owner priorities

There are exactly two primary tasks:

1. **Consolidate into `Gordonfive/vincent` and `Gordonfive/mission-control`, prove preservation, then delete the legacy `Gordonfive/codex-worker-platform` and `Gordonfive/GitBoy` repositories.**
2. **Resume Vincent ISO creation and physical testing from the corrected Workstream 2 state.**

Do not revive side projects or broaden scope before these are under control.

## New-session procedure

On first connection:

1. Fetch both new repositories and all branches/tags.
2. Read `AGENTS.md`, `docs/PROJECT_START_HERE.md`, and `docs/ROADMAP.md` in both repositories.
3. Inspect all Vincent migration, legacy, and Workstream 2 branches before changing `main`.
4. Verify exact branch tips because commits may have advanced after this handoff.
5. Use separate workstreams/threads if useful, but coordinate through pushed Git state only.
6. Update these handoff/roadmap files whenever a gate materially changes so another clean session can recover again.

## Workstream A handoff — consolidation and deletion

Known preserved Vincent refs:

- `legacy/codex-worker-platform/main` -> `0f6e93bb8cccc26edf8887eb50641ae0fe1495a2`
- `legacy/codex-worker-platform/checkpoint/vincent-migration-20260825` -> `5521b3fc1fd273ffc71e47c344d6bb9083cfdb3f`
- `legacy/GitBoy/main` -> `191f21a30ddf94d6181cbfbee1206c3fc5029c66`
- `migration/codex-worker-platform` -> `c981a5be667649d282c708763d67dcb47f7b28c9`
- `migration/GitBoy` -> `5f7a90ed81c2dd5b8dd177c7adbd1cb327b35e9a`
- `migration/integrate-worker-platform` -> `d6fb92a6a07905dc29a1431b17d2a953abd5fbc8` at handoff time

The migration verification report states that native legacy histories were copied and verified, but do not assume that alone proves the legacy repositories can be deleted. Before deletion, compare all current remote branches/tags and search for any post-copy commits, unmerged documentation, issues encoded only in branches, or private control-plane content that belongs in Mission Control.

Public/private split:

- Vincent: generic worker implementation, ISO/install/bootstrap/runtime/enrollment client, tests, public-safe docs, historical public evidence.
- Mission Control: authorization and approval state, fleet inventory, roles, repository scopes, assignments, private coordination/reports, private infrastructure metadata that is safe to retain in Git.
- Raw secrets never belong in either Git repository.

The owner directive in this handoff supersedes the earlier roadmap rule that delayed old-repository deletion until ISO acceptance: once a full preservation/consolidation proof is recorded, the old repositories are to be deleted. Never delete them before that proof.

Required final evidence before deletion:

- source/destination ref inventory and equality/preservation proof;
- no useful code/history/docs exist only in legacy repos;
- public/private boundary review passes;
- secret scan passes;
- active references no longer depend on legacy repository URLs/names;
- fresh recovery exercise succeeds using only Vincent and Mission Control;
- exact commits for the completed consolidation are recorded in both repositories.

After deletion, run one more recovery/reference check and record that the deleted repositories are no longer required.

## Workstream B handoff — ISO correction and testing

Owner accepted source `fc032f8df1c0abde295122a8a515e9cdcf7c7b70` for Workstream 2. Acceptance was recorded by `d6fb92a6a07905dc29a1431b17d2a953abd5fbc8`.

The accepted source successfully produced `vincent-debian-13.6.0-amd64.iso` with SHA-256 `bcebd5fed3c82f86c7259b8dd71297e99057f630698c1742e4461265b78842a2`, but the build was rejected because obsolete GitBoy package metadata remained embedded. `BUILD_STATUS=22`. **That ISO is invalid and must not be flashed.**

Correction state:

- branch: `workstream/ws2-iso-corrections`
- correction code: `3a6abb330fb11faffbd638b101ed11dca47f4216`
- report branch tip: `4edd5e95a403d605664402a7b1dc2d5c4f53b71b`
- report: `docs/reports/VINCENT_WS2_ISO_VALIDATION.md`
- correction CI evidence: 109 Python tests passed, `git diff --check` passed, wheel build passed

The correction removes generated egg-info and obsolete duplicate GitBoy CLI material, fixes executable bits, and strengthens the ISO validation workflow. It still requires exact-source review/acceptance or consolidation into a new exact authorized source before the replacement image becomes authoritative.

Replacement ISO procedure:

1. Fetch and verify exact source commit.
2. Run full tests and `git diff --check`.
3. Build with visible progress and timestamped `tee` logs; preserve pipeline exit status and print explicit final status.
4. Verify Debian source signatures/checksums.
5. Inspect payload and embedded commit.
6. Verify generated manifest/checksum.
7. Scan for credentials, private keys, reusable enrollment material, embedded worker identities, private fleet data, and obsolete names.
8. Publish no ISO as valid unless every gate returns success.
9. Before flashing, identify the exact removable device by model, serial, transport, removability, and `/dev/disk/by-id`; authorization applies only to that exact target.
10. Fresh install using whole-disk guided LVM and one root filesystem.
11. Verify `vincent-worker-NNNNNN`, persistent network, local login, SSH, Git, GitHub CLI, Docker, DDEV, Codex, Vincent, and Python packaging.
12. Verify fresh local identity, no authority before approval, scoped enrollment/revocation, one harmless real task, and repeat clean install.

No USB had been identified or flashed at this handoff. No release had been published.

## Operating rules

- Git wins over chat summaries.
- Fetch before deciding what is current.
- Preserve unexpected work rather than resetting it away.
- Large/long commands should show progress while also saving complete logs with `tee` so failures can be reviewed after the fact.
- Never infer success from silence or a truncated terminal buffer; capture explicit exit status.
- Never copy private Mission Control state into public Vincent.
- Workers implement and report; they do not invent product direction or grant themselves authority.

## End state for the next phase

The project is ready to leave the old ChatGPT project behind when:

- these recovery docs are on the default branches of both new repositories;
- the next project can connect to both repos and recover current state from Git alone;
- further progress is recorded back into Git rather than retained only in chat.
