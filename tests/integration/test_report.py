import matplotlib

matplotlib.use("Agg")

import nancora as nc
from tests.conftest import mixed_frame


def test_html_report_contains_scores_and_rejections(tmp_path):
    df = mixed_frame()
    result = nc.explore(df, max_analyses=3)
    path = tmp_path / "report.html"
    result.save(path)
    text = path.read_text(encoding="utf-8")
    assert "Nancora" in text
    assert "Recommendations" in text
    assert "Rejected" in text
    recs = result.recommendations()
    assert recs
    assert str(recs[0].score) in text or f"{recs[0].score:g}" in text


def test_visualize_matplotlib_and_plotly():
    df = mixed_frame()
    result = nc.explore(df, max_analyses=2)
    figs = result.visualize(backend="matplotlib")
    assert figs
    plotly_figs = result.visualize(backend="plotly")
    assert plotly_figs
