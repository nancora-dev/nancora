# Implementation phases

Each phase is independently testable. Do not skip tests to “finish the ecosystem.”

## Phase 0 — Skeleton

Package layout, public API, CI smoke import.

**Done when:** `pip install -e .` and `import nancora` succeed; GitHub Actions runs pytest and ruff.

## Phase 1 — Data and profile

CSV/JSON IO, schema inference, `DatasetProfile`.

**Done when:** `nc.read_csv` and `profile` tests pass on a mixed fixture.

## Phase 2 — Registry, first analyses, evidence

Builtin analyses register; `explore` returns evidenced candidates and JSON.

**Done when:** mixed-frame `explore` selects ≥1 candidate; `to_json` round-trips.

## Phase 3 — Scoring, redundancy, ranking

Heuristic traces; symmetric and similar rejection.

**Done when:** decision tests pass (strong pairs, symmetric collapse).

## Phase 4 — Full MVP analyses and targets

Ten registered analysis ids; `analyze(target=)` prioritizes target views.

**Done when:** registry test and target prioritization test pass.

## Phase 5 — Visualization and HTML

`PlotSpec` → Matplotlib/Plotly; `save("report.html")`.

**Done when:** HTML contains scores and rejected analyses; headless plots render.

## Phase 6 — CLI, docs, benchmark foundation

Typer CLI; documentation set; benchmark runner that **skips** without labels.

**Done when:** `nancora explore fixture.csv --out report.html` works; docs exist; runner prints `no labels; skip scoring` on empty labels.
