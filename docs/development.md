# Development

```bash
pip install -e ".[dev]"
pytest
ruff check src tests
```

Python 3.10+. Src layout. CI runs Ruff and Pytest on 3.10 and 3.12.

Decision tests live in `tests/regression/test_decisions.py`. Prefer obvious synthetic relationships over threshold-tuning.
