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
from nancora.plot import render as render_plot
from nancora.types import RESULT_SCHEMA_VERSION


class CallableList(list):
    def __call__(self) -> CallableList:
        return self


@dataclass
class AnalysisResult:
    dataset_profile: DatasetProfile
    selected: list[AnalysisCandidate]
    rejected: list[AnalysisCandidate]
    context: AnalysisContext
    timings: dict[str, float] = field(default_factory=dict)
    frame: pd.DataFrame | None = field(default=None, repr=False, compare=False)

    @property
    def profile(self) -> DatasetProfile:
        return self.dataset_profile

    @property
    def recommendations(self) -> CallableList[AnalysisCandidate]:
        return CallableList(self.selected)

    @property
    def insights(self) -> CallableList[str]:
        return CallableList(insight_for(c) for c in self.selected)

    @property
    def rejected_candidates(self) -> CallableList[AnalysisCandidate]:
        return CallableList(self.rejected)

    @property
    def visualizations(self) -> CallableList[Any]:
        if self.frame is None:
            return CallableList()
        figures = []
        for cand in self.selected:
            if cand.viz is not None:
                figures.append(render_plot(self.frame, cand.viz, backend="matplotlib"))
        return CallableList(figures)

    @property
    def decision_trace(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "selected": [self.explain(c.analysis_id) for c in self.selected],
            "rejected": [
                {
                    "analysis_id": r.analysis_id,
                    "variables": list(r.variables),
                    "reason": r.reject_reason.value if r.reject_reason else r.status.value,
                    "explanation": r.explanation,
                }
                for r in self.rejected
            ],
        }

    def explain(self, target: int | str = 0) -> dict[str, Any]:
        from nancora.engine.explain import explain_decision

        if not self.selected:
            return {"error": "No candidates selected"}
        cand: AnalysisCandidate | None = None
        if isinstance(target, int):
            if 0 <= target < len(self.selected):
                cand = self.selected[target]
        elif isinstance(target, str):
            for c in self.selected:
                if c.analysis_id == target:
                    cand = c
                    break
        if cand is None:
            cand = self.selected[0]
        return explain_decision(cand, self.rejected)


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "nancora_result_version": RESULT_SCHEMA_VERSION,
            "summary": self.summary(),
            "profile": self.dataset_profile.to_dict(),
            "recommendations": [c.to_dict() for c in self.selected],
            "rejected": [c.to_dict() for c in self.rejected],
            "insights": list(self.insights),
            "context": self.context.to_dict(),
            "timings": self.timings,
        }

    def to_json(self, indent: int | None = None) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: str | Path) -> Path:
        from nancora.report.html import write_html

        return write_html(self, path)

    def visualize(self, backend: str = "matplotlib") -> list[Any]:
        if self.frame is None:
            return []
        figures = []
        for cand in self.selected:
            if cand.viz is not None:
                figures.append(render_plot(self.frame, cand.viz, backend=backend))
        return figures

    def _repr_html_(self) -> str:
        target_str = (
            f" • Target: <strong>{self.context.target}</strong>" if self.context.target else ""
        )
        rec_rows = []
        for i, c in enumerate(self.selected, 1):
            score_val = c.score or 0.0
            score_color = (
                "#10b981" if score_val >= 70 else "#f59e0b" if score_val >= 50 else "#6b7280"
            )
            vars_str = ", ".join(c.variables)
            evidence_str = ""
            if c.evidence and c.evidence.notes:
                evidence_str = (
                    f"<br/><small style='color:#6b7280;'>Evidence: {c.evidence.notes[0]}</small>"
                )
            rec_rows.append(
                f'<tr style="border-bottom: 1px solid #e5e7eb;">\n'
                f'    <td style="padding: 8px; font-weight: 600; text-align: center; '
                f'color: #374151;">#{i}</td>\n'
                f'    <td style="padding: 8px;">\n'
                f'        <strong style="color: #111827;">{c.analysis_id}</strong>\n'
                f'        <span style="color: #6b7280; font-size: 0.85em;"> ({vars_str})</span>\n'
                f'        <div style="color: #4b5563; font-size: 0.85em; margin-top: 2px;">'
                f'{c.intent}</div>\n'
                f"        {evidence_str}\n"
                f"    </td>\n"
                f'    <td style="padding: 8px; text-align: right; vertical-align: top;">\n'
                f'        <span style="background-color: {score_color}; color: white; '
                f'padding: 2px 7px; border-radius: 10px; font-weight: 600; font-size: 0.8em;">\n'
                f"            {score_val:.1f}\n"
                f"        </span>\n"
                f"    </td>\n"
                f"</tr>\n"
            )
        insight_items = "".join(
            f"<li style='margin-bottom: 3px;'>{insight}</li>" for insight in self.insights
        )
        rejected_rows = []
        for r in self.rejected:
            reason = r.reject_reason.value if r.reject_reason else r.status.value
            vars_str = ", ".join(r.variables)
            rejected_rows.append(
                f"<li><code>{r.analysis_id}</code> ({vars_str}) &mdash; "
                f"<span style='color:#ef4444;'>{reason}</span></li>"
            )
        rejected_html = ""
        if rejected_rows:
            rejected_html = (
                f'<details style="margin-top: 12px; color: #4b5563; font-size: 0.85em;">\n'
                f'    <summary style="cursor: pointer; font-weight: 600; color: #374151;">\n'
                f"        Skipped / Redundant Analyses ({len(self.rejected)})\n"
                f"    </summary>\n"
                f'    <ul style="margin-top: 6px; padding-left: 18px;">\n'
                f'        {"".join(rejected_rows)}\n'
                f"    </ul>\n"
                f"</details>\n"
            )
        n_rows = self.dataset_profile.n_rows
        n_cols = self.dataset_profile.n_cols
        return (
            f'<div style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, '
            f'sans-serif; border: 1px solid #e5e7eb; border-radius: 8px; padding: 14px; '
            f'background-color: #ffffff; max-width: 780px; '
            f'box-shadow: 0 1px 3px rgba(0,0,0,0.05);">\n'
            f'    <div style="display: flex; justify-content: space-between; align-items: center; '
            f'border-bottom: 2px solid #3b82f6; padding-bottom: 6px; margin-bottom: 10px;">\n'
            f"        <div>\n"
            f'            <h3 style="margin: 0; color: #1e3a8a; font-size: 1.15em;">'
            f"Nancora Exploration Result</h3>\n"
            f'            <div style="color: #6b7280; font-size: 0.8em; margin-top: 2px;">\n'
            f"                Rows: <strong>{n_rows}</strong> • Columns: "
            f"<strong>{n_cols}</strong>{target_str}\n"
            f"            </div>\n"
            f"        </div>\n"
            f'        <div style="background: #dbeafe; color: #1e40af; padding: 3px 8px; '
            f'border-radius: 10px; font-weight: 600; font-size: 0.75em;">\n'
            f"            {len(self.selected)} Recommendations\n"
            f"        </div>\n"
            f"    </div>\n"
            f'    <div style="margin-bottom: 12px;">\n'
            f'        <h4 style="margin: 0 0 6px 0; color: #1f2937; font-size: 0.95em;">'
            f"Prioritized Recommendations</h4>\n"
            f'        <table style="width: 100%; border-collapse: collapse; text-align: left; '
            f'font-size: 0.85em;">\n'
            f"            <thead>\n"
            f'                <tr style="background-color: #f9fafb; color: #4b5563; '
            f'border-bottom: 1px solid #e5e7eb;">\n'
            f'                    <th style="padding: 5px 8px; width: 35px; '
            f'text-align: center;">Rank</th>\n'
            f'                    <th style="padding: 5px 8px;">Analysis Direction</th>\n'
            f'                    <th style="padding: 5px 8px; text-align: right; '
            f'width: 60px;">Score</th>\n'
            f"                </tr>\n"
            f"            </thead>\n"
            f"            <tbody>\n"
            f'                {"".join(rec_rows)}\n'
            f"            </tbody>\n"
            f"        </table>\n"
            f"    </div>\n"
            f'    <div style="background-color: #f8fafc; border-left: 3px solid #3b82f6; '
            f'padding: 8px 12px; margin-bottom: 10px; border-radius: 0 4px 4px 0;">\n'
            f'        <h4 style="margin: 0 0 4px 0; color: #1e293b; font-size: 0.9em;">'
            f"Key Analytical Insights</h4>\n"
            f'        <ul style="margin: 0; padding-left: 16px; color: #334155; '
            f'font-size: 0.85em;">\n'
            f"            {insight_items}\n"
            f"        </ul>\n"
            f"    </div>\n"
            f"    {rejected_html}\n"
            f"</div>\n"
        )


ExplorationResult = AnalysisResult
