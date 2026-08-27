# Vincent Current Status

**Status date:** 2026-08-27 (America/Sitka)

This file records temporary/current implementation and validation state. It is not a product specification or permanent historical archive.

## Repository state

- `main` remains the current default integration branch until the canonical documentation reset merges.
- Canonical documentation/governance reset is under review in PR #12 from `docs/canonical-docs-reset-20260827`.
- Active installer/ISO implementation and physical-test work remains on `workstream/iso-decisions-reconcile`; latest observed tip during this reset: `14e6d94e2ddea210a58ce866802e1c55f135befc`.
- The standalone AI-provider documentation branch is superseded by PR #12; its accepted provider-boundary content is represented in `PRODUCT.md`, `REQUIREMENTS.md`, architecture, and ADR-0011.
- The earlier documentation-cleanup branch/PR is superseded by PR #12.

Target branch policy after reconciliation: `main` is the only permanent branch; temporary PR branches are deleted after integration/supersession.

## Current installer/worker development

The active installer workstream includes current implementation for:

- operator-controlled network and storage/partitioning choices;
- active installer USB exclusion from target disks;
- dedicated locked `vincent` runtime service identity;
- unique installer build provenance and ISO/media identity;
- separate installer provenance versus current Vincent software version;
- runtime Ethernet/Wi-Fi resilience and network diagnostics;
- installer network-preflight evidence for DNS/interception/Debian-source failures;
- local status/diagnostic/console surfaces and non-secret evidence collection.

The active ISO branch remains the implementation authority for those changes until its code is reconciled and validated against the canonical requirements/ADRs after the documentation reset.

## Physical development strategy

- **Large workstation:** persistent first useful Vincent worker; keep online for real bounded work and Mission Control development rather than repeatedly reimaging it for routine installer regression testing.
- **Old laptop:** expendable physical installer test target for repeated clean installations, networking/storage/first-boot changes, and destructive failure-path testing.

Later, after the persistent workstation has performed useful work and required durable state exists elsewhere, deliberately destroy/reinstall its local worker state as the worker-impermanence/recovery acceptance test.

This is temporary lab strategy, not permanent product architecture.

## Documentation/governance reset state

Completed on the current documentation branch:

- Vincent is the product name; no acronym/backronym.
- MPL-2.0 license added.
- conventional `PRODUCT.md` and numbered `REQUIREMENTS.md` established;
- all 260 historical specification sections have an explicit disposition in `docs/history/SPECIFICATION_TRACEABILITY_2026-08-27.md`;
- the monolithic historical specification has been removed from the active tree;
- ADRs replace the old mixed decision register;
- permanent project-start, continuation-handoff, and planned-feature backlog documents are retired;
- GitHub issues are the unscheduled backlog;
- Mission Control owns the overall program roadmap; Vincent roadmap is product-specific;
- migration/reset/prototype reports have been removed from the active tree after distillation;
- independent SemVer, `CHANGELOG.md`, contribution workflow, PR template, and trunk/squash conventions established;
- repository validation now checks canonical documents, requirement/ADR IDs, links, public/private boundary, historical traceability, and credential patterns.

## Current validation

PR #12 CI reached the full test suite successfully:

- 109 unit/integration tests: PASS;
- credential-pattern scan: PASS;
- remaining CI cleanup at the time of this status update is limited to stale documentation terminology/dead-link corrections in the canonical-document validator.

## Next integration gates

1. Obtain green CI on PR #12.
2. Squash-merge PR #12 to `main`.
3. Close/delete superseded documentation/AI-provider branches and PRs.
4. Reconcile `workstream/iso-decisions-reconcile` against the new requirements/ADRs without losing its newer installer fixes.
5. Resume physical installer validation from that reconciled implementation branch.

Documentation status alone does not authorize destructive flashing/reinstallation, production actions, credential expansion, protected releases, or other high-impact operations that retain separate operator gates.
