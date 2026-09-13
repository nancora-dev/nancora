# Error Handling — Nancora Python Library

Nancora provides a clean exception hierarchy for user input and pipeline error handling.

## Exception Hierarchy

All Nancora exceptions derive from `NancoraError`:

```text
NancoraError (base exception)
├── AnalysisError
│   ├── InputError
│   └── ConfigurationError
├── DataError
└── ReportError
```

## Exception Types

### `InputError`

Raised when input arguments or dataset objects fail validation.

**Common Scenarios**:
- Passing `None` or non-DataFrame objects to `explore()`.
- Passing an empty DataFrame (`0` rows).
- Specifying a `target` column that does not exist in `df.columns`.
- Specifying a `target` parameter that is not a string.

```python
import nancora as nc

try:
    nc.explore(None)
except nc.InputError as e:
    print(f"Caught input error: {e}")
```

### `ConfigurationError`

Raised when exploration parameters are out of allowed bounds.

**Common Scenarios**:
- Passing `max_analyses <= 0` or non-integer values.

### `DataError`

Raised when dataset profiling or IO file parsing fails.

### `ReportError`

Raised when HTML report rendering or writing fails.

## Handling Nancora Exceptions

To catch any library failure:

```python
import nancora as nc

try:
    result = nc.explore(df, target="my_column")
except nc.NancoraError as err:
    print(f"Nancora error: {err}")
```
