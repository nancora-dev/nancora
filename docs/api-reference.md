# API Reference — Nancora Python Library

Complete documentation of Nancora's public API.

## Core Module Exports

```python
import nancora as nc
```

### Top-Level Functions

#### `nancora.explore(df, target=None, *, max_analyses=10, rng_seed=0)`

Profiles a DataFrame and runs unsupervised or target-aware exploration.

- **Parameters**:
  - `df` (*pd.DataFrame*): Input dataset.
  - `target` (*str | None*): Optional target column name.
  - `max_analyses` (*int*): Maximum number of top recommendations to return (default: 10).
  - `rng_seed` (*int*): Seed for reproducible selection ties (default: 0).
- **Returns**: `AnalysisResult`
- **Raises**: `InputError`, `ConfigurationError`

#### `nancora.analyze(df, target=None, *, max_analyses=10, rng_seed=0)`

Alias for `explore()`, providing target-aware or unsupervised dataset analysis.

#### `nancora.read_csv(filepath_or_buffer, **kwargs)`

Helper function to load a CSV file into a Pandas DataFrame.

#### `nancora.read_excel(io, **kwargs)`

Helper function to load an Excel (`.xlsx`) file into a Pandas DataFrame (requires `openpyxl`).

#### `nancora.read_parquet(path, **kwargs)`

Helper function to load a Parquet file into a Pandas DataFrame (requires `pyarrow`).

---

## Result Objects

### `AnalysisResult`

Result object returned by `explore()` and `analyze()`.

- **Properties**:
  - `.profile` (*DatasetProfile*): Dataset dimensions, column types, and data quality stats.
  - `.recommendations` (*list[AnalysisCandidate]*): Selected top recommendations.
  - `.insights` (*list[str]*): Human-readable natural language evidence insights.
  - `.rejected_candidates` (*list[AnalysisCandidate]*): Skipped or redundant candidate analyses.
  - `.decision_trace` (*dict*): Detailed audit trace of all selected and rejected candidates.
- **Methods**:
  - `.to_dict()` $\rightarrow$ *dict*: Returns dictionary payload.
  - `.to_json(indent=None)` $\rightarrow$ *str*: Returns JSON string representation.
  - `.save(path)` $\rightarrow$ *Path*: Saves static HTML report to file path.
  - `.explain(target=0)` $\rightarrow$ *dict*: Returns detailed score explanation for recommendation at index or ID.

---

## Exception Hierarchy

All exceptions inherit from `NancoraError`:

- `NancoraError`
  - `AnalysisError`
    - `InputError`: Raised when input data, DataFrame type, or target parameters are invalid.
    - `ConfigurationError`: Raised when configuration parameters (`max_analyses`) are invalid.
  - `DataError`: Raised when dataset profiling or loading fails.
  - `ReportError`: Raised when HTML report generation fails.
