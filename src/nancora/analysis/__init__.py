"""Analysis registry and listing. Builtin analyses register on import."""

from nancora.analysis import builtin as _builtin  # noqa: F401
from nancora.analysis.registry import get_analysis, list_analyses, register_analysis

__all__ = ["get_analysis", "list_analyses", "register_analysis"]
