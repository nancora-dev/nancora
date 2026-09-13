from nancora.data.schema import infer_schema
from nancora.types import ColumnKind
from tests.conftest import mixed_frame


def test_infer_numeric_and_categorical_and_datetime():
    df = mixed_frame()
    schema = {col.name: col for col in infer_schema(df)}
    assert schema["spend"].kind == ColumnKind.NUMERIC
    assert schema["region"].kind == ColumnKind.CATEGORICAL
    assert schema["day"].kind == ColumnKind.DATETIME
    assert schema["partial"].missing_rate > 0
