# Reports

`result.save("report.html")` writes a Jinja HTML document from `AnalysisResult.to_dict()`.

Sections: summary, recommendations (score + explanation + optional chart), insights, rejected (collapsed), limitations footer.

`result.save("out.json")` writes the same machine-readable payload.
