# Installation — Nancora Python Library

Nancora is available on PyPI and supports Python 3.10, 3.11, and 3.12.

## Standard Installation

Install Nancora using `pip`:

```bash
pip install nancora
```

## Optional Extras

Nancora provides optional dependencies for specialized file loading:

### Excel Support (`openpyxl`)

```bash
pip install "nancora[excel]"
```

### Parquet Support (`pyarrow`)

```bash
pip install "nancora[parquet]"
```

### All Extras

```bash
pip install "nancora[excel,parquet]"
```

## Development Installation

To clone and install Nancora locally for development and testing:

```bash
git clone https://github.com/nancora/nancora.git
cd nancora
pip install -e ".[dev]"
```

Verify your installation:

```python
import nancora as nc
print(nc.__version__)  # Output: 0.1.0
```
