# Privacy Scan

Release Sentinel can scan for maintainer-configured private identity strings before public release.

## No Default Private Patterns

The tool does not ship with maintainer-specific names, emails, domains, handles, or organizations. This avoids embedding private identity assumptions in the public package.

## CLI Patterns

Pass one or more private patterns directly:

```bash
release-sentinel --root . --private-pattern "private@example.invalid"
```

## Patterns File

Add a local file named `.release-sentinel-private-patterns` at the repository root:

```text
# comments and blank lines are ignored
private@example.invalid
internal-domain.example
```

Then run:

```bash
release-sentinel --root .
```

## File Types

The scan currently reads text-like files with these suffixes:

- `.md`
- `.py`
- `.toml`
- `.yml`
- `.yaml`
- `.txt`

It ignores `.git`, virtual environments, Python caches, and test caches.

## Limits

The privacy scan is a release-readiness guardrail, not a secret scanner. It does not replace tools designed for credentials, tokens, or high-volume history scanning.
