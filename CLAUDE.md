# Fermata Python SDK

Python client library for Hera API (Fermata On-Site).

## Commands

```bash
make install          # Create venv and install dependencies
make generate         # Copy OpenAPI specs from demetra + regenerate clients
make test             # Run tests (pytest)
make lint             # Lint (ruff + mypy, excludes _generated/)
make fmt              # Format code (ruff)
```

## Architecture

- `src/fermata/_generated/` — auto-generated from OpenAPI specs via `openapi-python-client`. **Never edit manually.**
- `src/fermata/_client.py` — `Fermata` async client with `infer()` convenience
- `src/fermata/_sync_client.py` — `FermataSync` sync wrapper (background event loop thread)
- `src/fermata/_namespaces/` — resource namespace classes (photos, inference, predictions, etc.)
- `src/fermata/_transport.py` — shared httpx client with auth, retry, error mapping
- `src/fermata/_auth.py` — token exchange + auto-refresh
- `src/fermata/types.py` — stable re-exports of generated model types
- `src/fermata/exceptions.py` — exception hierarchy

## Code generation

Generated code in `_generated/` is committed. To regenerate:

```bash
make generate
```

This copies specs from `demetra/api/openapi/` and runs `openapi-python-client` per domain. Generated models use attrs with `from_dict()`/`to_dict()` for JSON serialization.

The hand-written wrapper uses generated models for types but calls Hera endpoints directly via `Transport` (not via generated client/API functions).

## Testing

Tests use `respx` to mock httpx. MinIO uploads (presigned URLs) are mocked separately since they hit a different host than Hera.

## Git Workflow

- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
