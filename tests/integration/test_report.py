from pathlib import Path

import pandas as pd

import nancora as nc


def test_html_report_contains_scores_and_rejects(tmp_path: Path):
    df = pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
            "b": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0],
            "cat": list("abababab"),
        }
    )
    result = nc.explore(df, max_analyses=3)
    dest = tmp_path / "report.html"
    result.save(dest)
    html = dest.read_text(encoding="utf-8")
    assert "Nancora analysis report" in html
    assert "heuristic" in html.lower()
    assert str(result.selected[0].score) in html
    assert "Rejected analyses" in html
    figs = result.visualize(backend="matplotlib")
    assert figs
