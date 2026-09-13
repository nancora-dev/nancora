"""Matplotlib renderer for PlotSpec. Uses the Agg backend when no display is available."""

from __future__ import annotations

import os

import matplotlib

if os.environ.get("MPLBACKEND") is None:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from nancora.plot.spec import PlotSpec


def render_matplotlib(df: pd.DataFrame, spec: PlotSpec):
    fig, ax = plt.subplots(figsize=(6, 4))
    kind = spec.kind
    if kind == "hist" and spec.x:
        ax.hist(pd.to_numeric(df[spec.x], errors="coerce").dropna(), bins="auto", color="#3b6ea5")
        ax.set_xlabel(spec.x)
        ax.set_ylabel("count")
    elif kind == "bar" and spec.x:
        counts = df[spec.x].astype("string").value_counts().head(20)
        ax.bar(counts.index.astype(str), counts.values, color="#3b6ea5")
        ax.tick_params(axis="x", rotation=45)
        ax.set_ylabel("count")
    elif kind == "scatter" and spec.x and spec.y:
        ax.scatter(
            pd.to_numeric(df[spec.x], errors="coerce"),
            pd.to_numeric(df[spec.y], errors="coerce"),
            alpha=0.6,
            s=18,
            color="#3b6ea5",
        )
        ax.set_xlabel(spec.x)
        ax.set_ylabel(spec.y)
    elif kind == "box" and spec.x and spec.y:
        grouped = df[[spec.x, spec.y]].dropna()
        labels = list(grouped[spec.x].astype("string").unique())[:12]
        data = [
            pd.to_numeric(
                grouped.loc[grouped[spec.x].astype("string") == lab, spec.y], errors="coerce"
            ).dropna()
            for lab in labels
        ]
        ax.boxplot(data, tick_labels=[str(x) for x in labels])
        ax.set_xlabel(spec.x)
        ax.set_ylabel(spec.y)
    elif kind == "line" and spec.x and spec.y:
        frame = df[[spec.x, spec.y]].dropna().sort_values(spec.x)
        ax.plot(frame[spec.x], pd.to_numeric(frame[spec.y], errors="coerce"), color="#3b6ea5")
        ax.set_xlabel(spec.x)
        ax.set_ylabel(spec.y)
    elif kind == "heatmap":
        cols = spec.extra.get("columns") or []
        if cols:
            corr = df[cols].apply(pd.to_numeric, errors="coerce").corr()
            im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=45, ha="right")
            ax.set_yticklabels(corr.columns)
            fig.colorbar(im, ax=ax, fraction=0.046)
    else:
        ax.text(0.5, 0.5, f"Unsupported plot kind: {kind}", ha="center")
    ax.set_title(spec.title)
    fig.tight_layout()
    return fig
