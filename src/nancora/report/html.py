"""HTML report generated from AnalysisResult.to_dict()."""

from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from nancora.result import AnalysisResult

TEMPLATE_FALLBACK = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Nancora report</title>
  <style>
    body { font-family: Georgia, serif; margin: 2rem auto; max-width: 900px; color: #1b1b1b; }
    h1, h2 { font-family: system-ui, sans-serif; }
    .score { font-variant-numeric: tabular-nums; }
    details { margin: 0.5rem 0; }
    img { max-width: 100%; height: auto; }
    footer { margin-top: 3rem; font-size: 0.9rem; color: #444; }
    pre { background: #f4f1ea; padding: 0.75rem; overflow: auto; }
  </style>
</head>
<body>
  <h1>Nancora analysis report</h1>
  <p>Heuristic ranking only. Scores are not scientifically universal. Associations are not causal.</p>
  <h2>Summary</h2>
  <ul>
    <li>Rows: {{ summary.n_rows }}</li>
    <li>Columns: {{ summary.n_columns }}</li>
    <li>Selected: {{ summary.n_selected }}</li>
    <li>Rejected: {{ summary.n_rejected }}</li>
    <li>Target: {{ summary.target or "none" }}</li>
  </ul>
  <h2>Recommendations</h2>
  {% for rec in recommendations %}
    <article>
      <h3>{{ rec.analysis_id }} — {{ rec.variables | join(", ") }} <span class="score">({{ rec.score }})</span></h3>
      <p>{{ rec.insight }}</p>
      <pre>{{ rec.explanation }}</pre>
      {% if rec.image %}<img alt="{{ rec.analysis_id }}" src="{{ rec.image }}"/>{% endif %}
    </article>
  {% endfor %}
  <h2>Insights</h2>
  <ul>{% for line in insights %}<li>{{ line }}</li>{% endfor %}</ul>
  <h2>Rejected analyses</h2>
  {% for rec in rejected %}
    <details>
      <summary>{{ rec.analysis_id }} — {{ rec.variables | join(", ") }} ({{ rec.reject_reason }})</summary>
      <pre>{{ rec.explanation }}</pre>
    </details>
  {% endfor %}
  <footer>
    Nancora does not claim causal effects. Pairwise analyses may be capped on wide tables.
    Ranking scores are heuristics for attention, not ground truth.
  </footer>
</body>
</html>
"""


def _figures_as_data_uri(result: AnalysisResult) -> dict[int, str]:
    images: dict[int, str] = {}
    if result._df is None:
        return images
    try:
        figures = result.visualize(backend="matplotlib")
    except Exception:
        return images
    for index, fig in enumerate(figures):
        buffer = BytesIO()
        fig.savefig(buffer, format="png", dpi=110)
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        images[index] = f"data:image/png;base64,{encoded}"
        close = getattr(fig, "clf", None)
        if callable(close):
            import matplotlib.pyplot as plt

            plt.close(fig)
    return images


def write_html_report(result: AnalysisResult, path: Path) -> Path:
    payload = result.to_dict()
    images = _figures_as_data_uri(result)
    recommendations = []
    for index, rec in enumerate(payload["recommendations"]):
        item = dict(rec)
        item["image"] = images.get(index)
        recommendations.append(item)
    try:
        env = Environment(
            loader=PackageLoader("nancora.report", "templates"),
            autoescape=select_autoescape(["html"]),
        )
        template = env.get_template("report.html.j2")
        html = template.render(
            summary=payload["summary"],
            recommendations=recommendations,
            insights=payload["insights"],
            rejected=payload["rejected"],
        )
    except Exception:
        env = Environment(autoescape=select_autoescape(["html"]))
        html = env.from_string(TEMPLATE_FALLBACK).render(
            summary=payload["summary"],
            recommendations=recommendations,
            insights=payload["insights"],
            rejected=payload["rejected"],
        )
    path = Path(path)
    path.write_text(html, encoding="utf-8")
    return path
