from pathlib import Path
from tempfile import TemporaryDirectory
import io
import json
import unittest

from release_sentinel.cli import main


class CliTest(unittest.TestCase):
    def test_json_output_returns_zero_for_healthy_repo(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_healthy_repo(root)
            stdout = io.StringIO()

            exit_code = main(["--root", str(root), "--format", "json"], stdout=stdout)

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["summary"]["failed"], 0)
        self.assertGreaterEqual(payload["summary"]["passed"], 1)

    def test_text_output_returns_one_for_failing_repo(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Broken\n", encoding="utf-8")
            stdout = io.StringIO()

            exit_code = main(["--root", str(root)], stdout=stdout)

        self.assertEqual(exit_code, 1)
        self.assertIn("FAIL", stdout.getvalue())

    def test_private_pattern_option_flags_matching_text(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_healthy_repo(root)
            (root / "README.md").write_text("# Example\ncontact private@example.invalid\n", encoding="utf-8")
            stdout = io.StringIO()

            exit_code = main(
                ["--root", str(root), "--private-pattern", "private@example.invalid"],
                stdout=stdout,
            )

        self.assertEqual(exit_code, 1)
        self.assertIn("Private identity scan", stdout.getvalue())

    @staticmethod
    def _write_healthy_repo(root: Path) -> None:
        files = {
            "README.md": "# Example\n",
            "CONTRIBUTING.md": "# Contributing\n",
            "SECURITY.md": "# Security\n",
            "CHANGELOG.md": "# Changelog\n\n## 0.1.0\n- Initial release\n",
            "pyproject.toml": "[project]\nname = \"example\"\n",
            ".github/workflows/ci.yml": "name: CI\n",
            "tests/test_example.py": "def test_example():\n    assert True\n",
        }
        for relative_path, content in files.items():
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
