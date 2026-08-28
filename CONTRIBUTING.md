# Contributing to Vincent

Vincent is currently in pre-1.0 development. **Unsolicited external pull requests are not accepted yet.** The public contribution policy will be revisited at approximately Vincent 1.0 or later.

This document currently defines the repository workflow for owner-directed development and authorized coding agents.

## Repository workflow

- `main` is the only permanent branch.
- Create a short-lived branch for each bounded change.
- Open a pull request to `main`.
- Keep the PR focused on one coherent objective.
- Run required tests/validation and summarize evidence in the PR.
- Resolve review/conversation issues before integration.
- Standard merge method is **squash merge**.
- Delete the source branch after merge or after it is superseded and useful work has been preserved.
- Releases use Git tags/GitHub Releases; do not create permanent release branches.

## Documentation model

Before changing product behavior, understand the canonical documents in `docs/README.md`.

- Product intent/boundaries: `docs/PRODUCT.md`
- Stable requirements: `docs/REQUIREMENTS.md`
- Consequential decisions: `docs/decisions/ADR-*.md`
- Current design: `docs/ARCHITECTURE.md` and `docs/architecture/`
- Scheduled release outcomes: `docs/ROADMAP.md`
- Temporary current state: `docs/STATUS.md`
- Operations: `docs/operations/`
- Protocol contracts: `docs/protocols/`

Do not recreate permanent handoff, project-start, planned-feature, retired product-intent, or migration-archive documents.

## Requirement and ADR identifiers

- Vincent requirements use `VIN-REQ-####`.
- ADRs use `ADR-####` within this repository.
- Once an identifier is merged into `main`, never renumber, reuse, or silently repurpose it.
- Superseded/withdrawn entries retain their identifier and explicit status/replacement reference.
- Branch-local draft ADR numbers may be reconciled before merge to avoid collisions.

## Testing and evidence

A change is not verified merely because its code exists.

Run the checks appropriate to the change, including repository tests and `git diff --check`. Installer/runtime changes require their specific validation and, where applicable, physical acceptance evidence.

Keep PR evidence concise. Large raw logs, screenshots, generated ISO/build products, CI bundles and similar artifacts should use Actions/release/local artifacts rather than ordinary Git.

## Security

Never commit:

- private keys/passwords/tokens/authentication caches;
- Wi-Fi passphrases;
- AI-provider credentials;
- reusable enrollment/bootstrap secrets;
- private CIC Station fleet/deployment state;
- production credentials/data;
- other sensitive owner/project information.

Follow `SECURITY.md` for security reporting and `AGENTS.md` for agent-specific safety constraints.

## Licensing

Vincent source is licensed under MPL-2.0. External contribution/legal terms (CLA/DCO or similar) are intentionally deferred until outside contributions are opened.
