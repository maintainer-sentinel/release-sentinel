## Summary

- 

## Checklist

- [ ] Tests added or updated
- [ ] `CHANGELOG.md` updated under `## Unreleased`
- [ ] Documentation updated if behavior changed
- [ ] No private maintainer identity or secrets included

## Verification

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m release_sentinel --root .
```
