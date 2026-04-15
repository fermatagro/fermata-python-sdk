# Fermata Python SDK

Python client library for Hera API (Fermata On-Site).

## Commands

```bash
make install          # Create venv and install dependencies
make generate         # Filter OpenAPI specs to Hera-only ops + regenerate clients
make test             # Run unit tests (pytest, excludes integration/)
make lint             # Lint (ruff + mypy, excludes _generated/)
make fmt              # Format code (ruff)
```

## Architecture

```
TokenManager (_auth.py)           — self-contained token lifecycle (own httpx clients)
  ↓
FermataAuth (_http.py)            — httpx Auth flow: token injection + 401/502/503 retry
  ↓
ApiClient / SyncApiClient (_http.py) — duck-types generated AuthenticatedClient
  ↓
call_async / call_sync (_call.py) — unwrap generated Response → typed model or exception
  ↓
Namespaces (_namespaces/*.py)     — thin wrappers around generated API functions
  ↓
Generated code (_generated/)      — models + API functions from OpenAPI specs
```

### Key files

| File | Purpose |
|------|---------|
| `_auth.py` | `TokenManager` — token exchange, caching, auto-refresh. Owns its own httpx clients for `/auth/token`. |
| `_http.py` | `FermataAuth` (httpx Auth flow) + `ApiClient`/`SyncApiClient` adapters. All auth + retry logic lives here. |
| `_call.py` | `call_async()`/`call_sync()` — unwrap generated `Response`, map HTTP status to our exception hierarchy. |
| `_client.py` | `Fermata` — async client. Pipeline init, `infer()` convenience, deterministic photo IDs. |
| `_sync_client.py` | `FermataSync` — sync client. Direct sync calls, no background thread. |
| `_namespaces/*.py` | Each file has `Async*` + `Sync*` classes. Methods are one-liners calling generated functions. |
| `types.py` | Stable re-exports of generated model types (`Schedule`, `GrowingCycle`, `InferenceTask`, etc.) |
| `exceptions.py` | Exception hierarchy: `AuthError`, `NotFoundError`, `ConflictError`, etc. |
| `_generated/` | Auto-generated from filtered OpenAPI specs. **Never edit manually.** |

## Code generation

Generated code is committed. The generation pipeline:

1. Copy full specs from `demetra/api/openapi/*.yml`
2. **Filter** to Hera-only operations via `scripts/filter_spec.py`
3. Run `openapi-python-client` per domain

```bash
make generate
```

### Adding a new SDK method

1. Find the `operationId` in the Demetra OpenAPI spec
2. Add it to the `OPS` map in `scripts/generate.sh`:
   ```bash
   OPS[pipelines]="listSchedules getSchedule createFire newOperationId"
   ```
3. Run `make generate`
4. Use the generated function in your namespace:
   ```python
   from fermata._generated.pipelines.api.fires import new_operation as _new_op

   async def new_method(self, ...) -> SomeModel:
       return await call_async(_new_op.asyncio_detailed(..., client=self._c))
   ```

### How filtering works

`scripts/filter_spec.py` strips OpenAPI specs to only the operations listed in `generate.sh`. It preserves all referenced schemas and parameters transitively. This keeps the generated code minimal (~12 API functions across 6 domains instead of 100+).

## Auth + retry flow

All handled by `FermataAuth` (httpx Auth flow) — no retry logic in namespaces:

```
httpx client.request()
  → FermataAuth.async_auth_flow()
    → inject Bearer + X-Organization-Id
    → yield request → get response
    → 401? → refresh token, yield retry
    → 502/503? → backoff, yield retry (up to 3x)
  → generated _parse_response() → model or error
  → call_async() → 2xx: return model / non-2xx: raise typed exception
```

## Testing

### Unit tests (respx mocks)

```bash
make test
# or
pytest tests/ --ignore=tests/integration
```

- Mock responses must use correct status codes from the OpenAPI spec:
  - `createPhoto` → **201** (no body)
  - `submitInference` → **202**
  - `createPhotoUploadLink` → **200**
  - Everything else → **200**
- MinIO uploads (presigned URLs) are mocked separately via a second `respx.mock()` context

### Integration tests (real Hera)

```bash
# Start on-site infra
cd ../fermata-onsite/deploy && docker compose up -d postgres seaweedfs
docker run -d --name hera --network deploy_fermata-onsite --ip 172.28.0.10 \
  -e HERA_APP_ID=viscon-onsite-01 -e HERA_APP_SECRET=change-me-in-production \
  -e HERA_ORG_ID=org_viscon_nl_01 -e APP_S3_ACCESS_KEY_ID=admin \
  -e APP_S3_SECRET_ACCESS_KEY=admin \
  -e "POSTGRES_URL=postgres://postgres:postgres@172.28.0.2:5432/demetra?sslmode=disable" \
  fermatagro/hera:latest

# Run tests
pytest tests/integration/ -v
```

Tests create their own data (greenhouses, cycles, schedules) via the API.

## Git workflow

- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
