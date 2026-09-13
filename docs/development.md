# Development

```bash
pip install -e ".[dev]"
pytest
ruff check src tests benchmarks
```

Layout is `src/nancora`. Tests live under `tests/unit`, `tests/integration`, `tests/regression`.

CI: `.github/workflows/ci.yml` (Python 3.10 and 3.12).
