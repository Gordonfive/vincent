"""CAS-like publication of authoritative task-state files."""

from __future__ import annotations

import json
from pathlib import Path

from .models import Task
from .publication import GitPublisher, PublicationError, PublicationResult


class TaskRepository:
    def __init__(self, repository: Path, *, branch: str = "main", tasks_path: str = "coordination/tasks") -> None:
        self.repository = repository.resolve()
        self.branch = branch
        self.tasks_path = tasks_path
        self.publisher = GitPublisher(self.repository)

    def publish(self, task: Task, *, expected_commit: str) -> PublicationResult:
        path = (self.repository / self.tasks_path / f"{task.task_id}.json").resolve()
        if self.repository not in path.parents:
            raise PublicationError("task path escapes repository")
        current = self.publisher._git("rev-parse", "HEAD").stdout.strip()
        if current != expected_commit:
            raise PublicationError("coordination checkout changed before task update")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(task.to_mapping(), sort_keys=True, indent=2) + "\n", encoding="utf-8")
        relative = str(path.relative_to(self.repository))
        return self.publisher.publish(
            branch=self.branch,
            expected_remote_head=expected_commit,
            paths=(relative,),
            message=f"Task {task.task_id}: {task.state.value}",
        )
