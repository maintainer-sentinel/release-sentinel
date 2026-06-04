# Release Sentinel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a public, pseudonymous OSS maintainer tool that checks release-readiness and repository hygiene before maintainers publish changes.

**Architecture:** A small Python package exposes focused checks in `checks.py` and a CLI in `cli.py`. The same CLI can run locally or inside a composite GitHub Action without third-party dependencies.

**Tech Stack:** Python 3.11+ standard library, unittest, GitHub Actions composite action.

---

### Task 1: Release-Readiness Checks

**Files:**
- Create: `src/release_sentinel/checks.py`
- Create: `tests/test_checks.py`

- [ ] **Step 1: Write failing tests for required docs, CI detection, changelog, and privacy scan**
- [ ] **Step 2: Run `python3 -m unittest tests.test_checks -v` and verify failures**
- [ ] **Step 3: Implement `run_checks(root)` and `CheckResult`**
- [ ] **Step 4: Run `python3 -m unittest tests.test_checks -v` and verify pass**

### Task 2: CLI

**Files:**
- Create: `src/release_sentinel/cli.py`
- Create: `src/release_sentinel/__main__.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests for JSON output and non-zero failure exit**
- [ ] **Step 2: Implement CLI argument parsing and output**
- [ ] **Step 3: Run `python3 -m unittest discover -s tests -v`**

### Task 3: Repository Packaging and Maintainer Docs

**Files:**
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `action.yml`
- Create: `.github/workflows/ci.yml`
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/pull_request_template.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Create: `CHANGELOG.md`
- Create: `ROADMAP.md`
- Create: `MAINTAINERS.md`
- Create: `SUBMISSION.md`
- Create: `examples/healthy-repo/README.md`

- [ ] **Step 1: Add packaging and CI configuration**
- [ ] **Step 2: Add README narrative for maintenance, ecosystem role, and operations**
- [ ] **Step 3: Add contribution, security, roadmap, changelog, and submission materials**
- [ ] **Step 4: Run local tests and `python3 -m release_sentinel --root . --format json`**

### Task 4: Local Git Setup

**Files:**
- Modify: `.git/config` through git commands only

- [ ] **Step 1: Initialize local git repository**
- [ ] **Step 2: Configure repo-local pseudonymous author**
- [ ] **Step 3: Commit scaffold with a maintainer-style message**

### Task 5: GitHub Remote Setup

**Files:**
- No local file changes required unless remote URL is added.

- [ ] **Step 1: Create empty public GitHub repo under `maintainer-sentinel`**
- [ ] **Step 2: Add remote URL locally**
- [ ] **Step 3: Push only after authentication is available for the pseudonymous account**
