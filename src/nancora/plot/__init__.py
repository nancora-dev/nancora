"""Unified plot dispatch. Analyses emit PlotSpec; this module chooses a backend."""

from __future__ import annotations

import pandas as pd

from nancora.plot.spec import PlotSpec


def render(df: pd.DataFrame, spec: PlotSpec, backend: str = "matplotlib"):
    if backend == "matplotlib":
        from nancora.plot.matplotlib_backend import render_matplotlib

        return render_matplotlib(df, spec)
    if backend == "plotly":
        from nancora.plot.plotly_backend import render_plotly

        return render_plotly(df, spec)
    raise ValueError(f"Unknown plot backend: {backend}")


__all__ = ["PlotSpec", "render"]
