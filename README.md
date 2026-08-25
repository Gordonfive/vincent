# Vincent

Vincent is Linux-first infrastructure for reproducible, disposable Codex development workers. Private fleet coordination belongs in the separate Mission Control control plane.

## Current phase

**M1 — first disposable worker implementation.** The M0 architecture was accepted at `8ed265b05cb9549f2deed43ed8a4612150a496fe`. Protocol, claiming, recovery, isolation, validation, publication, enrollment, and readiness components are under executable test. No physical worker provisioning, disk erasure, production access, or autonomous deployment has occurred.

Current validation:

```text
PYTHONPATH=worker python3 -m unittest discover -s tests -q
```

The staged installer does not start a worker or grant credentials. See [`docs/operations/INSTALL_AND_ENROLL.md`](docs/operations/INSTALL_AND_ENROLL.md).

The repository-only M1 implementation is ready for disposable-host verification. See [`docs/operations/M1_DEPLOYMENT_GATE.md`](docs/operations/M1_DEPLOYMENT_GATE.md).

The Debian 13 USB prototype builder is documented in [`docs/operations/BUILD_AND_FLASH_USB.md`](docs/operations/BUILD_AND_FLASH_USB.md). It retains manual target-disk selection and confirmation during destructive testing.

Start with:

1. [`docs/PROJECT_START_HERE.md`](docs/PROJECT_START_HERE.md)
2. [`docs/project-dna/PROJECT_DNA.md`](docs/project-dna/PROJECT_DNA.md)
3. [`docs/architecture/SYSTEM_ARCHITECTURE.md`](docs/architecture/SYSTEM_ARCHITECTURE.md)
4. [`docs/ROADMAP.md`](docs/ROADMAP.md)

The original specification is preserved under [`docs/specification/`](docs/specification/README.md).

## Governing rule

> Git restores the work. Project DNA restores the intent. Mission Control restores the operation.
