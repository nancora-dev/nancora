from pathlib import Path

from typer.testing import CliRunner

from nancora.cli import app

runner = CliRunner()


def test_cli_explore(tmp_path: Path):
    csv = tmp_path / "data.csv"
    csv.write_text("x,y,g\n1,2,a\n2,4,b\n3,6,a\n4,8,b\n5,10,a\n6,12,b\n", encoding="utf-8")
    out = tmp_path / "r.html"
    result = runner.invoke(app, ["explore", str(csv), "--out", str(out), "--max-analyses", "4"])
    assert result.exit_code == 0, result.output
    assert out.exists()
    assert "Selected" in result.output
