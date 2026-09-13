"""HTML reports from AnalysisResult. Static Matplotlib images; no JS app."""

from __future__ import annotations

import base64
import io
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from nancora.exceptions import ReportError
from nancora.plot.matplotlib_backend import render_matplotlib
from nancora.result import AnalysisResult


def _figure_to_data_uri(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("ascii")
    import matplotlib.pyplot as plt

    plt.close(fig)
    return f"data:image/png;base64,{encoded}"


def write_html(result: AnalysisResult, path: str | Path) -> Path:
    dest = Path(path)
    env = Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("report.html.j2")
    recs = []
    for cand in result.selected:
        item = cand.to_dict()
        if result.frame is not None and cand.viz is not None:
            try:
                fig = render_matplotlib(result.frame, cand.viz)
                item["image"] = _figure_to_data_uri(fig)
            except Exception:  # noqa: BLE001
                item["image"] = None
        else:
            item["image"] = None
        recs.append(item)
    html = template.render(
        summary=result.summary(),
        profile=result.dataset_profile.to_dict(),
        recommendations=recs,
        insights=result.insights(),
        rejected=[c.to_dict() for c in result.rejected],
    )
    try:
        dest.write_text(html, encoding="utf-8")
    except OSError as exc:
        raise ReportError(f"Could not write HTML report: {dest}") from exc
    return dest
