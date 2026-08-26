# Vincent ISO Branch Consolidation — 2026-08-26

Decision checkpoint: `2026-08-26T08:30:34-08:00`
Roadmap checkpoint: `2026-08-26T08:30:34-08:00`

## Consolidation branch

`workstream/iso-decisions-reconcile`

The branch starts from current `main` and reconciles active Workstream 2 implementation with the current decision register rather than merging superseded behavior verbatim.

## Histories explicitly joined

Merge commit `67acab649ccd433a0919a51689bf1840a3455da4` joins:

- current-main reconciliation history;
- `workstream/iso-self-test-console` at `9e1448dc8bb15b79c5b57588f6f99c8389e8f53e`;
- `migration/ws2-build-fc032f8` at `869e4542b5a514f3aba15b53e5c0d3595ca6e643`;
- `workstream/migration-completion-audit` at `c071b2358a70cd2fe7b99cd67f5d705110dfa343`.

Other migration/workstream branches inspected were already ancestors of current `main` or contained preserved legacy history. Their refs remain for provenance and are not used as independent active implementation lines.

## Reconciliation choices

Current accepted decisions control conflicts:

- service Unix identity is `vincent`;
- no conventional human installer account is required;
- root is locked before first boot;
- disk partitioning remains the normal interactive Debian installer workflow; no Vincent-forced LVM/guided/atomic recipe remains;
- first boot fetches the exact embedded public Git commit with network retry;
- tty1 provides persistent build-aware status and live work output;
- tty2 provides optional non-root interactive Codex execution;
- every ISO build uses a monotonically increasing build number;
- build number is propagated to filename, ISO volume/media identity, manifest/checksums, installed metadata, status screen, and CI evidence.

Build sequence is initialized at `0001` in `installer/debian13/BUILD_NUMBER`.

## Remaining gate

Do not move `main` to this branch until `scripts/validate.sh` passes from the exact branch tip and the build/inspection pipeline confirms build-number consistency and the decision-compliant installer behavior.
