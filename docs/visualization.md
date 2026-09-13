# Visualization

Analyses emit a backend-agnostic `PlotSpec`. `nc.plot.render(spec, df, backend="matplotlib"|"plotly")` draws it.

HTML reports embed Matplotlib PNGs. Plotly is for interactive notebook use via `result.visualize(backend="plotly")`.
