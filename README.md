# Release Sentinel

[![CI](https://github.com/maintainer-sentinel/release-sentinel/actions/workflows/ci.yml/badge.svg)](https://github.com/maintainer-sentinel/release-sentinel/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/maintainer-sentinel/release-sentinel?display_name=tag)](https://github.com/maintainer-sentinel/release-sentinel/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Release Sentinel is a small release-readiness CLI and GitHub Action for open-source maintainers. It checks whether a repository has the basic operating signals maintainers rely on before publishing: maintainer docs, security policy, CI, tests, changelog structure, package metadata, and obvious private identity leakage.

The project is intentionally dependency-light. Maintainers should be able to run it in a local checkout, a release workflow, or a downstream repository without adopting a large governance platform.

## Why Maintainers Use This

- Catch release blockers before tagging a version.
- Give contributors clear signals that a project is actively maintained.
- Keep security and contribution process files visible.
- Run the same check locally and in CI.
- Scan for maintainer-configured private identity strings before public pushes.

## Ecosystem Role

Many useful open-source projects fail quietly because maintenance evidence is scattered: a changelog in one place, a missing security policy in another, tests that exist but are not wired into CI, or personal information accidentally committed during setup. Release Sentinel gives maintainers a repeatable pre-release check that supports healthier project operations without replacing human judgment.

This repository focuses on workflows that matter to community-connected projects:

- release hygiene before tags and package publication
- maintainer documentation that helps contributors participate
- security-response visibility for users and downstream integrators
- privacy checks for maintainers operating public projects
- simple machine-readable output for bots, dashboards, and future Codex-assisted workflows

## Maintenance & Evolution Strategy

Release Sentinel is maintained as a small core with clearly scoped checks. New checks should be added only when they improve release confidence for many repositories or address a concrete maintainer workflow.

Planned evolution:

- expand documentation-quality checks without enforcing one rigid template
- add optional policy profiles for Python, JavaScript, and GitHub Action projects
- support SARIF or annotations for workflow-native reporting
- publish maintenance notes in each release so users understand behavior changes
- keep all default checks explainable and easy to override in future versions

## Operational Excellence

The repository includes the same operational files it expects from others:

- automated tests in `tests/`
- CI in `.github/workflows/ci.yml`
- release notes in `CHANGELOG.md`
- security contact process in `SECURITY.md`
- contribution process in `CONTRIBUTING.md`
- maintainer roadmap in `ROADMAP.md`
- issue and pull request templates

Codex-assisted maintenance can be used for routine tasks such as drafting check proposals, summarizing issue patterns, and reviewing release notes. Human maintainers remain responsible for final review, security decisions, and releases.

## Install

```bash
python3 -m pip install -e .
```

## Run

```bash
release-sentinel --root .
```

Example output:

```text
[PASS] Required maintainer docs: README, contributing, security, and changelog files are present.
[PASS] CI workflow: Found 1 workflow file(s).
[PASS] Automated tests: Found 2 Python test file(s).
[PASS] Package metadata: pyproject.toml is present.
[PASS] Changelog format: CHANGELOG.md includes a release-oriented heading.
[PASS] Private identity scan: No private identity patterns configured.
```

Machine-readable output:

```bash
release-sentinel --root . --format json
```

Privacy patterns can be passed directly:

```bash
release-sentinel --root . --private-pattern "private@example.invalid"
```

Or stored one per line in `.release-sentinel-private-patterns`:

```text
# comments and blank lines are ignored
private@example.invalid
internal-domain.example
```

Run directly from the source tree:

```bash
PYTHONPATH=src python3 -m release_sentinel --root .
```

## GitHub Action

Use Release Sentinel in another repository:

```yaml
name: Release readiness

on:
  pull_request:
  workflow_dispatch:

jobs:
  release-sentinel:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: maintainer-sentinel/release-sentinel@v0.1.0
```

## Checks

| Check | What it verifies |
| --- | --- |
| Required maintainer docs | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `CHANGELOG.md` exist |
| CI workflow | at least one workflow exists under `.github/workflows/` |
| Automated tests | at least one `tests/test_*.py` file exists |
| Package metadata | `pyproject.toml` exists |
| Changelog format | `CHANGELOG.md` includes a release or `Unreleased` heading |
| Private identity scan | configured private identity strings are not present in text-like files |

See `docs/checks.md` for check details and `docs/privacy.md` for privacy-scan behavior.

## What This Is Not

Release Sentinel is not a compliance framework, security scanner, or replacement for maintainer judgment. It is a fast release-readiness guardrail for common repository-health signals.

## Usage Metrics & Impact Targets

Release Sentinel is new, so the initial success measures are adoption-oriented rather than inflated:

- 10 public stars from maintainers or contributors using release workflows
- 3 forks or external workflow trials
- 5 actionable issues or check proposals from users
- 2 tagged maintenance releases with changelog entries
- 1 external repository using the GitHub Action in CI

## Contributing

See `CONTRIBUTING.md`. Useful contributions include narrowly scoped checks, clearer docs, test cases for real maintainer workflows, and bug reports with reproducible repository layouts.

## Security

See `SECURITY.md`. Do not disclose security issues publicly until they have been triaged.

## License

MIT. See `LICENSE`.
