"""Conservative Git checkpoint and publication workflow."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


class PublicationError(RuntimeError):
    """Work could not be published without violating Git safety rules."""


@dataclass(frozen=True, slots=True)
class PublicationResult:
    starting_commit: str
    ending_commit: str
    remote_commit: str
    branch: str


class GitPublisher:
    def __init__(self, repository: Path, remote: str = "origin") -> None:
        self.repository = repository.resolve()
        self.remote = remote

    def _git(self, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", *arguments],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )
        if check and result.returncode:
            raise PublicationError(result.stderr.strip() or result.stdout.strip())
        return result

    def _remote_head(self, branch: str) -> str | None:
        result = self._git("ls-remote", "--heads", self.remote, f"refs/heads/{branch}")
        return result.stdout.split()[0] if result.stdout.strip() else None

    def publish(
        self,
        *,
        branch: str,
        expected_remote_head: str | None,
        paths: tuple[str, ...],
        message: str,
    ) -> PublicationResult:
        if not paths:
            raise PublicationError("checkpoint requires explicit paths")
        current_branch = self._git("symbolic-ref", "--short", "HEAD").stdout.strip()
        if current_branch != branch:
            raise PublicationError("current branch does not match publication branch")
        starting_commit = self._git("rev-parse", "HEAD").stdout.strip()
        self._git("fetch", "--no-tags", self.remote)
        observed_remote = self._remote_head(branch)
        if observed_remote != expected_remote_head:
            raise PublicationError("remote branch changed before checkpoint")
        for relative in paths:
            candidate = (self.repository / relative).resolve()
            if self.repository != candidate and self.repository not in candidate.parents:
                raise PublicationError("checkpoint path escapes repository")
        self._git("add", "--", *paths)
        staged = self._git("diff", "--cached", "--quiet", check=False)
        if staged.returncode == 0:
            raise PublicationError("checkpoint has no staged changes")
        if staged.returncode != 1:
            raise PublicationError(staged.stderr.strip() or "could not inspect checkpoint")
        self._git("commit", "-m", message)
        ending_commit = self._git("rev-parse", "HEAD").stdout.strip()
        self._git("fetch", "--no-tags", self.remote)
        if self._remote_head(branch) != expected_remote_head:
            raise PublicationError("remote branch changed before push")
        push = self._git("push", "--porcelain", self.remote, f"HEAD:refs/heads/{branch}", check=False)
        if push.returncode:
            raise PublicationError(push.stderr.strip() or push.stdout.strip())
        remote_commit = self._remote_head(branch)
        if remote_commit != ending_commit:
            raise PublicationError("remote commit verification failed")
        return PublicationResult(starting_commit, ending_commit, remote_commit, branch)
