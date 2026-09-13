"""Backend-agnostic plot description produced by analyses."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class PlotSpec:
    kind: str
    title: str
    x: str | None = None
    y: str | None = None
    color: str | None = None
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)
