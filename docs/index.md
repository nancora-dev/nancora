# Nancora — Python Data Analysis & Visualization Library

> You bring the data. Nancora brings the analytical direction.

**Nancora** is an open-source Python library for automated data analysis and visualization recommendations.

Rather than requiring data scientists to manually write repetitive exploratory analysis scripts or flooding users with dozens of uninformative charts, Nancora profiles datasets, generates candidate statistical analyses, evaluates empirical evidence, deduplicates redundant work, and ranks recommendations using transparent, explainable heuristic scores.

---

## Quick Example

```python
import pandas as pd
import nancora as nc

# Load dataset
df = pd.DataFrame({
    "age": [22, 25, 47, 52, 46, 56, 48, 33],
    "income": [25000, 32000, 75000, 89000, 71000, 95000, 82000, 49000],
    "city": ["Surat", "Surat", "Mumbai", "Delhi", "Mumbai", "Delhi", "Surat", "Mumbai"],
})

# Explore dataset
result = nc.explore(df)

# Print recommendations summary
print(result)
```

---

## Key Features

- **Analytical Intelligence Layer**: Determines *which* analyses are worth performing, leaving computation to Pandas/SciPy and visualization to Matplotlib.
- **Evidence-Backed Scoring**: Evaluates candidates on a 0–100 scale using empirical statistical signals (skewness, correlations, missingness, outlier rates).
- **Target-Aware Analysis**: Focuses recommendations on bivariate and group relationships involving a designated target variable (`target="col"`).
- **Explainable Output**: Every recommendation includes a mathematical score trace explaining why it was selected or skipped.
- **Offline-First & Deterministic**: Zero network dependencies, zero LLM calls, and 100% reproducible execution.

---

## Navigation

- [Installation](installation.md)
- [Quickstart Guide](quickstart.md)
- [Core Concepts](core-concepts.md)
- [API Reference](api-reference.md)
- [Practical Examples](examples.md)
- [Tutorials](tutorials.md)
- [Architecture](architecture.md)
- [Configuration](configuration.md)
- [Error Handling](error-handling.md)
- [Compatibility](compatibility.md)
- [Changelog](changelog.md)
- [Roadmap](roadmap.md)
- [Contributing Guide](contributing.md)
