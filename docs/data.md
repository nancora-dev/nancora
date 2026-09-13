# Data

`nc.read_csv`, `nc.read_json`, optional Excel/Parquet extras.

`nc.data.infer_schema` assigns kinds: numeric, categorical, datetime, boolean, text, unknown.

`nc.data.profile` builds `DatasetProfile` (row/column counts, missing columns, high cardinality, constants, ids).

Transforms: `drop_constant`, `coerce_datetime` — only helpers the engine needs.
