# Vincent Current Status

**Status date:** 2026-08-27 (America/Sitka)

This file records temporary/current implementation and validation state. It is not a product specification or permanent historical archive.

## Repository state

- `main` remains the current default integration branch while documentation/ISO reconciliation is in progress.
- This documentation reset is being developed on `docs/canonical-docs-reset-20260827` from current `main`.
- Active installer/ISO implementation and physical-test work remains on `workstream/iso-decisions-reconcile`; latest observed tip during this reset: `14e6d94e2ddea210a58ce866802e1c55f135befc`.
- Current AI-provider enrollment design input exists on `docs/ai-provider-enrollment-20260827`; its accepted provider-boundary content is being incorporated into `PRODUCT.md`, requirements and ADR-0011 rather than retained as a permanent branch/roadmap fork.
- Earlier `docs/documentation-cleanup-20260827` is superseded by this current-main reconstruction and must not be merged as-is.

Target branch policy after reconciliation: `main` is the only permanent branch; temporary PR branches are deleted after integration/supersession.

## Current installer/worker development

The installer workstream is actively validating/correcting the Debian physical installation path. Current accepted/implemented direction includes:

- operator-controlled network and storage/partitioning choices;
- active installer USB exclusion from target disks;
- dedicated locked `vincent` runtime service identity;
- unique installer build provenance and ISO-safe media identities;
- separate installer provenance versus current Vincent software version;
- runtime Ethernet/Wi-Fi resilience and network diagnostics;
- installer network-preflight evidence for physical DNS/interception/Debian-source failures;
- local status/diagnostic/console surfaces and non-secret evidence collection.

Current implementation details remain authoritative on the active ISO branch until its tested code is reconciled into `main`; product behavior is represented in the canonical requirements/ADRs so documentation no longer depends on branch-local decision-number collisions.

## Physical development strategy

Two physical roles are intentionally different during current development:

- **Large workstation:** persistent first useful Vincent worker; keep online for real bounded work and Mission Control development rather than repeatedly reimaging it for routine installer regression testing.
- **Old laptop:** expendable physical installer test target for repeated clean installations, networking/storage/first-boot changes and destructive failure-path testing.

Later, after the persistent workstation has performed useful work and required durable state exists elsewhere, deliberately destroy/reinstall its local worker state as the meaningful worker-impermanence/recovery acceptance test.

This is temporary lab/test strategy, not permanent product architecture.

## Documentation reset

Owner-approved documentation/governance changes being applied:

- Vincent is the product name; no acronym/backronym.
- MPL-2.0 for Vincent.
- conventional `PRODUCT.md` + numbered `REQUIREMENTS.md` replace Project DNA and the 260-section monolithic specification;
- ADRs replace the mixed `DECISIONS.md`/`VINCENT-DEC-*` register;
- permanent `PROJECT_START_HERE.md`, `CONTINUATION_HANDOFF.md`, and `PLANNED_FEATURES.md` are retired;
- GitHub issues are the unscheduled backlog;
- Mission Control owns the overall program roadmap; Vincent roadmap is product-specific;
- current/historical migration/reset reports are distilled then removed from the active tree;
- repository Wiki is disabled; repository Markdown is authoritative;
- independent SemVer and release-level `CHANGELOG.md`;
- `main` only permanent branch, short-lived PR branches, squash merge standard;
- main protection target: PR + required CI, no force push/deletion, no mandatory approving reviewer yet;
- outside contributions intentionally deferred until approximately 1.0 or later;
- Mission Control naming is reserved for the separate control-plane product; Vincent-local internals using legacy `mission_control` naming are implementation debt tracked separately.

## Current blockers / next integration gates

1. Complete the historical 260-section traceability/distillation pass and remove the obsolete specification only after every section has a recorded disposition.
2. Reconcile active ISO-branch implementation into the new requirements/ADR model without losing newer installer fixes.
3. Replace stale operations docs and remove migration/reset/handoff/start-here/planned-feature documents.
4. Add/verify MPL-2.0 license metadata, changelog and contribution workflow.
5. Validate documentation links/IDs/obsolete terminology and open a fresh PR from this branch.
6. Integrate or supersede remaining temporary branches, then delete them per trunk-based policy.

## Not currently authorized by documentation status alone

Documentation changes do not themselves authorize destructive flashing/reinstallation, production actions, credential expansion, protected merges/releases, or other high-impact operations that retain explicit operator gates.
