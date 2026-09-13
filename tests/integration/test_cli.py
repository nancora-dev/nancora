from typer.testing import CliRunner

from nancora.cli import app
from tests.conftest import mixed_frame


def test_cli_explore_writes_html(tmp_path):
    csv_path = tmp_path / "data.csv"
    mixed_frame().to_csv(csv_path, index=False)
    out = tmp_path / "out.html"
    runner = CliRunner()
    completed = runner.invoke(app, ["explore", str(csv_path), "--out", str(out)])
    assert completed.exit_code == 0, completed.output
    assert out.exists()
    assert "Selected" in completed.output
