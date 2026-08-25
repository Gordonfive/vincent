#!/bin/sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repository_root"

PYTHONPATH=worker python3 -m unittest discover -s tests -q
git diff --check
python3 scripts/check_migration_boundaries.py

wheel_directory=$(mktemp -d)
trap 'rm -rf "$wheel_directory"' EXIT HUP INT TERM
python3 -m pip wheel --no-deps --no-build-isolation --wheel-dir "$wheel_directory" .
find "$wheel_directory" -maxdepth 1 -type f -name '*.whl' -print
