import numpy as np

from nancora import numpy as ncnp
from nancora import stats as ncstats


def test_nan_aware_stats_and_pearson():
    x = np.array([1.0, 2.0, 3.0, np.nan])
    stats = ncnp.nan_aware_stats(x)
    assert stats["n"] == 3
    y = np.array([2.0, 4.0, 6.0, 8.0])
    x2 = np.array([1.0, 2.0, 3.0, 4.0])
    pear = ncstats.pearson(x2, y)
    assert pear["coefficient"] > 0.99
    assert pear["library"].startswith("scipy")
