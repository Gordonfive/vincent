# Vincent Current Status

**Status date:** 2026-08-27 (America/Sitka)

This file records temporary/current implementation and validation state. It is not a product specification or permanent historical archive.

## Repository state

- `main` is the canonical integration branch and the only permanent branch.
- The documentation/governance reset was merged through PR #12 at `fb5c8df423be39d80e0effcfe28e688fd7114810`; its validation completed successfully.
- Installer/ISO implementation from the former ISO workstreams was reconciled onto `main` at `1edbe47a5248ce2a378646decae6ccfaa1c6f1ef` without restoring retired migration/handoff documentation.
- Accepted independent version/build identity is preserved in ADR-0015: Vincent `0.1.0`, installer `0.1.0`, independent monotonic build counters; the current installer candidate is build `0022`.
- Earlier standalone AI-provider, documentation-cleanup, and ISO-consolidation branches are superseded by canonical state on `main`.

Branch policy: `main` is the only permanent branch; temporary PR branches are deleted after integration or supersession once useful work is preserved.

## Current installer/worker development

The reconciled installer candidate includes current implementation for:

- operator-controlled network and storage/partitioning choices;
- active installer USB exclusion from target disks;
- dedicated locked `vincent` runtime service identity;
- unique installer build provenance and ISO/media identity;
- separate installer provenance versus current Vincent software version/build identity;
- runtime Ethernet/Wi-Fi resilience and network diagnostics;
- installer network-preflight evidence for DNS/interception/Debian-source failures;
- offline installer dependency closure so Debian installation does not depend on an Internet package mirror;
- resumable first-boot state for interrupted bootstrap;
- preserved Codex companion-runtime layout and bubblewrap dependency;
- local status/diagnostic/console surfaces and non-secret evidence collection.

Worker-internal `mission_control` package/service identifiers remain implementation naming debt tracked in issue #5. Version/build identifiers also still require full runtime/tooling wiring under issue #20.

## Carried-forward physical-test state

Historical bug/test state from the old ISO branch has been transferred into GitHub issues rather than restoring the retired permanent bug-register document.

Current verification work:

- #13 — VINCENT-BUG-0002: Nouveau boot hang; open pending reproduction/current fix.
- #14 — VINCENT-BUG-0003: transient DNS/bootstrap recovery; open pending current verification.
- #15 — VINCENT-BUG-0001: resumable first boot; fixed in code, physical verification pending.
- #16 — VINCENT-BUG-0008: duplicate Wi-Fi SSID suppression; fixed in code, physical verification pending.
- #17 — VINCENT-BUG-0009: offline installer path on intercepted Wi-Fi; fixed in code, physical verification pending.
- #18 — VINCENT-BUG-0011: Codex companion runtime; fixed in code, physical verification pending.
- #25 — verified historical fixes for BUG-0004, BUG-0005, BUG-0006, BUG-0007, and BUG-0010; retained as closed regression/provenance evidence.

A historical bug is not assumed to remain present. Each applicable issue is verified against the current reconciled build and then either retained/reopened, closed as verified fixed, or closed as obsolete/superseded with evidence.

## Physical development strategy

- **Large workstation:** persistent first useful Vincent worker; keep online for real bounded work and Mission Control development rather than repeatedly reimaging it for routine installer regression testing, except where workstation-specific regression verification is required.
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
- permanent project-start, continuation-handoff, planned-feature, and permanent bug-register documents are retired;
- GitHub issues are the unscheduled backlog and current bug/verification tracker;
- Mission Control owns the overall program roadmap; Vincent roadmap is product-specific;
- migration/reset/prototype reports have been removed from the active tree after distillation;
- independent SemVer, `CHANGELOG.md`, contribution workflow, PR template, and trunk/squash conventions are established;
- repository validation checks canonical documents, requirement/ADR IDs, links, release-safety boundaries, historical traceability, and credential patterns;
- active canonical documentation contains no `GitBoy` references.

## Validation

Documentation-reset validation on PR #12 passed:

- 109 unit/integration tests: PASS;
- credential-pattern scan: PASS;
- canonical documentation validation: PASS.

The reconciled installer implementation passed repository validation before integration at `1edbe47a5248ce2a378646decae6ccfaa1c6f1ef`. Physical validation of installer build `0022` remains pending and must correspond to the exact source retained on `main`.

## Next technical gate

1. Resolve QA blockers that prevent a fresh installer from completing first boot reliably without depending on re-fetching its bundled Vincent payload.
2. Build the next Vincent Installer `0.1.0` candidate from the resulting exact accepted `main` commit.
3. Execute the carried-forward physical regression/verification issues on the laptop and workstation as applicable.
4. Close, retain, or reclassify each historical bug based on current evidence.

Documentation/consolidation status alone does not authorize destructive flashing/reinstallation, production actions, credential expansion, protected releases, or other high-impact operations that retain separate operator gates.
