from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from release_sentinel.checks import CheckResult, run_checks


def write_file(root: Path, relative_path: str, content: str = "ok\n") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class ReleaseReadinessChecksTest(unittest.TestCase):
    def test_missing_required_maintainer_files_fail(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_file(root, "README.md", "# Example\n")

            results = run_checks(root)

        failing = {result.id for result in results if not result.passed}
        self.assertIn("required-docs", failing)

    def test_healthy_repository_passes_core_checks(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_file(root, "README.md", "# Example\n")
            write_file(root, "CONTRIBUTING.md", "# Contributing\n")
            write_file(root, "SECURITY.md", "# Security\n")
            write_file(root, "CHANGELOG.md", "# Changelog\n\n## 0.1.0\n- Initial release\n")
            write_file(root, "pyproject.toml", "[project]\nname = \"example\"\n")
            write_file(root, ".github/workflows/ci.yml", "name: CI\n")
            write_file(root, "tests/test_example.py", "def test_example():\n    assert True\n")

            results = run_checks(root)

        self.assertTrue(all(result.passed for result in results), results)

    def test_changelog_without_version_heading_fails(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_file(root, "README.md", "# Example\n")
            write_file(root, "CONTRIBUTING.md", "# Contributing\n")
            write_file(root, "SECURITY.md", "# Security\n")
            write_file(root, "CHANGELOG.md", "# Changelog\n\n- Notes without release heading\n")
            write_file(root, "pyproject.toml", "[project]\nname = \"example\"\n")
            write_file(root, ".github/workflows/ci.yml", "name: CI\n")
            write_file(root, "tests/test_example.py", "def test_example():\n    assert True\n")

            results = run_checks(root)

        changelog = next(result for result in results if result.id == "changelog")
        self.assertFalse(changelog.passed)

    def test_privacy_scan_flags_private_identity_strings(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            private_email = "private@example.invalid"
            write_file(root, "README.md", f"contact {private_email} for help\n")

            results = run_checks(root, private_patterns=[private_email])

        privacy = next(result for result in results if result.id == "privacy-scan")
        self.assertFalse(privacy.passed)
        self.assertIn("private identity", privacy.detail.lower())

    def test_privacy_scan_passes_when_no_patterns_are_configured(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            write_file(root, "README.md", "contact private@example.invalid for help\n")

            results = run_checks(root)

        privacy = next(result for result in results if result.id == "privacy-scan")
        self.assertTrue(privacy.passed)
        self.assertIn("No private identity patterns configured", privacy.detail)


class CheckResultTest(unittest.TestCase):
    def test_check_result_serializes_to_dict(self) -> None:
        result = CheckResult(
            id="docs",
            title="Required docs",
            passed=True,
            detail="All required docs are present.",
        )

        self.assertEqual(
            result.to_dict(),
            {
                "id": "docs",
                "title": "Required docs",
                "passed": True,
                "detail": "All required docs are present.",
            },
        )


if __name__ == "__main__":
    unittest.main()
