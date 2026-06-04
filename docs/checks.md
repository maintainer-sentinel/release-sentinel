# Checks

Release Sentinel keeps default checks simple and explainable. A failed check should tell a maintainer what is missing and why it matters before a release.

## Required Maintainer Docs

Verifies these files exist:

- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CHANGELOG.md`

These files help contributors understand the project, report security issues safely, and review release history.

## CI Workflow

Verifies at least one workflow exists under `.github/workflows/`.

This does not require a specific CI provider or language. The goal is to confirm that the repository has an automated path for repeatable checks.

## Automated Tests

Verifies at least one Python test file exists under `tests/test_*.py`.

The current implementation is Python-focused because Release Sentinel itself is a Python package. Future profiles can support other ecosystems without changing the default behavior.

## Package Metadata

Verifies `pyproject.toml` exists.

Package metadata gives downstream users and tooling a consistent way to understand the project.

## Changelog Format

Verifies `CHANGELOG.md` includes a release-oriented heading such as:

```markdown
## Unreleased
```

or:

```markdown
## 0.1.0
```

This supports release review before tags are published.

## Private Identity Scan

Verifies configured private identity strings are not found in text-like files.

Release Sentinel does not include any maintainer-specific private strings by default. Maintainers opt in through CLI options or a local patterns file.
