# Data

`nc.read_csv`, `nc.read_excel`, `nc.read_json`, `nc.read_parquet` delegate to Pandas.

`nc.data.infer_schema` and `nc.data.profile` produce the typed profile the engine uses.

Transforms are few and engine-needed: `drop_constant`, `coerce_datetime`.
