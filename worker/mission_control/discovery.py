"""Deterministic task discovery from a clean Git coordination checkout."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .models import ProtocolError, Task, TaskState


class DiscoveryError(RuntimeError):
    pass


PRIORITY = {"CRITICAL": 0, "HIGH": 1, "NORMAL": 2, "LOW": 3}


class GitTaskSource:
    def __init__(self, repository: Path, *, branch: str = "main", tasks_path: str = "coordination/tasks") -> None:
        self.repository = repository.resolve()
        self.branch = branch
        self.tasks_path = tasks_path

    def _git(self, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(["git", *arguments], cwd=self.repository, text=True, capture_output=True, check=False)
        if check and result.returncode:
            raise DiscoveryError(result.stderr.strip() or result.stdout.strip())
        return result

    def synchronize(self) -> str:
        if self._git("status", "--porcelain=v1", "--untracked-files=all").stdout.strip():
            raise DiscoveryError("coordination checkout is dirty")
        current = self._git("symbolic-ref", "--short", "HEAD").stdout.strip()
        if current != self.branch:
            raise DiscoveryError("coordination checkout is on the wrong branch")
        self._git("fetch", "--no-tags", "origin", self.branch)
        self._git("merge", "--ff-only", f"origin/{self.branch}")
        return self._git("rev-parse", "HEAD").stdout.strip()

    def tasks(self) -> tuple[Task, ...]:
        root = (self.repository / self.tasks_path).resolve()
        if self.repository not in root.parents:
            raise DiscoveryError("task path escapes coordination repository")
        if not root.exists():
            return ()
        tasks: list[Task] = []
        for path in sorted(root.glob("*.json")):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                task = Task.from_mapping(raw)
            except (OSError, json.JSONDecodeError, ProtocolError) as exc:
                raise DiscoveryError(f"invalid task file {path.name}: {exc}") from exc
            if path.stem != task.task_id:
                raise DiscoveryError(f"task filename does not match task_id: {path.name}")
            tasks.append(task)
        return tuple(tasks)

    def eligible(self, worker_id: str, capabilities: frozenset[str]) -> tuple[Task, ...]:
        candidates = [
            task for task in self.tasks()
            if task.state is TaskState.QUEUED
            and (task.assigned_worker is None or task.assigned_worker == worker_id)
            and set(task.required_capabilities).issubset(capabilities)
        ]
        return tuple(sorted(candidates, key=lambda task: (PRIORITY.get(task.priority, 99), task.created_at, task.task_id)))
