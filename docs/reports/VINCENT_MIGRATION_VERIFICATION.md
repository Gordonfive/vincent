# Vincent migration verification

## Provenance

- Legacy source repository: `Gordonfive/codex-worker-platform`
- Legacy checkpoint branch: `checkpoint/vincent-migration-20260825`
- Legacy checkpoint commit: `5521b3fc1fd273ffc71e47c344d6bb9083cfdb3f`
- Legacy implementation/ISO commit: `8a06965f610ceb6a4a7becfdfaae0ce528a7394e`
- Vincent base commit: `c6c160e5c7776752370a424852a9be9f95ac7a23`
- Vincent preservation branch: `migration/codex-worker-platform`
- Vincent preservation commit: `c981a5be667649d282c708763d67dcb47f7b28c9`
- Vincent integration branch: `migration/integrate-worker-platform`
- Vincent integration commit before this verification update: `e6b45e7a6daf801b1aaf777b909d4c580af257c6`
- GitBoy source commit: `191f21a30ddf94d6181cbfbee1206c3fc5029c66`
- Vincent GitBoy preservation branch: `migration/GitBoy`
- Vincent GitBoy preservation commit: `5f7a90ed81c2dd5b8dd177c7adbd1cb327b35e9a`

## Migration boundary

The public tree contains the generic installer, ISO builder, bootstrap, enrollment client, worker runtime, health, logging, reporting, tests, and documentation. It contains no fleet inventory, assignments, private policy, project instructions, or credentials.

First boot creates a fresh local Ed25519 identity and enrollment request. The `vincent` command reads only public bootstrap instructions before enrollment. It does not authenticate to GitHub, publish to a public branch, or attempt private-repository access. Private access requires a matching local authorization object containing explicit repository scopes.

VS Code/VSCodium remains optional; the implementation and validation are headless.

## Legacy-deletion gate

The Vincent preservation branches contain complete source snapshots and exact source-commit provenance. They do not yet contain the legacy repositories' complete native commit DAGs because this migration runtime could write GitHub objects but could not authenticate a Git mirror transfer. Before either legacy repository is deleted, perform and verify a mirror-history import (or preserve verified Git bundles in Vincent). Deletion remains prohibited until that evidence and a successful Vincent ISO build are both accepted by the owner.

## Validation

- Python unit suite: 112 tests passed.
- Installer shell parsing: passed.
- Public-tree credential-pattern scan: passed.
- Active documentation public/private boundary scan: passed.
- User-facing command: `vincent`.
- Stable hostname format: `vincent-worker-NNNNNN`.
- ISO output format: `vincent-debian-<version>-<architecture>.iso`.

The prior GitBoy ISO remains preserved as historical evidence. It is not a Vincent release artifact. A fresh Vincent ISO must be built from the pushed migration commit on the external Debian build host, because this scratch environment does not contain the verified Debian source ISO or `xorriso`.

The legacy GitBoy public bootstrap policy is represented by Vincent's `bootstrap/instructions.json`, public security boundary, and `vincent` enrollment command. GitBoy remains online only for old links and provenance until the post-migration Vincent ISO is proven and the owner separately authorizes legacy-repository deletion.

## Deliberately retained compatibility identifiers

- The Python package and systemd service continue to use the internal `mission_control` / `mission-control-worker` names. Renaming these stateful paths and service identifiers in the same migration would add avoidable recovery risk. They are implementation identifiers, not the public product name or the private fleet repository contents.
- `docs/reports/DEBIAN_USB_PROTOTYPE.md` retains GitBoy names because it is immutable historical physical-test evidence.
- Original specification text under `docs/specification/` is preserved as historical source material.
- Historical source/checkpoint reports retain legacy repository names where provenance requires them.

No other active user-facing GitBoy identifier is intentionally retained.
