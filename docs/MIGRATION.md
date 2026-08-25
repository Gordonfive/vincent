# Migration to Vincent

## Source repositories

- `Gordonfive/codex-worker-platform` — authoritative implementation and ISO development history.
- `Gordonfive/GitBoy` — legacy public bootstrap policy.
- `Gordonfive/vincent` — new public worker-platform destination.
- `Gordonfive/mission-control` — new private fleet-control destination.

## Migration rules

1. Do not delete, rewrite, or archive either legacy repository until the new repositories contain verified replacements.
2. Preserve useful Git history when moving implementation into Vincent.
3. Reconcile every uncommitted workstation change before migration.
4. Replace user-facing GitBoy naming with Vincent.
5. Keep temporary internal compatibility identifiers only when changing them immediately would create unnecessary risk; document each remaining identifier.
6. Move fleet-specific policy and configuration to Mission Control.
7. Keep project-specific instructions in the project repository.
8. Rebuild and verify the ISO after the rename.
9. Record source and destination commit hashes and validation logs.
10. Archive legacy repositories only after owner acceptance.

No repository deletion is part of this migration.
