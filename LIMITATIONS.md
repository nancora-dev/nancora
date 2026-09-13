# Limitations

- **Heuristic scores.** The 0–100 ranking is for attention, not a universal scientific quality metric.
- **No causal claims.** Correlation, group differences, and time associations are descriptive.
- **Pairwise caps.** Wide tables do not enumerate every column pair. See `MAX_PAIRS` / `max_pairs`.
- **Not AutoML.** Nancora does not train production models or tune pipelines.
- **IQR outliers.** Tukey flags depend on distribution shape; they are not proof of error.
- **Datetime trends.** Time association uses a simple ordinal/Pearson helper; it is not a forecasting model.
- **Excel/Parquet** require optional extras.
- **Interactive Plotly** is for notebooks; HTML reports embed static Matplotlib PNGs when a frame is available.
- **Benchmark metrics** are computed only when human labels exist. Empty labels produce no scores.
