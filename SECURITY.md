# Security Policy

## Supported Versions

The latest tagged release receives security fixes. Pre-release versions may change quickly and should not be treated as stable policy engines.

## Reporting a Vulnerability

Please report security issues privately through GitHub's private vulnerability reporting when available. If private reporting is unavailable, open an issue with a minimal description and ask for maintainer contact before sharing exploit details.

Reports should include:

- affected version or commit
- expected behavior
- observed behavior
- reproduction steps that avoid exposing private data

## Response Targets

- Initial acknowledgement: within 7 days
- Triage decision: within 14 days
- Fix or mitigation target: based on severity and reproducibility

## Security Scope

In scope:

- incorrect checks that could hide release-critical failures
- privacy scan bypasses that expose configured private identity patterns
- workflow behavior that leaks repository data unexpectedly

Out of scope:

- social engineering
- denial-of-service against public GitHub infrastructure
- issues requiring access to a maintainer's private account
