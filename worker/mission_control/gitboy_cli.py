"""Single-command interactive bootstrap for a freshly installed Vincent worker."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request


INSTRUCTIONS_URL = "https://raw.githubusercontent.com/Gordonfive/Vincent/main/bootstrap/instructions.json"
EXPECTED_BOOTSTRAP_REPOSITORY = "Gordonfive/Vincent"


def run(command: list[str], *, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, cwd=cwd, text=True)


def load_instructions() -> dict:
    request = urllib.request.Request(INSTRUCTIONS_URL, headers={"User-Agent": "Vincent/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("schema_version") != 1:
        raise RuntimeError("unsupported public bootstrap schema")
    if payload.get("product") != "Vincent":
        raise RuntimeError("bootstrap product mismatch")
    if payload.get("bootstrap_repository") != EXPECTED_BOOTSTRAP_REPOSITORY:
        raise RuntimeError("bootstrap repository mismatch")
    allowed = payload.get("allowed_repositories")
    if not isinstance(allowed, list) or EXPECTED_BOOTSTRAP_REPOSITORY not in allowed:
        raise RuntimeError("invalid repository allowlist")
    return payload


def ensure_command(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"required command is missing: {name}; first-boot provisioning did not complete")


def github_login() -> None:
    status = subprocess.run(["gh", "auth", "status", "--hostname", "github.com"], text=True)
    if status.returncode != 0:
        run(["gh", "auth", "login", "--hostname", "github.com", "--git-protocol", "https", "--web"])


def clone_or_update(repository: str, destination: Path) -> None:
    if destination.exists():
        actual = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
            cwd=destination,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        if actual != repository:
            raise RuntimeError(f"existing checkout identity mismatch: {actual}")
        run(["git", "pull", "--ff-only", "origin", "main"], cwd=destination)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    run(["gh", "repo", "clone", repository, str(destination)])


def write_local_report(root: Path, instructions: dict) -> Path:
    report_root = Path.home() / ".local" / "state" / "vincent"
    report_root.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": 1,
        "product": "Vincent",
        "hostname": os.uname().nodename,
        "platform_repository": instructions["platform_repository"],
        "platform_checkout": str(root),
        "git_available": shutil.which("git") is not None,
        "github_cli_available": shutil.which("gh") is not None,
        "codex_available": shutil.which("codex") is not None,
        "status": "OWNER_AUTHENTICATED_LOCAL_REPORT",
    }
    enrollment_request = Path("/var/lib/vincent/enrollment-request.json")
    if enrollment_request.is_file():
        report["enrollment_request"] = json.loads(enrollment_request.read_text())
    path = report_root / "enrollment-report.json"
    path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    return path


def publish_report(checkout: Path, local_report: Path, instructions: dict) -> str:
    relative_root = Path(instructions["enrollment"]["report_path"])
    if relative_root.is_absolute() or ".." in relative_root.parts:
        raise RuntimeError("unsafe enrollment report path")
    destination = checkout / relative_root / f"{os.uname().nodename}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(local_report.read_text())
    run(["git", "config", "user.name", "Vincent Enrollment"] , cwd=checkout)
    run(["git", "config", "user.email", "vincent@localhost.invalid"], cwd=checkout)
    run(["git", "add", "--", str(destination.relative_to(checkout))], cwd=checkout)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=checkout)
    if staged.returncode != 0:
        run(["git", "commit", "-m", f"Enroll {os.uname().nodename}"], cwd=checkout)
        run(["git", "push", "origin", "HEAD:main"], cwd=checkout)
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=checkout, text=True, capture_output=True, check=True
    ).stdout.strip()


def main() -> int:
    try:
        for command in ("git", "gh", "codex"):
            ensure_command(command)
        print("Vincent: reading public bootstrap instructions...")
        instructions = load_instructions()
        platform_repository = instructions.get("platform_repository")
        if platform_repository not in instructions["allowed_repositories"]:
            raise RuntimeError("platform repository is not allowlisted")
        print("Vincent: GitHub authentication may open a browser/device flow.")
        github_login()
        checkout = Path.home() / ".local" / "share" / "vincent" / "platform"
        clone_or_update(platform_repository, checkout)
        report = write_local_report(checkout, instructions)
        report_commit = publish_report(checkout, report, instructions)
        print(f"Vincent: enrollment report published at commit {report_commit}")
        print("Vincent: starting Codex. Sign in with ChatGPT when prompted.")
        return run(["codex"], check=False, cwd=checkout).returncode
    except (OSError, RuntimeError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"Vincent bootstrap failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
