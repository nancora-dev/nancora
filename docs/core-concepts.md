# Core Concepts — Nancora Python Library

## The Analytical Decision Layer

Nancora acts as an **analytical decision layer** positioned above computation and visualization libraries:

```text
Dataset  ==>  Schema Detection  ==>  Candidate Generation  ==>  Evidence Collection
         ==>  Heuristic Scoring ==>  Redundancy Reduction  ==>  Rank & Report
```

## 10-Stage Pipeline Overview

1. **Schema Detection**: Profiles input data types (`numeric`, `categorical`, `boolean`, `datetime`, `identifier`).
2. **Candidate Generation**: Proposes candidate statistical analyses.
3. **Applicability Filtering**: Validates requirements (min rows, variable count, data type bounds).
4. **Evidence Collection**: Gathers statistical properties ($r$, ANOVA $F$, IQR outlier rates, missingness).
5. **Heuristic Scoring**: Calculates a 0–100 relevance score using priors and empirical evidence.
6. **Redundancy Reduction**: Suppresses overlapping or redundant candidate analyses.
7. **Coverage Optimization**: Boosts candidates that cover previously unanalyzed columns.
8. **Ranking & Selection**: Sorts candidates and selects top $N$ recommendations (default: 10).
9. **Explanation Trace**: Generates mathematical score breakdowns.
10. **Visualization & Report**: Produces Matplotlib plot specifications, JSON output, or HTML reports.

## Scoring Formula Breakdown

Candidates are scored on a 0–100 scale using seven component factors:

$$\text{Score} = \text{Base Prior} + \text{Target Proximity} + \text{Evidence Strength} + \text{Information Value} + \text{Data Quality} + \text{Coverage Boost} + \text{Complexity Penalty}$$

> **Note**: Scores are ranking heuristics for exploratory attention. Correlation or association does not imply causation.
