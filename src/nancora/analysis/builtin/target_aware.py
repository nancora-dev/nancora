"""Target-aware views. Prioritized when analyze(target=...) is used — not AutoML."""

from __future__ import annotations

from typing import Any

import pandas as pd

from nancora.analysis.base import (
    Analysis,
    AnalysisCandidate,
    AnalysisContext,
    AnalysisRequirements,
    CandidateDraft,
    Evidence,
)
from nancora.analysis.pairing import ranked_numeric_names
from nancora.analysis.registry import register_analysis
from nancora.data.profile import DatasetProfile
from nancora.numeric.arrays import nan_aware_stats
from nancora.plot.spec import PlotSpec
from nancora.stats.tests import f_oneway_groups, pearson
from nancora.types import CATEGORICAL_LEVEL_CAP, ColumnKind


@register_analysis
class TargetAware(Analysis):
    id = "target_aware"
    analysis_type = "target"
    intent = "Relate columns to a specified target"
    family = "target"
    requirements = AnalysisRequirements(
        min_rows=5, min_variables=1, max_variables=2, needs_target=True
    )

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        if not context.target or profile.column(context.target) is None:
            return []
        target = context.target
        tcol = profile.column(target)
        drafts: list[CandidateDraft] = []
        drafts.append(
            CandidateDraft(
                analysis_id=self.id,
                analysis_type=self.analysis_type,
                intent="Describe the target column",
                variables=(target,),
                requirements=self.requirements,
                family="target_univariate",
                complexity=1.0,
                viz=PlotSpec(
                    kind="hist" if tcol and tcol.kind == ColumnKind.NUMERIC else "bar",
                    title=f"Target distribution: {target}",
                    x=target,
                ),
            )
        )
        if tcol and tcol.kind == ColumnKind.NUMERIC:
            for name in ranked_numeric_names(profile, exclude={target})[:8]:
                a, b = sorted((name, target))
                drafts.append(
                    CandidateDraft(
                        analysis_id=self.id,
                        analysis_type=self.analysis_type,
                        intent="Numeric association with the target",
                        variables=(a, b),
                        requirements=self.requirements,
                        family="target_numeric_pair",
                        complexity=2.0,
                        viz=PlotSpec(
                            kind="scatter", title=f"{name} vs target {target}", x=name, y=target
                        ),
                    )
                )
        cats = []
        for n in profile.names_of(ColumnKind.CATEGORICAL, ColumnKind.BOOLEAN):
            cinfo = profile.column(n)
            if n != target and cinfo is not None and cinfo.n_unique <= CATEGORICAL_LEVEL_CAP:
                cats.append(n)
        if tcol and tcol.kind == ColumnKind.NUMERIC:
            for cat in cats[:8]:
                drafts.append(
                    CandidateDraft(
                        analysis_id=self.id,
                        analysis_type=self.analysis_type,
                        intent="Target by categorical group",
                        variables=(cat, target),
                        requirements=self.requirements,
                        family="target_cat_num",
                        complexity=2.1,
                        viz=PlotSpec(
                            kind="box", title=f"Target {target} by {cat}", x=cat, y=target
                        ),
                    )
                )
        return drafts

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        vars_ = candidate.variables
        stats: dict[str, Any]
        if len(vars_) == 1:
            name = vars_[0]
            if pd.api.types.is_numeric_dtype(df[name]):
                stats = dict(nan_aware_stats(df[name]))
            else:
                stats = {
                    "n_levels": int(df[name].nunique(dropna=True)),
                    "n": int(df[name].notna().sum()),
                }
            return Evidence(
                stats=stats,
                provenance={"library": "pandas/numpy", "method": "target_univariate"},
                notes=["Target description only; not a predictive model."],
            )
        a, b = vars_
        if pd.api.types.is_numeric_dtype(df[a]) and pd.api.types.is_numeric_dtype(df[b]):
            stats = dict(pearson(df[a], df[b]))
        else:
            cat = a if not pd.api.types.is_numeric_dtype(df[a]) else b
            num = b if cat == a else a
            stats = dict(f_oneway_groups(df[num], df[cat]))
        return Evidence(
            stats=dict(stats),
            provenance={
                "library": "scipy.stats",
                "method": str(stats.get("method", "target_assoc")),
            },
            notes=["Association with the target is not causation and not a fitted model."],
        )
