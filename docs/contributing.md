# Contributing to Nancora

Thank you for your interest in contributing to Nancora!

## Development Setup

1. **Fork and clone the repository**:

   ```bash
   git clone https://github.com/nancora/nancora.git
   cd nancora
   ```

2. **Create a virtual environment and install development dependencies**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Running Tests

Run the full automated test suite using `pytest`:

```bash
python -m pytest
```

Run intelligence benchmarks:

```bash
python -m benchmarks.runner
```

## Code Style & Linting

Nancora uses `ruff` for code formatting and linting, and `mypy` for static type checking:

```bash
ruff check src tests
mypy src
```

## Submitting Pull Requests

1. Create a feature branch (`git checkout -b feature/my-feature`).
2. Ensure all unit tests and benchmarks pass cleanly.
3. Commit your changes with clear, descriptive commit messages.
4. Push to your fork and submit a Pull Request.
