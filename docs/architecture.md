# Architecture

Pipeline: data → schema → profile → candidates → evidence → scoring → redundancy → ranking → recommendations → visualization → insights → report.

Scientific libraries are engines, not products Nancora reimplements.

- Pandas: frames and IO
- NumPy: arrays and univariate numeric summaries
- SciPy: named association tests
- Matplotlib / Plotly: PlotSpec backends

The recommendation engine is the product differentiator. See `src/nancora/engine/`.
