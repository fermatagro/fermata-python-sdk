from __future__ import annotations

import pytest
import respx
import httpx

from fermata._auth import TokenManager
from fermata._transport import Transport
from fermata.exceptions import NotFoundError, ServerError, ConnectionError

HERA_URL = "http://hera-test:3000"

TOKEN_RESPONSE = {
    "access_token": "mock-jwt",
    "token_type": "Bearer",
    "expires_in": 3600,
}


@pytest.fixture
def token_mock(mock_hera):
    """Token endpoint is already mocked by conftest."""
    return mock_hera


async def test_auth_header_injected(mock_hera):
    mock_hera.get("/api/v1/test").respond(json={"ok": True})

    tm = TokenManager(HERA_URL, "app", "secret")
    async with Transport(HERA_URL, tm) as t:
        resp = await t.request("GET", "/api/v1/test")
        assert resp.json() == {"ok": True}

    # Verify auth header was sent
    last_request = mock_hera.calls[-1].request
    assert last_request.headers["authorization"] == "Bearer mock-jwt-token"


async def test_404_raises_not_found(mock_hera):
    mock_hera.get("/api/v1/missing").respond(status_code=404, json={"message": "not found"})

    tm = TokenManager(HERA_URL, "app", "secret")
    async with Transport(HERA_URL, tm) as t:
        with pytest.raises(NotFoundError):
            await t.request("GET", "/api/v1/missing")


async def test_500_raises_server_error(mock_hera):
    mock_hera.get("/api/v1/broken").respond(status_code=500, json={"message": "internal error"})

    tm = TokenManager(HERA_URL, "app", "secret")
    async with Transport(HERA_URL, tm) as t:
        with pytest.raises(ServerError):
            await t.request("GET", "/api/v1/broken")


async def test_retry_on_503(mock_hera):
    call_count = 0

    def side_effect(request):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return httpx.Response(503, json={"message": "unavailable"})
        return httpx.Response(200, json={"ok": True})

    mock_hera.get("/api/v1/flaky").mock(side_effect=side_effect)

    tm = TokenManager(HERA_URL, "app", "secret")
    async with Transport(HERA_URL, tm, max_retries=3) as t:
        resp = await t.request("GET", "/api/v1/flaky")
        assert resp.json() == {"ok": True}
        assert call_count == 3
