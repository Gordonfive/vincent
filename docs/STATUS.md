# Vincent Current Status

**Status date:** 2026-08-27 (America/Sitka)

This file records temporary/current implementation and validation state. It is not a product specification or permanent historical archive.

## Repository state

- `main` is the canonical integration branch.
- The documentation/governance reset was merged through PR #12 at `fb5c8df423be39d80e0effcfe28e688fd7114810`.
- PR #12 validation completed successfully.
- Active installer/ISO implementation and physical-test work remains separate on `workstream/iso-decisions-reconcile`; latest observed tip during the documentation reset was `14e6d94e2ddea210a58ce866802e1c55f135befc`.
- Earlier standalone AI-provider and documentation-cleanup branches/PRs are superseded by the canonical documentation now on `main`.

Branch policy: `main` is the only permanent branch; temporary PR branches are deleted after integration or supersession once useful work is preserved.

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

The active ISO branch remains the implementation authority for those changes until its code is reconciled and validated against the canonical requirements/ADRs.

## Physical development strategy

- **Large workstation:** persistent first useful Vincent worker; keep online for real bounded work and Mission Control development rather than repeatedly reimaging it for routine installer regression testing.
- **Old laptop:** expendable physical installer test target for repeated clean installations, networking/storage/first-boot changes, and destructive failure-path testing.

Later, after the persistent workstation has performed useful work and required durable state exists elsewhere, deliberately destroy/reinstall its local worker state as the worker-impermanence/recovery acceptance test.

This is temporary lab strategy, not permanent product architecture.

## Documentation/governance state

The documentation cleanup/reorganization gate is complete on `main`:

- Vincent is the product name; no acronym/backronym.
- MPL-2.0 license is established.
- conventional `PRODUCT.md` and numbered `REQUIREMENTS.md` are authoritative;
- all 260 historical specification sections have an explicit disposition in `docs/history/SPECIFICATION_TRACEABILITY_2026-08-27.md`;
- the monolithic historical specification has been removed from the active tree;
- ADRs replace the old mixed decision register;
- permanent project-start, continuation-handoff, and planned-feature backlog documents are retired;
- GitHub issues are the unscheduled backlog;
- Mission Control owns the overall program roadmap; Vincent roadmap is product-specific;
- migration/reset/prototype reports have been removed from the active tree after distillation;
- independent SemVer, `CHANGELOG.md`, contribution workflow, PR template, and trunk/squash conventions are established;
- repository validation checks canonical documents, requirement/ADR IDs, links, public/private boundary, historical traceability, and credential patterns;
- active repository search found no remaining `GitBoy` references.

## Validation

PR #12 validation completed successfully:

- 109 unit/integration tests: PASS;
- credential-pattern scan: PASS;
- canonical documentation validation: PASS.

## Next technical gate

The next technical task, not part of this documentation closeout, is to reconcile `workstream/iso-decisions-reconcile` against the canonical requirements/ADRs before resuming physical installer validation.

Documentation status alone does not authorize destructive flashing/reinstallation, production actions, credential expansion, protected releases, or other high-impact operations that retain separate operator gates.
