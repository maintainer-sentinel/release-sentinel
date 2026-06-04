# Contributing

Release Sentinel accepts small, well-tested changes that improve release-readiness checks for open-source maintainers.

## Good Contributions

- Add a check that catches a common release or maintenance failure.
- Improve a check message so maintainers know exactly what to fix.
- Add tests for edge cases from real repository layouts.
- Improve documentation for setup, CI usage, or release workflows.

## Development

```bash
python3 -m pip install -e .
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Pull Request Expectations

- Keep the change narrowly scoped.
- Add or update tests for behavior changes.
- Update `CHANGELOG.md` under `## Unreleased`.
- Avoid adding dependencies unless the benefit is larger than the maintenance cost.

## Maintainer Review

Maintainers review changes for:

- clear release-readiness value
- readable failure messages
- low operational burden
- passing tests and CI
- no private or unnecessary user data collection
