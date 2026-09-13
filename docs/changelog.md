# Changelog — Nancora Python Library

All notable changes to the Nancora library are documented in this file.

## [0.1.0] — Initial Release

### Added
- **Core Pipeline**: 10-stage deterministic exploration pipeline (`explore`, `analyze`).
- **10 Built-in Analysis Candidates**:
  - `missingness_analysis`
  - `cardinality_analysis`
  - `numeric_distribution`
  - `categorical_distribution`
  - `outlier_analysis`
  - `correlation_analysis`
  - `numeric_relationship`
  - `categorical_numeric`
  - `datetime_numeric_trend`
  - `target_aware`
- **Explainable Scoring**: 0–100 heuristic relevance scoring with decision traces and score breakdowns.
- **Redundancy & Coverage**: Family-level redundancy suppression and coverage optimization.
- **Outputs & Reports**: `AnalysisResult` with `.to_dict()`, `.to_json()`, and static HTML report generation.
- **CLI**: Typer-based command-line interface (`nancora explore`, `nancora analyze`).
- **Input Validation & Exception Hierarchy**: `InputError`, `ConfigurationError`, `DataError`, `AnalysisError`, `ReportError`.
- **Dynamic Version Exposure**: `nancora.__version__` exposure via `importlib.metadata`.
