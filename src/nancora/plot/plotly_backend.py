"""Plotly renderer for PlotSpec. Interactive use in notebooks; optional in reports."""

from __future__ import annotations

import pandas as pd

from nancora.plot.spec import PlotSpec


def render_plotly(df: pd.DataFrame, spec: PlotSpec):
    import plotly.express as px
    import plotly.graph_objects as go

    kind = spec.kind
    if kind == "hist" and spec.x:
        return px.histogram(df, x=spec.x, title=spec.title)
    if kind == "bar" and spec.x:
        counts = df[spec.x].astype("string").value_counts().head(20).reset_index()
        counts.columns = [spec.x, "count"]
        return px.bar(counts, x=spec.x, y="count", title=spec.title)
    if kind == "scatter" and spec.x and spec.y:
        return px.scatter(df, x=spec.x, y=spec.y, title=spec.title, opacity=0.7)
    if kind == "box" and spec.x and spec.y:
        return px.box(df, x=spec.x, y=spec.y, title=spec.title)
    if kind == "line" and spec.x and spec.y:
        frame = df[[spec.x, spec.y]].dropna().sort_values(spec.x)
        return px.line(frame, x=spec.x, y=spec.y, title=spec.title)
    if kind == "heatmap":
        cols = spec.extra.get("columns") or []
        corr = (
            df[cols].apply(pd.to_numeric, errors="coerce").corr()
            if cols
            else df.corr(numeric_only=True)
        )
        return go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=list(corr.columns),
                y=list(corr.columns),
                colorscale="RdBu",
                zmin=-1,
                zmax=1,
            ),
            layout={"title": spec.title},
        )
    return go.Figure(layout={"title": f"Unsupported plot kind: {kind}"})
