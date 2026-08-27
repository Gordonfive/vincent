#!/usr/bin/env python3
"""Repository validation for Vincent documentation and public-boundary invariants."""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md",
    "README.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
    "docs/README.md",
    "docs/PRODUCT.md",
    "docs/REQUIREMENTS.md",
    "docs/ARCHITECTURE.md",
    "docs/ROADMAP.md",
    "docs/STATUS.md",
    "docs/decisions/README.md",
    "docs/history/SPECIFICATION_TRACEABILITY_2026-08-27.md",
]
RETIRED_PATHS = [
    "docs/PROJECT_START_HERE.md",
    "docs/CONTINUATION_HANDOFF.md",
    "docs/PLANNED_FEATURES.md",
    "docs/DECISIONS.md",
    "docs/MIGRATION.md",
    "docs/project-dna",
    "docs/specification",
]
OBSOLETE_ACTIVE_TERMS = (
    "Verified Intelligent Node for Codex Execution, Networking, and Tasks",
    "Verified Intelligent Networked Codex Execution Node Technology",
    "Gordonfive/GitBoy",
    "Gordonfive/codex-worker-platform",
    "VINCENT-DEC-",
    "Project DNA",
)
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
REQ = re.compile(r"\bVIN-REQ-\d{4}\b")
ADR_FILE = re.compile(r"ADR-(\d{4})-[a-z0-9-]+\.md$")


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        yield path


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required canonical document: {rel}")
    for rel in RETIRED_PATHS:
        if (ROOT / rel).exists():
            failures.append(f"retired document/path still present: {rel}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        if any(part.lower() in PRIVATE_PATH_PARTS for part in rel.parts):
            failures.append(f"private-state path in public repository: {rel}")

    adr_numbers: dict[str, pathlib.Path] = {}
    history_dir = ROOT / "docs/history"

    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")

        if path.suffix == ".md" and history_dir not in path.parents:
            for token in OBSOLETE_ACTIVE_TERMS:
                if token in text:
                    failures.append(f"obsolete active documentation term {token!r}: {path.relative_to(ROOT)}")

        if path.parent == ROOT / "docs/decisions" and path.name != "README.md":
            match = ADR_FILE.fullmatch(path.name)
            if not match:
                failures.append(f"invalid ADR filename: {path.relative_to(ROOT)}")
            else:
                number = match.group(1)
                if number in adr_numbers:
                    failures.append(
                        f"duplicate ADR number {number}: {adr_numbers[number].relative_to(ROOT)} and {path.relative_to(ROOT)}"
                    )
                adr_numbers[number] = path

        if path.suffix == ".md":
            for raw in MARKDOWN_LINK.findall(text):
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

    requirements = (ROOT / "docs/REQUIREMENTS.md").read_text(encoding="utf-8")
    ids = REQ.findall(requirements)
    if len(ids) != len(set(ids)):
        failures.append("duplicate VIN-REQ identifier in docs/REQUIREMENTS.md")

    matrix = (ROOT / "docs/history/SPECIFICATION_TRACEABILITY_2026-08-27.md").read_text(encoding="utf-8")
    section_numbers = [int(n) for n in re.findall(r"^\| (\d+) \|", matrix, flags=re.MULTILINE)]
    if section_numbers != list(range(1, 261)):
        failures.append("specification traceability matrix does not contain exactly sections 1..260")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("Vincent canonical document/link/requirement/ADR/public-boundary checks: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
