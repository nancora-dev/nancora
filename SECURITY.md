# Security

Nancora is a local library. It reads files the caller provides and writes reports to local paths.

- Do not pass untrusted HTML templates into the report loader (templates are packaged).
- CSV/Excel/JSON/Parquet parsing uses Pandas; treat untrusted files as you would with Pandas.
- No network services, authentication, or secret storage in the MVP.
- Report a vulnerability privately to the maintainers; do not file public issues with exploit details for remote code execution in parsers.
