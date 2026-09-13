"""Curated IO. Pandas does the work; Nancora only standardizes errors and return types."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from nancora.exceptions import DataError


def _as_path(source: str | Path) -> Path:
    return Path(source)


def read_csv(source: str | Path, **kwargs) -> pd.DataFrame:
    try:
        return pd.read_csv(_as_path(source), **kwargs)
    except Exception as exc:  # noqa: BLE001 — surface as DataError
        raise DataError(f"Could not read CSV: {source}") from exc


def read_json(source: str | Path, **kwargs) -> pd.DataFrame:
    try:
        return pd.read_json(_as_path(source), **kwargs)
    except Exception as exc:  # noqa: BLE001
        raise DataError(f"Could not read JSON: {source}") from exc


def read_excel(source: str | Path, **kwargs) -> pd.DataFrame:
    try:
        return pd.read_excel(_as_path(source), **kwargs)
    except ImportError as exc:
        raise DataError("Excel support requires nancora[excel] (openpyxl).") from exc
    except Exception as exc:  # noqa: BLE001
        raise DataError(f"Could not read Excel: {source}") from exc


def read_parquet(source: str | Path, **kwargs) -> pd.DataFrame:
    try:
        return pd.read_parquet(_as_path(source), **kwargs)
    except ImportError as exc:
        raise DataError("Parquet support requires nancora[parquet] (pyarrow).") from exc
    except Exception as exc:  # noqa: BLE001
        raise DataError(f"Could not read Parquet: {source}") from exc
