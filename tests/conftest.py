import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")


def mixed_frame(n: int = 40) -> pd.DataFrame:
    x = pd.Series(range(n), dtype=float)
    partial = pd.Series([1.0, np.nan] * (n // 2))
    return pd.DataFrame(
        {
            "spend": x,
            "revenue": x * 2 + 0.01,
            "noise": pd.Series(n * [0.0]) + pd.Series(range(n)).mod(3),
            "region": ["east", "west"] * (n // 2),
            "day": pd.date_range("2021-01-01", periods=n, freq="D"),
            "partial": partial,
        }
    )

