# Architecture

Pipeline:

DATA → SCHEMA → PROFILE → CANDIDATES → EVIDENCE → SCORING → REDUNDANCY → RANKING → RECOMMENDATIONS → VISUALIZATION → INSIGHTS → REPORT

Scientific libraries are engines, not products Nancora reimplements.

- Pandas: IO and frames
- NumPy: arrays
- SciPy: named statistical tests
- Matplotlib / Plotly: `PlotSpec` backends

The intelligence engine (`nancora.engine`) is the differentiator. Builtin analyses live in `nancora.analysis.builtin` and register through `register_analysis`.
