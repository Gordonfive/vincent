#!/usr/bin/env python3
"""Migration-only static checks for public Vincent."""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SELF = pathlib.Path(__file__).resolve()

ACTIVE_ROOTS = [ROOT / ".github", ROOT / "bootstrap", ROOT / "config", ROOT / "installer", ROOT / "scripts", ROOT / "tests", ROOT / "worker"]
ACTIVE_FILES = [ROOT / "pyproject.toml"]
OBSOLETE = ("GitBoy", "gitboy", "Gordonfive/GitBoy", "Gordonfive/codex-worker-platform")
PRIVATE_PATH_PARTS = {"fleet", "assignments", "dispatch", "private-reports", "authorization-state", "production-data", "credentials", "secrets"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def tracked_files():
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    for raw in result.stdout.split(b"\0"):
        if raw:
            yield ROOT / raw.decode("utf-8")


def active_tracked_files():
    roots = [path.resolve() for path in ACTIVE_ROOTS]
    exact = {path.resolve() for path in ACTIVE_FILES}
    for path in tracked_files():
        resolved = path.resolve()
        if resolved in exact:
            yield path
            continue
        for root in roots:
            try:
                resolved.relative_to(root)
            except ValueError:
                continue
            else:
                yield path
                break


def check_obsolete_names():
    failures = []
    for path in active_tracked_files():
        if path.resolve() == SELF:
            continue
        try:
            data = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in OBSOLETE:
            if token in data:
                failures.append(f"active obsolete name {token!r}: {path.relative_to(ROOT)}")
    return failures


def check_public_private_boundary():
    failures = []
    for path in tracked_files():
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part.lower() in PRIVATE_PATH_PARTS for part in rel.parts):
            failures.append(f"private-state path in public repository: {rel}")
    return failures


def check_markdown_links():
    failures = []
    for path in tracked_files():
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        data = path.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK.findall(data):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"link escapes repository: {path.relative_to(ROOT)} -> {target}")
                continue
            if not resolved.exists():
                failures.append(f"broken relative link: {path.relative_to(ROOT)} -> {target}")
    return failures


def check_specification():
    spec = ROOT / "docs/specification"
    required = [
        spec / "sections-068-092.md",
        spec / "sections-068-canonical-supplied-fragment.md",
        spec / "sections-068-077.md",
        spec / "sections-078-092.md",
    ]
    failures = [f"missing specification preservation file: {p.relative_to(ROOT)}" for p in required if not p.is_file()]
    if failures:
        return failures
    fragment = (spec / "sections-068-canonical-supplied-fragment.md").read_text(encoding="utf-8")
    expected_fragment_markers = ["# 68. Instructions to the First Codex", "## First assignment", "### Step 1 — Establish repository", "### Step 2 — Preserve"]
    for marker in expected_fragment_markers:
        if marker not in fragment:
            failures.append(f"canonical supplied fragment missing marker: {marker}")
    older = (spec / "sections-068-077.md").read_text(encoding="utf-8") + "\n" + (spec / "sections-078-092.md").read_text(encoding="utf-8")
    headings = [int(n) for n in re.findall(r"^# (\d+)\. ", older, flags=re.MULTILINE)]
    if headings != list(range(68, 93)):
        failures.append(f"preserved continuation heading sequence is {headings!r}, expected 68..92")
    index = (spec / "sections-068-092.md").read_text(encoding="utf-8")
    if "latest user-supplied" not in index or "No missing prose was reconstructed or invented" not in index:
        failures.append("canonical sections 068-092 index does not record owner precedence/non-reconstruction rule")
    return failures


def main():
    failures = []
    failures.extend(check_obsolete_names())
    failures.extend(check_public_private_boundary())
    failures.extend(check_markdown_links())
    failures.extend(check_specification())
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("migration boundary/reference/specification checks: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
