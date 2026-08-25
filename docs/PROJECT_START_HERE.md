# Project Start Here

Use this file to recover the Vincent / Mission Control project in a completely new ChatGPT or Codex session. Prior chat history and legacy repositories are not required for normal recovery.

## First actions

1. Connect to and fetch both authoritative repositories:
   - `Gordonfive/vincent`
   - `Gordonfive/mission-control`
2. Read this file, `AGENTS.md`, `docs/ROADMAP.md`, and `docs/CONTINUATION_HANDOFF.md` in both repositories.
3. Treat Git evidence and explicit owner decisions as authoritative.
4. Inspect current reports before beginning a workstream.

## Repository roles

- `Gordonfive/vincent` is PUBLIC and owns the generic Vincent worker platform, Debian ISO, installer, first boot, enrollment client, runtime, tests, public-safe documentation, and releases.
- `Gordonfive/mission-control` is PRIVATE and owns fleet authorization, enrollment approval, inventory, roles, repository scopes, assignments, private coordination, and reports.
- Historical worker-platform and bootstrap repositories were migration sources only. Their known Git histories are preserved under Vincent `legacy/*` refs and they are not required for project recovery.

## Durable Vincent history

Important accepted/corrective evidence preserved in Git:

- accepted Workstream 1 source for ISO testing: `fc032f8df1c0abde295122a8a515e9cdcf7c7b70`;
- durable owner acceptance record: `d6fb92a6a07905dc29a1431b17d2a953abd5fbc8`;
- Workstream 2 correction code: `3a6abb330fb11faffbd638b101ed11dca47f4216`;
- Workstream 2 correction/report tip: `4edd5e95a403d605664402a7b1dc2d5c4f53b71b`.

The first ISO built from the accepted source was rejected. Its SHA-256 is:

`bcebd5fed3c82f86c7259b8dd71297e99057f630698c1742e4461265b78842a2`

It must never be flashed. Migration consolidation does not authorize a replacement ISO source.

## Specification preservation

The specification archive under `docs/specification/` preserves Sections 1–260. For Sections 68–92, the owner directed that the latest supplied source is authoritative where it differs: the exact newer Section 68 fragment is preserved and supersedes the conflicting older Section 68; preserved Sections 69–92 remain authoritative because no newer replacement was supplied. The precedence is recorded in `docs/specification/sections-068-092.md`.

## Safety boundaries

- Never put private fleet data or secrets in public Vincent.
- Never commit raw tokens, passwords, private keys, authentication caches, reusable enrollment credentials, or production data to either repository.
- Do not use the rejected ISO.
- Migration completion does not authorize ISO flashing, release publication, production/project credentials, worker enrollment, or destructive hardware operations.

## Recovery goal

A fresh project connected only to Vincent and Mission Control must be able to determine what the system is, why it exists, what has been completed, what failed, authority boundaries, and exactly how to continue. Migration reports in `docs/reports/` provide preservation and validation evidence.
