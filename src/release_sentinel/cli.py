from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TextIO

from release_sentinel.checks import CheckResult, run_checks


DEFAULT_PRIVATE_PATTERNS_FILE = ".release-sentinel-private-patterns"


def main(argv: list[str] | None = None, stdout: TextIO | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="release-sentinel",
        description="Check whether an open-source repository is ready for release.",
    )
    parser.add_argument("--root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--private-pattern",
        action="append",
        default=[],
        help="Private identity string to scan for. May be passed multiple times.",
    )
    parser.add_argument(
        "--private-patterns-file",
        default=DEFAULT_PRIVATE_PATTERNS_FILE,
        help="File containing one private identity pattern per line.",
    )
    args = parser.parse_args(argv)

    output = stdout or sys.stdout
    root = Path(args.root)
    private_patterns = [*args.private_pattern, *_load_private_patterns(root / args.private_patterns_file)]
    results = run_checks(root, private_patterns=private_patterns)
    if args.format == "json":
        _write_json(results, output)
    else:
        _write_text(results, output)
    return 0 if all(result.passed for result in results) else 1


def _write_json(results: list[CheckResult], output: TextIO) -> None:
    passed = sum(1 for result in results if result.passed)
    failed = len(results) - passed
    payload = {
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": len(results),
        },
        "results": [result.to_dict() for result in results],
    }
    output.write(json.dumps(payload, indent=2) + "\n")


def _write_text(results: list[CheckResult], output: TextIO) -> None:
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        output.write(f"[{status}] {result.title}: {result.detail}\n")


def _load_private_patterns(path: Path) -> list[str]:
    if not path.is_file():
        return []
    patterns: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            patterns.append(stripped)
    return patterns


if __name__ == "__main__":
    raise SystemExit(main())
