# Contributing

## Local Quality Gates

Run these checks before opening a pull request:

```bash
ruff check src tests
black --check src tests
mypy src/genibus
pytest --cov=genibus --cov-fail-under=85
```

## Documentation Build

```bash
sphinx-build -W docs docs/_build/html
```

## Commit Style

Use focused commits with conventional prefixes such as:

- `feat:` for features
- `fix:` for bug fixes
- `test:` for tests
- `docs:` for documentation
- `chore:` for maintenance

