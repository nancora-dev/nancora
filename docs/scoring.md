# Scoring

Conceptual mix: relevance + relationship strength + information value + data quality + coverage − complexity.

Normalized to 0–100. Documented as a **ranking heuristic**. Each candidate stores a decision trace (`ScoreBreakdown.format_trace()`).

Weights live in `src/nancora/engine/score.py` (`BASE_RELEVANCE` and helper functions). Do not describe scores as scientifically universal.
