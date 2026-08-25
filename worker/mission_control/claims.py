"""Compare-and-swap task claim primitives.

The in-memory store proves semantics and supports supervisor tests. A GitHub/Git
adapter must provide the same create-if-absent contract before physical workers
are allowed to compete for tasks.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Protocol


class ClaimConflict(RuntimeError):
    """Another worker already owns the task claim."""


class ClaimStoreError(RuntimeError):
    """The claim store could not establish or inspect ownership safely."""


class ClaimStore(Protocol):
    def create(self, claim: "Claim") -> "Claim": ...
    def get(self, task_id: str) -> "Claim | None": ...
    def verify(self, claim: "Claim") -> bool: ...


@dataclass(frozen=True, slots=True)
class Claim:
    task_id: str
    task_revision: int
    worker_id: str
    nonce: str
    source_commit: str

    @property
    def reference(self) -> str:
        return f"refs/mission-control/claims/{self.task_id}"


class InMemoryClaimStore:
    """Thread-safe reference store with atomic create-if-absent semantics."""

    def __init__(self) -> None:
        self._claims: dict[str, Claim] = {}
        self._lock = Lock()

    def create(self, claim: Claim) -> Claim:
        with self._lock:
            if claim.reference in self._claims:
                raise ClaimConflict(claim.reference)
            self._claims[claim.reference] = claim
            return claim

    def get(self, task_id: str) -> Claim | None:
        with self._lock:
            return self._claims.get(f"refs/mission-control/claims/{task_id}")

    def verify(self, claim: Claim) -> bool:
        return self.get(claim.task_id) == claim


class GitClaimStore:
    """Atomic Git-ref claim store using create-only force-with-lease pushes."""

    def __init__(self, repository: Path, remote: str = "origin") -> None:
        self.repository = repository
        self.remote = remote

    def _git(self, *arguments: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.update(
            GIT_AUTHOR_NAME="Mission Control Worker",
            GIT_AUTHOR_EMAIL="worker@localhost.invalid",
            GIT_COMMITTER_NAME="Mission Control Worker",
            GIT_COMMITTER_EMAIL="worker@localhost.invalid",
        )
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repository,
            env=environment,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )

    def _validate_reference(self, reference: str) -> None:
        result = self._git("check-ref-format", reference)
        if result.returncode:
            raise ClaimStoreError(f"unsafe claim reference: {reference!r}")

    @staticmethod
    def _payload(claim: Claim) -> str:
        return json.dumps(
            {
                "schema_version": 1,
                "task_id": claim.task_id,
                "task_revision": claim.task_revision,
                "worker_id": claim.worker_id,
                "nonce": claim.nonce,
                "source_commit": claim.source_commit,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def create(self, claim: Claim) -> Claim:
        self._validate_reference(claim.reference)
        tree = self._git("mktree", input_text="")
        if tree.returncode:
            raise ClaimStoreError(tree.stderr.strip() or "could not create claim tree")
        commit = self._git("commit-tree", tree.stdout.strip(), input_text=self._payload(claim))
        if commit.returncode:
            raise ClaimStoreError(commit.stderr.strip() or "could not create claim object")
        object_id = commit.stdout.strip()
        push = self._git(
            "push",
            "--porcelain",
            f"--force-with-lease={claim.reference}:",
            self.remote,
            f"{object_id}:{claim.reference}",
        )
        if push.returncode:
            combined = f"{push.stdout}\n{push.stderr}".lower()
            if "stale info" in combined or "rejected" in combined:
                raise ClaimConflict(claim.reference)
            raise ClaimStoreError(push.stderr.strip() or push.stdout.strip())
        if not self.verify(claim):
            raise ClaimStoreError("remote did not retain the claim that was pushed")
        return claim

    def get(self, task_id: str) -> Claim | None:
        reference = f"refs/mission-control/claims/{task_id}"
        self._validate_reference(reference)
        lookup = self._git("ls-remote", "--refs", self.remote, reference)
        if lookup.returncode:
            raise ClaimStoreError(lookup.stderr.strip() or "remote claim lookup failed")
        if not lookup.stdout.strip():
            return None
        object_id = lookup.stdout.split()[0]
        fetch = self._git("fetch", "--no-tags", self.remote, reference)
        if fetch.returncode:
            raise ClaimStoreError(fetch.stderr.strip() or "remote claim fetch failed")
        message = self._git("show", "-s", "--format=%B", object_id)
        if message.returncode:
            raise ClaimStoreError(message.stderr.strip() or "claim object is unreadable")
        try:
            data = json.loads(message.stdout)
            if data.pop("schema_version") != 1:
                raise ValueError("unsupported claim schema")
            return Claim(**data)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ClaimStoreError("remote claim payload is invalid") from exc

    def verify(self, claim: Claim) -> bool:
        return self.get(claim.task_id) == claim
