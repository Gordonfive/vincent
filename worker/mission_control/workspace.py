"""Workspace identity and contamination checks performed before execution."""

from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


class WorkspaceError(RuntimeError):
    """A workspace is not safe to use automatically."""


@dataclass(frozen=True, slots=True)
class WorkspaceStatus:
    root: Path
    head: str
    branch: str
    remote_url: str
    changes: tuple[str, ...]

    @property
    def clean(self) -> bool:
        return not self.changes


@dataclass(frozen=True, slots=True)
class PreparedWorkspace:
    path: Path
    branch: str
    starting_commit: str
    ddev_project: str


def stable_identifier(*parts: str, limit: int = 63) -> str:
    raw = "-".join(parts).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", raw).strip("-") or "task"
    digest = hashlib.sha256(raw.encode()).hexdigest()[:8]
    prefix_limit = max(1, limit - len(digest) - 1)
    return f"{slug[:prefix_limit].rstrip('-')}-{digest}"


class WorkspaceManager:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def task_path(self, project_id: str, worker_id: str, task_id: str) -> Path:
        return self.root / stable_identifier(project_id, worker_id, task_id)

    @staticmethod
    def repository_url(locator: str) -> str:
        if locator.startswith(("/", "./", "../", "file://", "ssh://", "https://", "git@")):
            return locator
        if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", locator):
            return f"git@github.com:{locator}.git"
        raise WorkspaceError("repository locator is not supported")

    @staticmethod
    def task_branch(task_id: str, worker_id: str) -> str:
        return f"mission-control/{stable_identifier(task_id, worker_id, limit=80)}"

    def prepare(
        self,
        *,
        project_id: str,
        repository: str,
        base_branch: str,
        worker_id: str,
        task_id: str,
    ) -> PreparedWorkspace:
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.task_path(project_id, worker_id, task_id)
        url = self.repository_url(repository)
        branch = self.task_branch(task_id, worker_id)
        if path.exists():
            status = self.inspect(path, expected_remote=url, expected_branch=branch)
            self.require_clean(status)
            self._git(path, "fetch", "--no-tags", "origin")
            remote_head = self._git(path, "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
            if remote_head and remote_head.split()[0] != status.head:
                raise WorkspaceError("remote task branch changed unexpectedly")
            return PreparedWorkspace(path, branch, status.head, stable_identifier(project_id, worker_id, task_id))
        result = subprocess.run(
            ["git", "clone", "--no-checkout", "--origin", "origin", url, str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise WorkspaceError(result.stderr.strip() or "repository clone failed")
        try:
            base_commit = self._git(path, "rev-parse", f"origin/{base_branch}")
            remote_task = self._git(path, "ls-remote", "--heads", "origin", f"refs/heads/{branch}")
            if remote_task:
                self._git(path, "switch", "--track", "-c", branch, f"origin/{branch}")
            else:
                self._git(path, "switch", "-c", branch, f"origin/{base_branch}")
            status = self.inspect(path, expected_remote=url, expected_branch=branch)
            self.require_clean(status)
            return PreparedWorkspace(path, branch, status.head, stable_identifier(project_id, worker_id, task_id))
        except Exception:
            # Preserve the incomplete clone as evidence; never delete automatically.
            raise

    @staticmethod
    def _git(path: Path, *arguments: str) -> str:
        result = subprocess.run(
            ["git", *arguments], cwd=path, text=True, capture_output=True, check=False
        )
        if result.returncode:
            raise WorkspaceError(result.stderr.strip() or "Git workspace inspection failed")
        return result.stdout.strip()

    def inspect(
        self,
        path: Path,
        *,
        expected_remote: str,
        expected_branch: str,
        expected_head: str | None = None,
    ) -> WorkspaceStatus:
        resolved = path.resolve()
        if self.root not in resolved.parents:
            raise WorkspaceError("workspace is outside the configured root")
        top = Path(self._git(resolved, "rev-parse", "--show-toplevel")).resolve()
        if top != resolved:
            raise WorkspaceError("workspace path is not the repository root")
        remote = self._git(resolved, "remote", "get-url", "origin")
        if remote != expected_remote:
            raise WorkspaceError("workspace remote does not match task repository")
        branch = self._git(resolved, "symbolic-ref", "--short", "HEAD")
        if branch != expected_branch:
            raise WorkspaceError("workspace branch does not match task branch")
        head = self._git(resolved, "rev-parse", "HEAD")
        if expected_head is not None and head != expected_head:
            raise WorkspaceError("workspace HEAD does not match expected commit")
        changes = tuple(
            line for line in self._git(resolved, "status", "--porcelain=v1", "--untracked-files=all").splitlines() if line
        )
        return WorkspaceStatus(resolved, head, branch, remote, changes)

    @staticmethod
    def require_clean(status: WorkspaceStatus) -> None:
        if status.changes:
            raise WorkspaceError("workspace contains preserved local changes")
