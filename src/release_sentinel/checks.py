from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class CheckResult:
    id: str
    title: str
    passed: bool
    detail: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "id": self.id,
            "title": self.title,
            "passed": self.passed,
            "detail": self.detail,
        }


REQUIRED_DOCS = (
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
)

def run_checks(root: str | Path, private_patterns: list[str] | None = None) -> list[CheckResult]:
    repo_root = Path(root)
    return [
        _check_required_docs(repo_root),
        _check_ci_workflow(repo_root),
        _check_tests(repo_root),
        _check_packaging(repo_root),
        _check_changelog(repo_root),
        _check_privacy_scan(repo_root, private_patterns or []),
    ]


def _check_required_docs(root: Path) -> CheckResult:
    missing = [path for path in REQUIRED_DOCS if not (root / path).is_file()]
    if missing:
        return CheckResult(
            id="required-docs",
            title="Required maintainer docs",
            passed=False,
            detail="Missing required files: " + ", ".join(missing),
        )
    return CheckResult(
        id="required-docs",
        title="Required maintainer docs",
        passed=True,
        detail="README, contributing, security, and changelog files are present.",
    )


def _check_ci_workflow(root: Path) -> CheckResult:
    workflow_dir = root / ".github" / "workflows"
    workflows = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    if not workflows:
        return CheckResult(
            id="ci-workflow",
            title="CI workflow",
            passed=False,
            detail="No GitHub Actions workflow found in .github/workflows.",
        )
    return CheckResult(
        id="ci-workflow",
        title="CI workflow",
        passed=True,
        detail=f"Found {len(workflows)} workflow file(s).",
    )


def _check_tests(root: Path) -> CheckResult:
    tests_dir = root / "tests"
    test_files = list(tests_dir.glob("test_*.py")) if tests_dir.is_dir() else []
    if not test_files:
        return CheckResult(
            id="tests",
            title="Automated tests",
            passed=False,
            detail="No Python test files found under tests/.",
        )
    return CheckResult(
        id="tests",
        title="Automated tests",
        passed=True,
        detail=f"Found {len(test_files)} Python test file(s).",
    )


def _check_packaging(root: Path) -> CheckResult:
    if not (root / "pyproject.toml").is_file():
        return CheckResult(
            id="packaging",
            title="Package metadata",
            passed=False,
            detail="Missing pyproject.toml package metadata.",
        )
    return CheckResult(
        id="packaging",
        title="Package metadata",
        passed=True,
        detail="pyproject.toml is present.",
    )


def _check_changelog(root: Path) -> CheckResult:
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        return CheckResult(
            id="changelog",
            title="Changelog format",
            passed=False,
            detail="Missing CHANGELOG.md.",
        )
    content = changelog.read_text(encoding="utf-8").lower()
    has_version_heading = re.search(r"^##\s+(v?\d+\.\d+\.\d+|unreleased)\b", content, re.MULTILINE)
    if not has_version_heading:
        return CheckResult(
            id="changelog",
            title="Changelog format",
            passed=False,
            detail="CHANGELOG.md needs a version or Unreleased heading.",
        )
    return CheckResult(
        id="changelog",
        title="Changelog format",
        passed=True,
        detail="CHANGELOG.md includes a release-oriented heading.",
    )


def _check_privacy_scan(root: Path, private_patterns: list[str]) -> CheckResult:
    normalized_patterns = [pattern.lower() for pattern in private_patterns if pattern.strip()]
    if not normalized_patterns:
        return CheckResult(
            id="privacy-scan",
            title="Private identity scan",
            passed=True,
            detail="No private identity patterns configured.",
        )

    findings: list[str] = []
    for path in _iter_text_files(root):
        content = path.read_text(encoding="utf-8", errors="ignore").lower()
        for pattern in normalized_patterns:
            if pattern in content:
                findings.append(str(path.relative_to(root)))
                break
    if findings:
        return CheckResult(
            id="privacy-scan",
            title="Private identity scan",
            passed=False,
            detail="Potential private identity strings found in: " + ", ".join(sorted(set(findings))),
        )
    return CheckResult(
        id="privacy-scan",
        title="Private identity scan",
        passed=True,
        detail="No configured private identity strings found in tracked text-like files.",
    )


def _iter_text_files(root: Path) -> list[Path]:
    ignored_parts = {".git", ".venv", "__pycache__", ".pytest_cache"}
    allowed_suffixes = {".md", ".py", ".toml", ".yml", ".yaml", ".txt"}
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        if path.suffix.lower() in allowed_suffixes:
            files.append(path)
    return files
