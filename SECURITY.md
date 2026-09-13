# Security

- Nancora reads local tabular files the caller provides. Treat untrusted CSV/Excel/JSON as untrusted data.
- Reports may embed summary statistics from the input frame. Do not publish reports that contain secrets.
- There is no network service, authentication, or multi-tenant sandbox in this package.
- Please report vulnerabilities privately to the maintainers; do not file public issues with exploit details for production deployments you do not own.
