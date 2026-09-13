"""Tests for input validation, custom exceptions, and version exposure."""

import pandas as pd
import pytest

import nancora as nc
from nancora.exceptions import (
    AnalysisError,
    ConfigurationError,
    DataError,
    InputError,
    NancoraError,
    ReportError,
)


def test_version_exposure():
    """Verify nancora.__version__ exists and equals 0.1.0."""
    assert hasattr(nc, "__version__")
    assert nc.__version__ == "0.1.0"


def test_exception_hierarchy():
    """Verify custom exception classes inherit from NancoraError."""
    assert issubclass(InputError, NancoraError)
    assert issubclass(ConfigurationError, NancoraError)
    assert issubclass(DataError, NancoraError)
    assert issubclass(AnalysisError, NancoraError)
    assert issubclass(ReportError, NancoraError)


def test_non_dataframe_input():
    """Verify non-DataFrame input raises InputError with helpful message."""
    with pytest.raises(InputError, match="Input dataset is None"):
        nc.explore(None)

    with pytest.raises(InputError, match="Expected a pandas DataFrame, got list"):
        nc.explore([1, 2, 3])

    with pytest.raises(InputError, match="Expected a pandas DataFrame, got dict"):
        nc.explore({"a": [1, 2]})


def test_empty_dataframe_input():
    """Verify empty DataFrame input raises InputError."""
    with pytest.raises(InputError, match="Input dataset is empty"):
        nc.explore(pd.DataFrame())


def test_invalid_target_type():
    """Verify non-string target parameter raises InputError."""
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    with pytest.raises(InputError, match="Target column must be a string"):
        nc.explore(df, target=123)


def test_missing_target_column():
    """Verify nonexistent target column raises InputError."""
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    with pytest.raises(InputError, match="Target column 'invalid_col' not found"):
        nc.explore(df, target="invalid_col")


def test_invalid_max_analyses():
    """Verify non-positive or non-integer max_analyses raises ConfigurationError."""
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

    with pytest.raises(ConfigurationError, match="max_analyses must be an integer >= 1"):
        nc.explore(df, max_analyses=0)

    with pytest.raises(ConfigurationError, match="max_analyses must be an integer >= 1"):
        nc.explore(df, max_analyses=-5)

    with pytest.raises(ConfigurationError, match="max_analyses must be an integer >= 1"):
        nc.explore(df, max_analyses="ten")


def test_valid_pipeline_execution():
    """Verify valid explore and analyze execution."""
    df = pd.DataFrame({
        "age": [20, 30, 40, 50, 60],
        "income": [20000, 40000, 60000, 80000, 100000],
        "city": ["A", "B", "A", "B", "A"],
    })
    res_explore = nc.explore(df)
    assert res_explore is not None
    assert len(res_explore.recommendations) > 0

    res_analyze = nc.analyze(df, target="income")
    assert res_analyze is not None
    assert res_analyze.context.target == "income"
