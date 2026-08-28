# Planning and Work Tracking

GitHub issues are the active planning system for Vincent.

## Authority

- GitHub issues: active work, defects, verification work, blockers, follow-ups, and unscheduled ideas.
- Pull requests: implementation/review state and change-specific evidence.
- Repository milestones: target Vincent releases.
- Repository labels: lightweight priority, workstream, and cross-product classification where useful.
- `docs/ROADMAP.md`: Vincent product/release outcomes.
- `docs/REQUIREMENTS.md`: stable product requirements.
- ADRs: consequential accepted decisions.
- `docs/STATUS.md`: concise current implementation/test state.

A separate GitHub Projects v2 board is intentionally not part of the authoritative workflow. Routine project management must remain directly maintainable through repository-native GitHub data rather than requiring a manually synchronized second planning surface.

## Cross-product work

CIC Station owns the canonical Vincent + CIC Station program roadmap in `logrusbox/cic-station/docs/PROGRAM_ROADMAP.md`.

Cross-product work should have one primary issue in the repository that owns the implementation or decision. Create a counterpart issue only when the other repository has distinct implementation or verification work. Do not create duplicate mirror issues merely for visibility.

## Lightweight metadata

Prefer native GitHub metadata:

- issue state for open/completed work;
- milestone for target release;
- labels for priority/workstream/cross-product classification;
- assignee only when ownership needs to be explicit;
- linked PRs and issue dependencies for implementation/blocking relationships.

Avoid story points, sprint fields, estimates, duplicated release fields, permanent handoff documents, and other metadata that requires continual manual synchronization without demonstrated value.
