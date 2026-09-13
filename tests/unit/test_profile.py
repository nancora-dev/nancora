from tests.conftest import mixed_frame

from nancora.data.profile import profile


def test_profile_counts():
    df = mixed_frame()
    result = profile(df)
    assert result.n_rows == len(df)
    assert result.n_columns == df.shape[1]
    assert "partial" in result.missing_columns
    payload = result.to_dict()
    assert "columns" in payload
