"""Load builtin analyses so they self-register."""

from nancora.analysis.builtin import (  # noqa: F401
    cardinality_analysis,
    categorical_distribution,
    categorical_numeric,
    correlation_analysis,
    datetime_numeric_trend,
    missingness_analysis,
    numeric_distribution,
    numeric_relationship,
    outlier_analysis,
    target_aware,
)
