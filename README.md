# Nancora

> Automated data analysis and visualization recommendations for Python.

Nancora is an open-source Python library designed to systematically guide exploratory data analysis (EDA). Instead of requiring data practitioners to manually write repetitive analysis scripts or wading through hundreds of unguided charts, Nancora profiles a tabular dataset, evaluates candidate statistical analyses based on empirical evidence, suppresses redundant insights, and ranks actionable recommendations paired with visual specifications.

**Latest release:** `0.1.1`

---

## Project Status

| Category | Indicator | Details |
| :--- | :--- | :--- |
| **Package** | [![PyPI version](https://img.shields.io/pypi/v/nancora.svg)](https://pypi.org/project/nancora/) | Published on PyPI (`nancora`) |
| **Python** | [![Python Version](https://img.shields.io/pypi/pyversions/nancora.svg)](https://pypi.org/project/nancora/) | Python `>=3.10` (tested on 3.10, 3.11, 3.12) |
| **License** | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) | Open Source (MIT License) |
| **Quality & CI** | [![CI](https://github.com/nancora/nancora/actions/workflows/ci.yml/badge.svg)](https://github.com/nancora/nancora/actions/workflows/ci.yml) | Automated test suite and static analysis |

---

## Documentation

Nancora includes a comprehensive documentation suite located in the [`docs/`](docs/) directory:

| Documentation | Description | Link |
| :--- | :--- | :--- |
| **Index** | Main documentation homepage & navigation | [`docs/index.md`](docs/index.md) |
| **Quickstart** | Get started with Nancora in minutes | [`docs/quickstart.md`](docs/quickstart.md) |
| **Installation** | Installation options and requirements | [`docs/installation.md`](docs/installation.md) |
| **Core Concepts** | Understand Nancora's analysis and scoring workflow | [`docs/core-concepts.md`](docs/core-concepts.md) |
| **API Reference** | Public API documentation for functions and objects | [`docs/api-reference.md`](docs/api-reference.md) |
| **Examples** | Practical code examples and workflows | [`docs/examples.md`](docs/examples.md) |
| **Tutorials** | Step-by-step guides for analysis scenarios | [`docs/tutorials.md`](docs/tutorials.md) |
| **Architecture** | Internal pipeline design and component architecture | [`docs/architecture.md`](docs/architecture.md) |
| **Configuration** | Configure exploration parameters and limits | [`docs/configuration.md`](docs/configuration.md) |
| **Error Handling** | Exception hierarchy and input validation rules | [`docs/error-handling.md`](docs/error-handling.md) |
| **Compatibility** | Python, Pandas, and environment compatibility | [`docs/compatibility.md`](docs/compatibility.md) |
| **Changelog** | Version history and release notes | [`docs/changelog.md`](docs/changelog.md) |
| **Roadmap** | Development roadmap and planned releases | [`docs/roadmap.md`](docs/roadmap.md) |
| **Contributing** | Guidelines for contributing to Nancora | [`docs/contributing.md`](docs/contributing.md) |

---

## Why Nancora?

When presented with a new tabular dataset, data practitioners encounter an **analytical decision problem**: even a small dataset with 20 columns yields hundreds of candidate summary statistics, correlation pairs, distribution screens, and group comparisons. The vast majority of these candidates yield trivial or redundant findings.

Standard computational libraries (Pandas, SciPy) execute whatever statistical operations you request, and visualization tools (Matplotlib, Plotly) render whatever charts you code. Traditional automated EDA tools often default to rendering monolithic HTML reports containing every possible chart, causing visual overload.

**Nancora acts as an analytical decision layer on top of the scientific Python ecosystem.** It evaluates candidate analyses before computing or rendering them, prioritizing directions with genuine statistical signal while penalizing uninformative or redundant exploration.

```text
+-------------------------------------------------------------------------------+
|                             DATA SCIENCE STACK                                |
+-------------------------------------------------------------------------------+
|  Nancora       --> Decides WHICH analyses are worth performing                |
|  Pandas/SciPy  --> Performs statistical COMPUTATION                           |
|  Matplotlib    --> Performs visual RENDERING                                  |
+-------------------------------------------------------------------------------+
```

### Key Differences

| Capability / Focus | Traditional AutoEDA | Nancora |
| :--- | :--- | :--- |
| **Primary Goal** | Render all possible charts for every column | Select and rank high-signal candidate analyses |
| **Decision Mechanism** | Hardcoded visual templates | Evidence-backed 0–100 heuristic scoring |
| **Redundancy Control** | Minimal (displays repetitive feature pairs) | Active family & variable overlap suppression |
| **Explainability** | Opaque / implicit chart outputs | Transparent decision traces & mathematical score breakdowns |
| **Target Awareness** | Separate tool or unguided | Guided exploration toward a designated target variable |
| **Execution Model** | Heavy dependencies or LLM wrappers | Lightweight, offline-first, pure Python / Pandas / SciPy |

---

## Features

- **Automated Dataset Exploration & Profiling**: Detects statistical column types (`numeric`, `categorical`, `boolean`, `datetime`, `identifier`), shape, and cell missingness rates.
- **Evidence-Backed Heuristic Scoring**: Evaluates candidate analyses on an explainable 0–100 scale using empirical signals (skewness, correlations, missingness, outlier rates).
- **Target-Aware Exploration**: Accepts a `target` column parameter to prioritize bivariate and group relationships involving key target variables.
- **Redundancy Suppression**: Suppresses overlapping candidate analyses that share common variable pairs or analytical families.
- **Explainable Decision Traces**: Generates mathematical score breakdowns explaining why each candidate analysis was selected or skipped.
- **Declarative Visualization Specs**: Constructs Matplotlib-ready visual specifications (`hist`, `bar`, `scatter`, `box`, `line`) for top recommendations.
- **Rich Serialization & Reporting**: Supports Jupyter Notebook HTML summary tables, self-contained static HTML reports, and JSON export.
- **Command-Line Interface (CLI)**: Includes a built-in terminal CLI (`nancora explore`, `nancora analyze`) with CSV, JSON, Excel, and Parquet file support.
- **Robust Exception Hierarchy**: Enforces strict input validation (`NancoraError`, `InputError`, `ConfigurationError`, `DataError`, `ReportError`).
- **Deterministic & Offline-First**: 100% reproducible execution using seedable tie-breaking (`rng_seed`), zero network dependencies, and zero LLM calls.

---

## Installation

### Standard Installation

Install Nancora from PyPI using `pip`:

```bash
pip install nancora
```

Alternatively:

```bash
python -m pip install nancora
```

### Python Version Support

Nancora requires **Python 3.10 or higher**. It is tested and validated against:
- Python 3.10
- Python 3.11
- Python 3.12

### Optional File Format Extras

To enable additional file format readers in the CLI or IO module:

```bash
# Excel (.xlsx) file support
pip install "nancora[excel]"

# Parquet (.parquet) file support
pip install "nancora[parquet]"
```

### Development Installation

To install Nancora locally for development and testing:

```bash
git clone https://github.com/nancora/nancora.git
cd nancora
pip install -e ".[dev]"
```

---

## Quickstart

### 1. Unsupervised Dataset Exploration

Pass any Pandas `DataFrame` to `nancora.explore()` to discover key analytical directions:

```python
import pandas as pd
import nancora as nc

# 1. Create or load a dataset
df = pd.DataFrame({
    "age": [21, 25, 31, 42, 55, 62, 29, 35],
    "income": [25000, 35000, 50000, 70000, 90000, 115000, 48000, 62000],
    "city": ["Surat", "Surat", "Mumbai", "Delhi", "Mumbai", "Delhi", "Surat", "Mumbai"],
})

# 2. Run automated dataset exploration
result = nc.explore(df)

# 3. Print recommendations summary
print(result)
```

In a **Jupyter Notebook**, evaluating `result` automatically renders an interactive HTML summary table in the cell output.

### 2. Target-Aware Exploration & Report Export

If you have a primary variable of interest (e.g., customer churn, sales amount, diagnostic result), specify `target`:

```python
import nancora as nc

# Load dataset using Nancora IO helper
df = nc.read_csv("customer_data.csv")

# Run target-aware exploration focused on "income"
result = nc.explore(df, target="income", max_analyses=5)

# Inspect human-readable evidence insights
for insight in result.insights:
    print(f"• {insight}")

# Save self-contained HTML report to disk
result.save("income_analysis_report.html")
```

---

## How It Works

Nancora processes datasets through a deterministic 10-stage execution pipeline:

```text
Dataset Input
      │
      ▼
1. Schema Detection & Data Profiling
      │
      ▼
2. Candidate Analysis Generation
      │
      ▼
3. Applicability & Constraint Validation
      │
      ▼
4. Empirical Evidence Collection
      │
      ▼
5. Heuristic Score Computation (0–100 Scale)
      │
      ▼
6. Redundancy Suppression & Overlap Control
      │
      ▼
7. Coverage Optimization & Target Proximity Boost
      │
      ▼
8. Candidate Ranking & Top-N Selection
      │
      ▼
9. Explanation Synthesis & Trace Audit
      │
      ▼
10. Visualization Specs & HTML/JSON Report Output
```

### Stage Summary

1. **Schema Detection**: Identifies column types (`numeric`, `categorical`, `boolean`, `datetime`, `identifier`) and dataset shape.
2. **Candidate Generation**: Proposes candidate analyses across dataset, univariate, bivariate, and target-focused categories.
3. **Applicability Validation**: Verifies minimum row thresholds, column compatibility, and dataset bounds.
4. **Evidence Collection**: Runs empirical statistical checks (IQR outlier ratios, Pearson correlation $r$, ANOVA group statistics).
5. **Heuristic Scoring**: Combines base priors, target proximity, statistical evidence, and data quality into an explainable 0–100 score.
6. **Redundancy Reduction**: Suppresses redundant candidate analyses sharing overlapping variable pairs or families.
7. **Coverage Optimization**: Awards coverage boosts to top candidates that introduce previously unrepresented columns.
8. **Ranking & Selection**: Sorts candidates by final score and selects the top $N$ recommendations (default: 10).
9. **Explanation Synthesis**: Builds human-readable evidence summaries and mathematical decision traces.
10. **Visualization & Reporting**: Emits `AnalysisResult` containers, Matplotlib visual specifications, JSON payloads, or self-contained HTML reports.

---

## Examples

Runnable example scripts and notebooks are available in the [`examples/`](examples/) directory:

| Example Script | Description | Link |
| :--- | :--- | :--- |
| `basic_exploration.py` | Basic unsupervised dataset exploration workflow | [`examples/basic_exploration.py`](examples/basic_exploration.py) |
| `target_analysis.py` | Target-aware exploration focused on a key column | [`examples/target_analysis.py`](examples/target_analysis.py) |
| `file_loading.py` | Loading datasets from CSV, Excel, Parquet, and JSON | [`examples/file_loading.py`](examples/file_loading.py) |
| `mvp_acceptance.py` | Full pipeline acceptance workflow and report generation | [`examples/mvp_acceptance.py`](examples/mvp_acceptance.py) |
| `nancora_quickstart.ipynb` | Interactive Jupyter Notebook quickstart tutorial | [`examples/nancora_quickstart.ipynb`](examples/nancora_quickstart.ipynb) |

---

## Supported Analysis & Visualization Capabilities

Nancora evaluates ten built-in analysis families in release `0.1.1`:

| Capability / Analysis ID | Category | Target Requirement | Description & Evidence Evaluated | Visual Spec | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `missingness_analysis` | Dataset | Any | Analyzes cell missing rates across columns. Penalized (-25) when missingness is 0%. | Bar chart | Available |
| `cardinality_analysis` | Univariate | Any | Detects high uniqueness ratios and primary key candidates. | Bar chart | Available |
| `numeric_distribution` | Univariate | Continuous | Analyzes skewness, kurtosis, mean, and standard deviation. | Histogram | Available |
| `categorical_distribution` | Univariate | Discrete | Measures class balance and frequency distributions across levels. | Bar chart | Available |
| `outlier_analysis` | Univariate | Continuous ($N \ge 8$) | Screens continuous variables for extreme values using IQR bounds. | Histogram | Available |
| `correlation_analysis` | Bivariate | Continuous pairs | Computes pairwise Pearson correlation coefficients ($r$). | Scatter / Heatmap | Available |
| `numeric_relationship` | Bivariate | Continuous pairs | Evaluates continuous association between numerical column pairs. | Scatter plot | Available |
| `categorical_numeric` | Bivariate | Categorical + Continuous | Compares numeric distributions across category levels (ANOVA / group stats). | Box plot | Available |
| `datetime_numeric_trend` | Bivariate | Datetime + Continuous | Analyzes temporal trends and time-series progressions. | Line chart | Available |
| `target_aware` | Bivariate | Target column | Directly screens features against a specified target variable (`target="col"`). | Scatter / Box / Bar | Available |

---

## Configuration

Nancora provides explicit configuration parameters for pipeline exploration:

```python
import nancora as nc

result = nc.explore(
    df,
    target="income",    # Primary column of interest (default: None)
    max_analyses=5,     # Maximum recommendations returned (default: 10, must be >= 1)
    rng_seed=42,        # Random seed for reproducible tie-breaking (default: 0)
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `df` | `pd.DataFrame` | *Required* | Input pandas DataFrame to analyze. Must be non-empty ($N \ge 1$). |
| `target` | `str \| None` | `None` | Optional target column name for target-aware exploration. |
| `max_analyses` | `int` | `10` | Maximum number of top recommendations returned in `result.recommendations`. |
| `rng_seed` | `int` | `0` | Seed used for deterministic ranking tie-breaking. |

---

## Error Handling

Nancora provides a clean exception hierarchy for input validation and diagnostic reporting. All custom exceptions derive from `NancoraError`:

```text
NancoraError (base library exception)
├── AnalysisError
│   ├── InputError (raised on invalid DataFrames, missing target columns, or bad types)
│   └── ConfigurationError (raised when max_analyses < 1 or parameters out of bounds)
├── DataError (raised on dataset profiling or IO loading failures)
└── ReportError (raised on HTML report generation or file writing failures)
```

### Exception Usage Example

```python
import pandas as pd
import nancora as nc

try:
    # Attempt exploration with non-existent target column
    result = nc.explore(df, target="non_existent_column")
except nc.InputError as err:
    print(f"Input validation error: {err}")
except nc.ConfigurationError as err:
    print(f"Configuration error: {err}")
except nc.NancoraError as err:
    print(f"Nancora error: {err}")
```

---

## Command-Line Interface (CLI)

Nancora includes a built-in terminal CLI (`nancora`) built with Typer:

### Terminal Usage

```bash
# Basic exploration of a CSV file
nancora explore data.csv --out report.html

# Target-aware exploration focusing on "churn_status"
nancora analyze data.csv --target churn_status --out report.html

# Output JSON summary payload to stdout
nancora explore data.csv --json
```

---

## Development & Contributing

We welcome community contributions, bug reports, feature proposals, and documentation improvements!

### Development Environment Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/nancora/nancora.git
   cd nancora
   ```

2. Create a virtual environment and install development dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Run the automated test suite:
   ```bash
   pytest
   ```

4. Run the intelligence benchmark harness:
   ```bash
   python -m benchmarks.runner
   ```

5. Run static analysis and linting:
   ```bash
   ruff check src tests
   mypy src
   ```

For detailed contribution guidelines, please review [`CONTRIBUTING.md`](CONTRIBUTING.md) or [`docs/contributing.md`](docs/contributing.md).

---

## Project Roadmap

| Release | Focus | Planned / Available Capabilities | Status |
| :--- | :--- | :--- | :--- |
| **`v0.1.0` – `v0.1.1`** | **Foundation & Library Quality** | 10 built-in analysis candidate families, 7-factor explainable scoring engine, redundancy control, coverage optimization, Jupyter HTML output, static HTML reports, JSON export, input validation, and Typer CLI. | **Available** |
| **`v0.2.0`** | **Intelligence Improvements** | Multivariate candidate generators (3+ variable interactions), native interactive Plotly rendering support for HTML reports, and non-linear association metrics (Mutual Information). | Planned |
| **`v0.3.0`** | **Ecosystem & Customization** | Plugin architecture for custom analysis candidate registration (`@register_analysis`), exportable Jupyter `.ipynb` notebook generation, and file-based heuristic configuration (`nancora.toml`). | Planned |
| **`v1.0.0`** | **API Stability & Enterprise Polish** | Stable public API guarantee, expanded file connectors, and comprehensive benchmark validation suite. | Future Goal |

---

## Project Vision

Nancora aims to make exploratory data analysis systematic, reproducible, and transparent for Python data practitioners. By acting as an analytical decision layer between raw data and compute/visualization engines, Nancora provides data scientists with structured guidance without requiring opaque AI models or generating overwhelming visual clutter.

---

## License

Nancora is open-source software licensed under the [MIT License](LICENSE).

```text
Copyright (c) 2026 Nancora
Licensed under the MIT License.
```
