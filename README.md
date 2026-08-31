# Vincent

Vincent is Fleet's Linux-first managed worker platform for turning ordinary computers into reproducible AI development workers.

The component name is **Vincent**. It is not an acronym. Lowercase `vincent` is used for commands, packages, service identities, paths, configuration keys, and other technical identifiers where lowercase is conventional.

Vincent provides the Debian-based installer, first-boot/runtime software, local worker services, diagnostics, update mechanisms, Git/project connection, AI-provider adapters, and the execution environment used for bounded development work.

A fresh Vincent installation is independently functional. It can install, boot, diagnose itself, maintain Debian and its toolchain, update Vincent from its trusted public release channel, and reach an unassigned READY state without CIC Station.

CIC Station is Fleet's separate optional control plane for managed workers. Project repositories remain authoritative for their own source, requirements, instructions, tests, and durable project artifacts.

## Documentation

Start with:

- [`docs/README.md`](docs/README.md) — documentation index and authority model
- [`docs/PRODUCT.md`](docs/PRODUCT.md) — component definition, goals, and boundaries
- [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) — numbered component requirements
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — system architecture
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — Vincent component/release roadmap
- [`docs/STATUS.md`](docs/STATUS.md) — current implementation and test state
- [`docs/decisions/README.md`](docs/decisions/README.md) — Architecture Decision Record index
- [`AGENTS.md`](AGENTS.md) — instructions for coding/AI agents working in this repository
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — development and repository workflow
- [`SECURITY.md`](SECURITY.md) — security reporting and repository security rules

The overall Fleet roadmap, cross-component integration issues, and Fleet governance are owned by [`logrusbox/fleet`](https://github.com/logrusbox/fleet). This repository's roadmap covers Vincent only.

## Repository boundary

This public repository owns reusable Vincent software and public-safe documentation, including:

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
