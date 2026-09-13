"""Nancora: recommend which analyses are worth the user's attention."""

from nancora import analysis, data, plot, stats
from nancora import numeric as numpy
from nancora.analysis.registry import get_analysis, list_analyses, register_analysis
from nancora.data.io import read_csv, read_excel, read_json, read_parquet
from nancora.engine import analyze, explore
from nancora.result import AnalysisResult

__all__ = [
    "AnalysisResult",
    "analysis",
    "analyze",
    "data",
    "explore",
    "get_analysis",
    "list_analyses",
    "numpy",
    "plot",
    "read_csv",
    "read_excel",
    "read_json",
    "read_parquet",
    "register_analysis",
    "stats",
]
