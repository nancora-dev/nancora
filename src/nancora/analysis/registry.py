"""Internal analysis registry. Future plugins use the same decorator; there is no marketplace."""

from __future__ import annotations

from nancora.analysis.base import Analysis

_REGISTRY: dict[str, Analysis] = {}


def register_analysis(cls=None):
    """Register an Analysis implementation. Usable as @register_analysis or @register_analysis()."""

    def deco(klass):
        instance = klass()
        analysis_id = getattr(instance, "id", None) or getattr(klass, "id")
        _REGISTRY[analysis_id] = instance
        return klass

    if cls is None:
        return deco
    return deco(cls)


def get_analysis(analysis_id: str) -> Analysis:
    if analysis_id not in _REGISTRY:
        raise KeyError(f"Unknown analysis: {analysis_id}")
    return _REGISTRY[analysis_id]


def list_analyses() -> list[str]:
    return sorted(_REGISTRY)


def all_analyses() -> list[Analysis]:
    return [_REGISTRY[k] for k in list_analyses()]
