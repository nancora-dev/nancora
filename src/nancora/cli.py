"""Command-line interface around explore/analyze."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from nancora.data.io import read_csv, read_excel, read_json, read_parquet
from nancora.engine import run_pipeline
from nancora.result import AnalysisResult

app = typer.Typer(add_completion=False, no_args_is_help=True, help="Nancora: recommend analyses worth attention.")


def _load(path: Path):
    suffix = path.suffix.lower()
    if suffix in {".csv", ".txt"}:
        return read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return read_excel(path)
    if suffix == ".json":
        return read_json(path)
    if suffix == ".parquet":
        return read_parquet(path)
    raise typer.BadParameter(f"Unsupported file type: {suffix}")


@app.command()
def explore(
    path: Path = typer.Argument(..., exists=True, readable=True),
    target: Optional[str] = typer.Option(None, help="Optional target column."),
    max_analyses: int = typer.Option(10, help="Maximum selected analyses."),
    out: Optional[Path] = typer.Option(None, help="Write HTML or JSON report."),
    json_out: bool = typer.Option(False, "--json", help="Print JSON to stdout."),
) -> None:
    """Profile a table and recommend analyses."""
    df = _load(path)
    payload = run_pipeline(df, target=target, max_analyses=max_analyses)
    result = AnalysisResult(
        _profile=payload["profile"],
        _candidates=payload["candidates"],
        _context=payload["context"],
        _timings=payload["timings"],
        _n_drafts=payload["n_drafts"],
        _df=df,
    )
    if json_out:
        typer.echo(result.to_json())
    else:
        summary = result.summary()
        typer.echo(
            f"Selected {summary['n_selected']} analyses "
            f"(rejected {summary['n_rejected']}) from {path.name}."
        )
        for rec in result.recommendations():
            typer.echo(f"  {rec.score:5.1f}  {rec.analysis_id}  {', '.join(rec.variables)}")
    if out is not None:
        result.save(out)
        typer.echo(f"Wrote {out}")


@app.command()
def version() -> None:
    """Print the package version."""
    from nancora import __version__

    typer.echo(__version__)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
