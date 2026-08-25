# Vincent Workstream 2 ISO validation

Date: 2026-08-25 (America/Sitka)

## Authority

- Workstream 1 accepted source: `fc032f8df1c0abde295122a8a515e9cdcf7c7b70`.
- Durable owner acceptance record: `d6fb92a6a07905dc29a1431b17d2a953abd5fbc8`.
- Destructive flash authority remains separate and requires exact-device identification and owner authorization.

## Accepted-source validation result

The accepted source was tested without substituting legacy repositories or staging content.

Repository validation passed at the accepted source:

- 112 Python tests passed.
- `git diff --check` passed.
- `vincent-worker-platform` wheel build passed.

The repository's original ISO workflow then failed before image creation because tracked installer shell scripts were mode `100644` while the workflow invoked them directly. `fetch-source.sh` returned `Permission denied` with exit status 126.

An execution-harness-only workflow was used to checkout the exact accepted source commit in detached-HEAD state and invoke the accepted scripts through `sh`. The harness did not modify the source tree used to create the image.

That exact-source build produced:

- image: `vincent-debian-13.6.0-amd64.iso`
- SHA-256: `bcebd5fed3c82f86c7259b8dd71297e99057f630698c1742e4461265b78842a2`
- Debian source SHA-256: `65273beed27b2df543b68b65630ba525cfbad8df2b12035732b2dff87d6664e7`
- embedded platform commit: `fc032f8df1c0abde295122a8a515e9cdcf7c7b70`
- installer inspection: PASS
- generated checksum verification: PASS
- manifest verification: PASS
- private-key/credential pattern scan: PASS
- embedded identity-file scan: PASS

The Debian source ISO was verified against Debian's signed checksum data before use.

## Rejection

The image is **rejected and not eligible for flashing** because the required active obsolete-name scan found tracked legacy generated metadata in the embedded platform archive:

- `worker/codex_worker_platform.egg-info/SOURCES.txt` referenced `tests/test_gitboy_cli.py` and `worker/mission_control/gitboy_cli.py`.
- `worker/codex_worker_platform.egg-info/entry_points.txt` advertised the obsolete `gitboy = mission_control.gitboy_cli:main` console command.

The build/validation harness therefore terminated with `BUILD_STATUS=22`. The rejected ISO was not published as a verified artifact.

## Corrective source

Correction commit `3a6abb330fb11faffbd638b101ed11dca47f4216` was created directly on top of the accepted source. It:

- removes tracked generated `worker/codex_worker_platform.egg-info/` metadata;
- removes obsolete duplicate `worker/mission_control/gitboy_cli.py` and `tests/test_gitboy_cli.py` files;
- preserves the authoritative `vincent` console entry point in `pyproject.toml`;
- marks operational shell scripts executable;
- strengthens the ISO workflow to run the full repository validation, Debian source verification, ISO build, payload inspection, checksum/manifest verification, credential/identity scan, active obsolete-name scan, timestamped `tee` logging, and explicit final build status;
- uploads the ISO only after all gates pass and uploads non-ISO failure evidence when validation fails.

Non-destructive CI on the correction passed:

- 109 Python tests passed;
- `git diff --check` passed;
- `vincent-worker-platform` wheel build passed.

## Current gate

No USB has been identified or flashed. No destructive authorization has been requested or inferred. No release has been published and no production/project authority has been granted.

The corrected branch must receive explicit owner acceptance of its exact tip commit before a replacement ISO is treated as the authorized Workstream 2 build source.
