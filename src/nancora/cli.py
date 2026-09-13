"""Command-line entry point. Thin wrapper over explore/analyze."""

from __future__ import annotations

from pathlib import Path

import typer

from nancora.data.io import read_csv, read_excel, read_json, read_parquet
from nancora.engine import analyze, explore

app = typer.Typer(help="Nancora: recommend analyses worth attention.")


def _load(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return read_csv(path)
    if suffix == ".json":
        return read_json(path)
    if suffix in {".xlsx", ".xls"}:
        return read_excel(path)
    if suffix in {".parquet", ".pq"}:
        return read_parquet(path)
    raise typer.BadParameter(f"Unsupported file type: {suffix}")


@app.command("explore")
def explore_cmd(
    path: Path = typer.Argument(..., exists=True, readable=True),
    max_analyses: int = typer.Option(10, "--max-analyses"),
    out: Path | None = typer.Option(None, "--out", help="Write HTML or JSON report"),
    json_out: bool = typer.Option(False, "--json", help="Print JSON to stdout"),
) -> None:
    """Unsupervised exploration."""
    df = _load(path)
    result = explore(df, max_analyses=max_analyses)
    _emit(result, out, json_out)


@app.command("analyze")
def analyze_cmd(
    path: Path = typer.Argument(..., exists=True, readable=True),
    target: str = typer.Option(..., "--target"),
    max_analyses: int = typer.Option(10, "--max-analyses"),
    out: Path | None = typer.Option(None, "--out"),
    json_out: bool = typer.Option(False, "--json"),
) -> None:
    """Target-aware analysis."""
    df = _load(path)
    result = analyze(df, target=target, max_analyses=max_analyses)
    _emit(result, out, json_out)


def _emit(result, out: Path | None, json_out: bool) -> None:
    if json_out:
        typer.echo(result.to_json())
    else:
        summary = result.summary()
        typer.echo(f"Selected {summary['n_selected']} analyses (rejected {summary['n_rejected']}).")
        for item in summary["top_scores"]:
            typer.echo(f"  {item['score']:>5}  {item['analysis_id']}  {item['variables']}")
    if out is not None:
        result.save(out)
        typer.echo(f"Wrote {out}")


if __name__ == "__main__":
    app()
