import nancora as nc


def test_ten_builtin_analyses_registered():
    ids = nc.list_analyses()
    expected = {
        "numeric_distribution",
        "categorical_distribution",
        "numeric_relationship",
        "categorical_numeric",
        "datetime_numeric_trend",
        "correlation_analysis",
        "outlier_analysis",
        "missingness_analysis",
        "cardinality_analysis",
        "target_aware",
    }
    assert expected.issubset(set(ids))
    assert len(expected) == 10
