# Project Start Here

This file is retained as a compatibility entry point. New contributors and agents should use `docs/README.md` as the documentation index.

## Start sequence

1. Read `AGENTS.md`.
2. Read `docs/README.md` and `docs/STATUS.md`.
3. Read `docs/DECISIONS.md` and `docs/ROADMAP.md`.
4. Inspect current branches, issues, and pull requests before acting, especially for installer/ISO work that may be ahead of `main`.
5. Read task-specific architecture, operations, security, protocol, and validation documentation.
6. Consult `Gordonfive/mission-control` only when work crosses into private fleet/control-plane concerns.

## Repository roles

- Vincent is PUBLIC and owns the generic worker platform, Debian installer/ISO tooling, first boot, self-tests, diagnostics, update logic, runtime, public-safe documentation, tests, and releases.
- Mission Control is PRIVATE and owns optional private fleet enrollment approval, authorization, inventory, roles, repository scopes, assignments, and private coordination.
- Individual project repositories own project-specific source, requirements, tests, and task authority.

## Current operating model

A fresh Vincent installation is generic. It must boot, self-test, update, and reach an unassigned READY state without automatically contacting or requiring Mission Control. The operator later selects and authenticates an appropriate Git control/project source.

## Safety boundaries

- Never commit raw tokens, passwords, private keys, authentication caches, reusable enrollment credentials, production data, or private fleet state to public Vincent.
- Destructive installer-media writes require exact-target identification and applicable authorization.
- Do not infer physical-test success from a successful image build alone.
- Accepted timestamped decisions override older implementation assumptions or historical specification text.

## Recovery principle

Normal project recovery depends on the current Vincent and Mission Control repositories plus active branches, issues, pull requests, releases, and validation evidence. Prior chat history and retired migration repositories are not operational dependencies.
