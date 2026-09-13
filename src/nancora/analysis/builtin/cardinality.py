"""Cardinality scan for categorical and identifier-like columns."""

from __future__ import annotations

import pandas as pd

from nancora.analysis.base import AnalysisContext, CandidateDraft, Evidence
from nancora.analysis.evidence import evidence_from_stats
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.types import ColumnKind, PlotKind


@register_analysis
class CardinalityAnalysis:
    id = "cardinality"
    analysis_type = "quality"
    intent = "Report unique-value counts that affect grouping and identifiers."

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        cols = [
            c.name
            for c in profile.columns
            if c.kind in {ColumnKind.CATEGORICAL, ColumnKind.BOOLEAN, ColumnKind.TEXT, ColumnKind.NUMERIC}
        ]
        cols = sorted(cols)[: context.max_univariate]
        if not cols:
            return []
        return [
            CandidateDraft(
                analysis_id=self.id,
                analysis_type=self.analysis_type,
                intent=self.intent,
                variables=tuple(cols),
                requirements={"min_rows": 1},
            )
        ]

    def compute_evidence(self, df: pd.DataFrame, draft: CandidateDraft) -> Evidence:
        card = {}
        for name in draft.variables:
            n_unique = int(df[name].nunique(dropna=True))
            n = max(int(df[name].notna().sum()), 1)
            card[name] = {
                "n_unique": n_unique,
                "unique_ratio": float(n_unique / n),
            }
        stats = {"cardinality": card}
        return evidence_from_stats(stats, method="nunique", library="pandas")

    def plot_spec(self, draft: CandidateDraft, evidence: Evidence) -> PlotSpec:
        return PlotSpec(
            kind=PlotKind.BAR,
            title="Column cardinality",
            columns=list(draft.variables),
            extra={"source": "cardinality"},
        )

    def insight(self, draft: CandidateDraft, evidence: Evidence) -> str:
        card = evidence.stats.get("cardinality", {})
        high = [name for name, payload in card.items() if payload.get("unique_ratio", 0) > 0.9]
        if high:
            return f"High unique-value ratio in: {', '.join(sorted(high))}."
        return "No column is close to a unique identifier based on unique-value ratio."
