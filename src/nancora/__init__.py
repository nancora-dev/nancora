import importlib.metadata

try:
    __version__ = importlib.metadata.version("nancora")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0"

from nancora import analysis, data, plot, stats
from nancora import numeric as numpy
from nancora.analysis.registry import get_analysis, list_analyses, register_analysis
from nancora.data.io import read_csv, read_excel, read_json, read_parquet
from nancora.engine import analyze, explore
from nancora.result import AnalysisResult, ExplorationResult

__all__ = [
    "__version__",
    "AnalysisResult",
    "ExplorationResult",
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
