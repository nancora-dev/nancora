"""Datetime × numeric trend. Ordinal time association, not a forecast."""

from __future__ import annotations

import numpy as np
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
from nancora.plot.spec import PlotSpec
from nancora.stats.tests import spearman
from nancora.types import PAIRWISE_CAP, ColumnKind


@register_analysis
class DatetimeNumericTrend(Analysis):
    id = "datetime_numeric_trend"
    analysis_type = "bivariate"
    intent = "Describe how a numeric column changes with time"
    family = "time_num_pair"
    requirements = AnalysisRequirements(
        min_rows=5,
        column_kinds=(ColumnKind.DATETIME, ColumnKind.NUMERIC),
        min_variables=2,
        max_variables=2,
    )

    def propose(self, profile: DatasetProfile, context: AnalysisContext) -> list[CandidateDraft]:
        times = profile.names_of(ColumnKind.DATETIME)
        nums = ranked_numeric_names(profile)
        drafts = []
        for t in times:
            for num in nums:
                drafts.append(
                    CandidateDraft(
                        analysis_id=self.id,
                        analysis_type=self.analysis_type,
                        intent=self.intent,
                        variables=(t, num),
                        requirements=self.requirements,
                        family=self.family,
                        complexity=2.3,
                        viz=PlotSpec(kind="line", title=f"{num} over {t}", x=t, y=num),
                    )
                )
                if len(drafts) >= PAIRWISE_CAP:
                    return drafts
        return drafts

    def compute_evidence(self, df: pd.DataFrame, candidate: AnalysisCandidate) -> Evidence:
        t, num = candidate.variables
        ts = pd.to_datetime(df[t], errors="coerce")
        ordinal = ts.to_numpy(dtype="datetime64[ns]").astype("int64").astype(float)
        ordinal[ts.isna().to_numpy()] = np.nan
        stats = spearman(ordinal, df[num])
        return Evidence(
            stats=dict(stats),
            provenance={
                "library": str(stats.get("library", "scipy.stats")),
                "method": "spearman_time_ordinal",
            },
            notes=["Time association is not a forecast or causal effect."],
        )
