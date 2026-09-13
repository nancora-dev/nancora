# Scoring

Conceptual (heuristic):

relevance + relationship strength + information value + data quality + coverage − redundancy − complexity

Normalized to 0–100 and clamped. Every selected candidate stores a decision trace, for example:

```
Base relevance: 82
Relationship strength: +14
...
Final score: 94.2
```

This is **not** a scientifically universal quality score.
