"""Cardinality of categorical-like columns (including high-cardinality flags)."""

from __future__ import annotations

import pandas as pd

from nancora.analysis.base import (
    Analysis,
    AnalysisCandidate,
    AnalysisContext,
    AnalysisRequirements,
    CandidateDraft,
    Evidence,
)
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.plot.spec import PlotSpec
from nancora.types import ColumnKind


@register_analysis
class CardinalityAnalysis(Analysis):
    id = "cardinality_analysis"
    analysis_type = "univariate"
    intent = "Measure uniqueness of a column"
    family = "cardinality"
    requirements = AnalysisRequirements(min_rows=1, min_variables=1, max_variables=1)

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        drafts = []
        names = profile.names_of(
            ColumnKind.CATEGORICAL, ColumnKind.TEXT, ColumnKind.BOOLEAN, include_id=True
        )
        names += [c.name for c in profile.columns if c.name in profile.high_cardinality]
        seen = set()
        for name in names:
            if name in seen:
                continue
            seen.add(name)
            drafts.append(
                CandidateDraft(
                    analysis_id=self.id,
                    analysis_type=self.analysis_type,
                    intent=self.intent,
                    variables=(name,),
                    requirements=self.requirements,
                    family=self.family,
                    complexity=1.0,
                    viz=PlotSpec(kind="bar", title=f"Cardinality of {name}", x=name),
                )
            )
        return drafts[:15]

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        name = candidate.variables[0]
        n = max(len(df), 1)
        n_unique = int(df[name].nunique(dropna=True))
        return Evidence(
            stats={
                "n_unique": n_unique,
                "unique_ratio": float(n_unique / n),
                "n": int(df[name].notna().sum()),
            },
            provenance={"library": "pandas", "method": "nunique"},
            notes=["High uniqueness may indicate an identifier."],
        )
