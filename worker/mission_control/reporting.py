"""Machine-readable task reports with a small human-readable rendering."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from .validation import ValidationResult


@dataclass(frozen=True, slots=True)
class CompletionReport:
    schema_version: int
    task_id: str
    worker_id: str
    project: str
    repository: str
    branch: str
    starting_commit: str
    ending_commit: str
    status: str
    started_at: str
    completed_at: str
    changes_summary: tuple[str, ...]
    validation: tuple[ValidationResult, ...]
    push_status: str
    unresolved_items: tuple[str, ...]
    human_decisions: tuple[str, ...]
    platform_version: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, indent=2) + "\n"

    def to_markdown(self) -> str:
        checks = "\n".join(
            f"- {'PASS' if result.passed else 'FAIL'}: `{result.name}` (exit {result.exit_status})"
            for result in self.validation
        ) or "- No validation evidence"
        changes = "\n".join(f"- {item}" for item in self.changes_summary) or "- None"
        unresolved = "\n".join(f"- {item}" for item in self.unresolved_items) or "- None"
        return (
            f"# Task {self.task_id}: {self.status}\n\n"
            f"Worker: `{self.worker_id}`  \nBranch: `{self.branch}`  \n"
            f"Commit: `{self.starting_commit}` → `{self.ending_commit}`  \n"
            f"Push: `{self.push_status}`\n\n## Changes\n\n{changes}\n\n"
            f"## Validation\n\n{checks}\n\n## Unresolved items\n\n{unresolved}\n"
        )


@dataclass(frozen=True, slots=True)
class BlockedReport:
    schema_version: int
    task_id: str
    worker_id: str
    reason_code: str
    attempted: tuple[str, ...]
    preserved_state: tuple[str, ...]
    unsafe_reason: str
    options: tuple[str, ...]
    question: str
    created_at: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, indent=2) + "\n"

    def to_markdown(self) -> str:
        attempted = "\n".join(f"- {item}" for item in self.attempted) or "- None"
        preserved = "\n".join(f"- {item}" for item in self.preserved_state) or "- None"
        options = "\n".join(f"- {item}" for item in self.options) or "- None"
        return (
            f"# Task {self.task_id}: BLOCKED\n\nReason: `{self.reason_code}`\n\n"
            f"## Attempted\n\n{attempted}\n\n## Preserved state\n\n{preserved}\n\n"
            f"## Why continuation is unsafe\n\n{self.unsafe_reason}\n\n"
            f"## Options\n\n{options}\n\n## Required decision\n\n{self.question}\n"
        )


@dataclass(frozen=True, slots=True)
class DecisionRequest:
    schema_version: int
    decision_id: str
    task_id: str
    worker_id: str
    question: str
    options: tuple[str, ...]
    recommendation: str
    blocking: bool
    status: str = "OPEN"
    response: str | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, indent=2) + "\n"


class ReportPublisher:
    def __init__(self, repository, *, branch: str = "main", reports_path: str = "coordination/reports"):
        from pathlib import Path
        from .publication import GitPublisher

        self.repository = Path(repository).resolve()
        self.branch = branch
        self.reports_path = reports_path
        self.publisher = GitPublisher(self.repository)

    def publish(self, report: CompletionReport | BlockedReport, *, expected_commit: str):
        report_type = "blocked" if isinstance(report, BlockedReport) else "completion"
        root = self.repository / self.reports_path / report.task_id
        root.mkdir(parents=True, exist_ok=True)
        json_path = root / f"{report_type}.json"
        markdown_path = root / f"{report_type}.md"
        json_path.write_text(report.to_json(), encoding="utf-8")
        markdown_path.write_text(report.to_markdown(), encoding="utf-8")
        return self.publisher.publish(
            branch=self.branch,
            expected_remote_head=expected_commit,
            paths=(str(json_path.relative_to(self.repository)), str(markdown_path.relative_to(self.repository))),
            message=f"Report {report.task_id}: {report_type}",
        )
