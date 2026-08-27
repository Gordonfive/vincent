# Vincent

Vincent is a Linux-first platform for turning ordinary computers into reproducible AI development workers.

The product name is **Vincent**. It is not an acronym. Lowercase `vincent` is used for commands, packages, service identities, paths, configuration keys, and other technical identifiers where lowercase is conventional.

Vincent provides the Debian-based installer, first-boot/runtime software, local worker services, diagnostics, update mechanisms, Git/project connection, AI-provider adapters, and the execution environment used for bounded development work.

A fresh Vincent installation is independently functional. It can install, boot, diagnose itself, maintain Debian and its toolchain, update Vincent from its trusted public release channel, and reach an unassigned READY state without Mission Control.

Mission Control is a separate optional control-plane product for managed fleets. Project repositories remain authoritative for their own source, requirements, instructions, tests, and durable project artifacts.

Vincent is currently developed in a **private repository** under [ADR-0014](docs/decisions/ADR-0014-private-development-public-release.md). It is intended for a later deliberate public/open-source release after the required release-content and security review.

## Documentation

Start with:

- [`docs/README.md`](docs/README.md) — documentation index and authority model
- [`docs/PRODUCT.md`](docs/PRODUCT.md) — product definition, goals, and boundaries
- [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) — numbered product requirements
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — system architecture
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — Vincent product/release roadmap
- [`docs/STATUS.md`](docs/STATUS.md) — current implementation and test state
- [`docs/decisions/README.md`](docs/decisions/README.md) — Architecture Decision Record index
- [`AGENTS.md`](AGENTS.md) — instructions for coding/AI agents working in this repository
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — development and repository workflow
- [`SECURITY.md`](SECURITY.md) — security reporting and repository security rules

The overall Vincent + Mission Control program roadmap is owned by the private Mission Control program repository. This repository's roadmap covers Vincent only.

## Repository boundary

This repository owns reusable Vincent software and public-release-safe documentation, including:

- Debian installer/ISO tooling and reproducible build inputs;
- first-boot and local runtime components;
- worker self-tests, status, logging, network recovery, and diagnostics;
- trusted Vincent update logic;
- generic Git/project connection behavior;
- AI-provider adapter interfaces and provider-specific local enrollment integration;
- tests, schemas, operations documentation, release metadata, and release artifacts.

This repository must never contain private fleet state, private project operating state, reusable credentials, authentication caches, private keys, production secrets, or owner-specific infrastructure configuration.

## Versioning and license

Vincent uses independent [Semantic Versioning](https://semver.org/) for software releases. Installer build numbers are separate immutable provenance identifiers and are never reused as Vincent software versions.

Vincent is licensed under the **Mozilla Public License 2.0 (MPL-2.0)**. Modifications to MPL-covered Vincent source files remain available under MPL when distributed, while separate surrounding integrations may use other licenses subject to their own terms.
