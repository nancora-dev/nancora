# Roadmap — Nancora Python Library

This document outlines the development roadmap for Nancora, distinguishing current functionality from planned future releases.

## Current Release: v0.1.x (Foundation & Library Quality)

- **10 Built-in Analysis Candidates**: Univariate, bivariate, data quality, and target-aware screens.
- **Explainable Scoring Engine**: 7-factor 0–100 heuristic scoring with complete decision traces.
- **Redundancy Control & Coverage**: Deduplication of overlapping variable pairs and coverage optimization.
- **Serialization & Reports**: Rich Jupyter Notebook HTML rendering, standalone HTML reports, and JSON export.
- **Input Validation**: `InputError` and `ConfigurationError` input safety checks.

---

## Planned Future Releases

### v0.2.0 — Expanded Intelligence
- **Multivariate Candidates**: 3+ variable interactions and non-linear relationship screens.
- **Interactive Plotly Rendering**: Native Plotly HTML figure rendering in static reports.
- **Enhanced Signal Detection**: Non-linear association metrics (Mutual Information, Distance Correlation).

### v0.3.0 — Ecosystem & Customization
- **Plugin Architecture**: Custom analysis candidate registration API (`@register_analysis`).
- **Jupyter Notebook Export**: Exporting exploration recommendations directly to executable `.ipynb` notebooks.
- **Configurable Heuristic Priors**: Customizing scoring weights via config files (`nancora.toml`).
