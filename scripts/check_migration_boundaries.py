#!/usr/bin/env python3
"""Migration-only static checks for public Vincent."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SELF = pathlib.Path(__file__).resolve()

ACTIVE_ROOTS = [
    ROOT / ".github",
    ROOT / "bootstrap",
    ROOT / "config",
    ROOT / "installer",
    ROOT / "scripts",
    ROOT / "tests",
    ROOT / "worker",
]
ACTIVE_FILES = [ROOT / "pyproject.toml"]
OBSOLETE = ("GitBoy", "gitboy", "Gordonfive/GitBoy", "Gordonfive/codex-worker-platform")

PRIVATE_PATH_PARTS = {
    "fleet",
    "assignments",
    "dispatch",
    "private-reports",
    "authorization-state",
    "production-data",
    "credentials",
    "secrets",
}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def text_files(paths: list[pathlib.Path]):
    for path in paths:
        if not path.exists():
            continue
        if path.is_file():
            yield path
            continue
        for child in path.rglob("*"):
            if child.is_file() and ".git" not in child.parts:
                yield child


def check_obsolete_names() -> list[str]:
    failures: list[str] = []
    for path in text_files(ACTIVE_ROOTS + ACTIVE_FILES):
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


def check_public_private_boundary() -> list[str]:
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        if any(part.lower() in PRIVATE_PATH_PARTS for part in rel.parts):
            failures.append(f"private-state path in public repository: {rel}")
    return failures


def check_markdown_links() -> list[str]:
    failures: list[str] = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
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


def check_specification() -> list[str]:
    required = ROOT / "docs/specification/sections-068-092.md"
    if not required.is_file():
        return ["missing canonical docs/specification/sections-068-092.md"]
    text = required.read_text(encoding="utf-8")
    headings = re.findall(r"^# (\d+)\. ", text, flags=re.MULTILINE)
    expected = [str(number) for number in range(68, 93)]
    if headings != expected:
        return [f"specification heading sequence is {headings!r}, expected 68..92"]
    return []


def main() -> int:
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
