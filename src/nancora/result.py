"""First-class analysis result: machine-readable, explainable, reportable."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from nancora.analysis.base import AnalysisCandidate, AnalysisContext
from nancora.analysis.evidence import insight_for
from nancora.data.profile import DatasetProfile
from nancora.exceptions import ReportError
from nancora.plot import render as render_plot
from nancora.types import RESULT_SCHEMA_VERSION


@dataclass
class AnalysisResult:
    dataset_profile: DatasetProfile
    selected: list[AnalysisCandidate]
    rejected: list[AnalysisCandidate]
    context: AnalysisContext
    timings: dict[str, float] = field(default_factory=dict)
    frame: pd.DataFrame | None = field(default=None, repr=False, compare=False)

    def summary(self) -> dict[str, Any]:
        return {
            "n_rows": self.dataset_profile.n_rows,
            "n_cols": self.dataset_profile.n_cols,
            "target": self.context.target,
            "n_selected": len(self.selected),
            "n_rejected": len(self.rejected),
            "top_scores": [
                {"analysis_id": c.analysis_id, "variables": list(c.variables), "score": c.score}
                for c in self.selected[:5]
            ],
            "runtime_seconds": self.timings.get("runtime_seconds"),
        }

    def profile(self) -> DatasetProfile:
        return self.dataset_profile

    def recommendations(self) -> list[AnalysisCandidate]:
        return list(self.selected)

    def insights(self) -> list[str]:
        return [insight_for(c) for c in self.selected]

    def rejected_candidates(self) -> list[AnalysisCandidate]:
        return list(self.rejected)


    def visualize(self, backend: str = "matplotlib"):
        if self.frame is None:
            raise ReportError("No DataFrame attached; cannot visualize.")
        figures = []
        for cand in self.selected:
            if cand.viz is None:
                continue
            figures.append(render_plot(self.frame, cand.viz, backend=backend))
        return figures

    def to_dict(self) -> dict[str, Any]:
        return {
            "nancora_result_version": RESULT_SCHEMA_VERSION,
            "summary": self.summary(),
            "profile": self.dataset_profile.to_dict(),
            "recommendations": [c.to_dict() for c in self.selected],
            "rejected": [c.to_dict() for c in self.rejected],
            "insights": self.insights(),
            "context": {
                "target": self.context.target,
                "max_analyses": self.context.max_analyses,
                "rng_seed": self.context.rng_seed,
            },
            "timings": dict(self.timings),
        }

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True, default=str)

    def save(self, path: str | Path) -> Path:
        dest = Path(path)
        if dest.suffix.lower() == ".json":
            dest.write_text(self.to_json(), encoding="utf-8")
            return dest
        if dest.suffix.lower() in {".html", ".htm"}:
            from nancora.report.html import write_html

            return write_html(self, dest)
        raise ReportError(f"Unsupported save suffix: {dest.suffix}")
