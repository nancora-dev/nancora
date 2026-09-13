# Limitations

- Ranking scores are **heuristics** (0–100). They are not a universal measure of scientific quality.
- Pairwise analyses are **capped** (`PAIRWISE_CAP`) so wide tables do not explode combinatorially. Some real relationships will not be proposed.
- Correlation, ANOVA-style group tests, and time-ordinal Spearman statistics are **associations**. They are not causal effects and not forecasts.
- IQR outlier flags are a fence heuristic, not a contamination model.
- Schema kinds use dtype plus cardinality heuristics; integer codes may be labeled categorical or numeric incorrectly.
- HTML reports embed static Matplotlib images. Plotly is for interactive `visualize(backend="plotly")`.
- The benchmark runner does **not** ship claimed leaderboard numbers. Empty labels mean metrics are skipped.
- Nancora is not AutoML, not a database, not a cloud product, and not an LLM assistant.
