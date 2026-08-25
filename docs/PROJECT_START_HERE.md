# Project Start Here

Use this file to recover the Vincent / Mission Control project in a completely new ChatGPT or Codex session. Do not depend on prior chat history.

## First actions

1. Connect to and fetch both authoritative repositories:
   - `Gordonfive/vincent`
   - `Gordonfive/mission-control`
2. Read this file, then `docs/ROADMAP.md`, then `docs/CONTINUATION_HANDOFF.md` in both repositories.
3. Read each repository's `AGENTS.md` before making changes.
4. Fetch all branches and tags before assuming `main` contains all migration or ISO work.
5. Treat Git evidence as authoritative and reconcile any newer commits before acting on commit IDs recorded below.

## Repository roles

- `Gordonfive/vincent` is PUBLIC and owns the generic Vincent worker platform, Debian ISO, installer, first boot, enrollment client, runtime, tests, public-safe documentation, and releases.
- `Gordonfive/mission-control` is PRIVATE and owns fleet authorization, enrollment approval, inventory, roles, repository scopes, assignments, private coordination, and reports.
- `Gordonfive/codex-worker-platform` and `Gordonfive/GitBoy` are legacy migration sources. The owner has directed that they be deleted after verified consolidation into the two new repositories.

## Current exact Vincent state

Important refs as of 2026-08-25:

- old Vincent `main`: `c6c160e5c7776752370a424852a9be9f95ac7a23`
- accepted Workstream 1 migration source for ISO testing: `fc032f8df1c0abde295122a8a515e9cdcf7c7b70`
- durable owner acceptance record: `d6fb92a6a07905dc29a1431b17d2a953abd5fbc8`
- Workstream 2 correction code: `3a6abb330fb11faffbd638b101ed11dca47f4216`
- Workstream 2 correction/report branch tip: `4edd5e95a403d605664402a7b1dc2d5c4f53b71b`
- branch: `workstream/ws2-iso-corrections`

The first Vincent ISO built from the accepted source was rejected because the obsolete-name scan found stale generated GitBoy metadata. It must not be flashed. Read `docs/reports/VINCENT_WS2_ISO_VALIDATION.md` on `workstream/ws2-iso-corrections`.

## Two active workstreams

### A. Consolidation and legacy-repository retirement

Finish moving all useful implementation, native history, documentation, Project DNA, reports, and private control-plane state into Vincent and Mission Control. Prove the new repositories are self-sufficient. Then execute the owner's directive to delete the two legacy repositories only after preservation is verified.

### B. Vincent ISO creation and physical test

Review the Workstream 2 correction, establish one exact authorized replacement source commit, rebuild and fully inspect the Vincent ISO, then proceed through the separately gated flash and physical-install sequence.

These workstreams may be handled in separate ChatGPT threads. Coordinate only through Git; each thread must fetch current refs before acting.

## Safety boundaries

- Never put private fleet data or secrets in public Vincent.
- Never commit raw tokens, passwords, private keys, authentication caches, reusable enrollment credentials, or production data to either repository.
- Do not flash an unidentified storage device.
- Do not use the rejected ISO.
- Preserve unexpected branches or dirty work until understood.
- Destructive repository deletion is conditional on successful preservation/consolidation proof.

## Recovery goal

A fresh ChatGPT project connected only to `Gordonfive/vincent` and `Gordonfive/mission-control` must be able to determine what the system is, why it exists, what has been completed, what failed, what remains, and exactly how to continue without access to the old ChatGPT project.
