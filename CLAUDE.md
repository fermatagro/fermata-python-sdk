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
TokenManager (_auth.py)           — self-contained token lifecycle (own httpx client)
  ↓
FermataAuth (_http.py)            — httpx Auth flow: token injection + 401/502/503 retry
  ↓
ApiClient (_http.py)              — duck-types generated AuthenticatedClient
  ↓
call_async (_call.py)             — unwrap generated Response → typed model or exception
  ↓
Async* namespaces (_namespaces/)  — all logic lives here (body building, API calls)
  ↓
Sync* namespaces (_namespaces/)   — typed one-line delegates to Async* via run()
  ↓
Generated code (_generated/)      — models + API functions from OpenAPI specs
```

### Async-first pattern

All logic is written once in `Async*` classes. `Sync*` classes delegate to them via `loop.run_until_complete()`:

```python
# Async — all logic here
class AsyncPipelines:
    async def get_schedule(self, schedule_id: str) -> ModelsSchedule:
        return await call_async(_get_schedule.asyncio_detailed(UUID(schedule_id), client=self._c))

# Sync — typed delegate, zero logic
class SyncPipelines:
    def get_schedule(self, schedule_id: str) -> ModelsSchedule:
        return self._run(self._a.get_schedule(schedule_id))
```

`FermataSync` wraps `Fermata` the same way — no duplicated `infer()` or `_init_pipeline()`.

### Key files

| File | Purpose |
|------|---------|
| `_auth.py` | `TokenManager` — async-only token exchange, caching, auto-refresh. |
| `_http.py` | `FermataAuth` (async httpx Auth flow) + `ApiClient` adapter. All auth + retry logic. |
| `_call.py` | `call_async()` — unwrap generated `Response`, map HTTP status to our exception hierarchy. |
| `_client.py` | `Fermata` — async client. Pipeline init, `infer()` convenience, deterministic photo IDs. |
| `_sync_client.py` | `FermataSync` — wraps `Fermata` with `loop.run_until_complete()`. ~50 lines, no logic duplication. |
| `_namespaces/*.py` | `Async*` classes (logic) + `Sync*` classes (typed delegates). |
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

## README consistency

When changing public API (method signatures, return types, new parameters, new namespaces), update `README.md` in the same commit:
- `infer()` signature block must match actual parameters
- Methods reference table must match actual return types
- `PipelineRun` fields table must match the dataclass
- Code examples must use current API (e.g., typed model attributes, not dict access)
- `photos.create()` returns `None` (not `Photo`)
- `list_schedules()` / `get_schedule()` return typed `Schedule` objects

## Git workflow

- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
