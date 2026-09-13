# Recommendation engine

`generate → validate → evidence → score → redundancy → coverage bonus → rank/select`

`nc.explore` and `nc.analyze` share this pipeline. `analyze` sets `target` on `AnalysisContext`.

Rejected candidates are retained with machine-readable `reject_reason` values.
