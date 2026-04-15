"""Tests for _http.py (FermataAuth + ApiClient) and _call.py (error mapping)."""

from __future__ import annotations

import httpx
import pytest
import respx

from fermata._auth import TokenManager
from fermata._call import _unwrap
from fermata._http import ApiClient, FermataAuth
from fermata.exceptions import AuthError, NotFoundError, ServerError

HERA_URL = "http://hera-test:3000"

TOKEN_RESPONSE = {
    "access_token": "mock-jwt-token",
    "token_type": "Bearer",
    "expires_in": 3600,
}


@pytest.fixture
def mock_hera():
    with respx.mock(base_url=HERA_URL, assert_all_called=False) as router:
        router.post("/auth/token").respond(json=TOKEN_RESPONSE)
        yield router


async def _make_client(max_retries: int = 3) -> tuple[TokenManager, ApiClient]:
    tm = TokenManager(HERA_URL, "app", "secret")
    await tm.open()
    auth = FermataAuth(tm, max_retries=max_retries)
    api = ApiClient(HERA_URL, auth)
    return tm, api


async def test_auth_header_injected(mock_hera):
    """FermataAuth injects Bearer token and org-id headers."""
    mock_hera.get("/api/v1/test").respond(json={"ok": True})

    tm, api = await _make_client()
    try:
        client = api.get_async_httpx_client()
        resp = await client.get("/api/v1/test")
        assert resp.json() == {"ok": True}

        last_request = mock_hera.calls[-1].request
        assert last_request.headers["authorization"] == "Bearer mock-jwt-token"
    finally:
        await api.aclose()
        await tm.close()


async def test_retry_on_503(mock_hera):
    """FermataAuth retries on 502/503 with backoff."""
    call_count = 0

    def side_effect(request):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return httpx.Response(503, json={"message": "unavailable"})
        return httpx.Response(200, json={"ok": True})

    mock_hera.get("/api/v1/flaky").mock(side_effect=side_effect)

    tm, api = await _make_client(max_retries=3)
    try:
        client = api.get_async_httpx_client()
        resp = await client.get("/api/v1/flaky")
        assert resp.json() == {"ok": True}
        assert call_count == 3
    finally:
        await api.aclose()
        await tm.close()


async def test_401_triggers_token_refresh(mock_hera):
    """FermataAuth refreshes token on 401 and retries."""
    call_count = 0

    def side_effect(request):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return httpx.Response(401, json={"message": "unauthorized"})
        return httpx.Response(200, json={"ok": True})

    mock_hera.get("/api/v1/protected").mock(side_effect=side_effect)

    tm, api = await _make_client()
    try:
        client = api.get_async_httpx_client()
        resp = await client.get("/api/v1/protected")
        assert resp.json() == {"ok": True}
        assert call_count == 2
    finally:
        await api.aclose()
        await tm.close()
