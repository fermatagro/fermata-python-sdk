from __future__ import annotations

import httpx
import pytest
import respx

from fermata._auth import TokenManager
from fermata.exceptions import AuthError, ConnectionError

HERA_URL = "http://hera-test:3000"


async def test_token_exchange():
    with respx.mock(base_url=HERA_URL) as router:
        router.post("/auth/token").respond(json={
            "access_token": "jwt-123",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

        tm = TokenManager(HERA_URL, "user", "pass")
        await tm.open()
        try:
            token = await tm.get_token()
            assert token == "jwt-123"
        finally:
            await tm.close()


async def test_token_cached():
    call_count = 0

    def side_effect(request):
        nonlocal call_count
        call_count += 1
        return httpx.Response(200, json={
            "access_token": f"jwt-{call_count}",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

    with respx.mock(base_url=HERA_URL) as router:
        router.post("/auth/token").mock(side_effect=side_effect)

        tm = TokenManager(HERA_URL, "user", "pass")
        await tm.open()
        try:
            t1 = await tm.get_token()
            t2 = await tm.get_token()
            assert t1 == t2
            assert call_count == 1
        finally:
            await tm.close()


async def test_force_refresh():
    call_count = 0

    def side_effect(request):
        nonlocal call_count
        call_count += 1
        return httpx.Response(200, json={
            "access_token": f"jwt-{call_count}",
            "token_type": "Bearer",
            "expires_in": 3600,
        })

    with respx.mock(base_url=HERA_URL) as router:
        router.post("/auth/token").mock(side_effect=side_effect)

        tm = TokenManager(HERA_URL, "user", "pass")
        await tm.open()
        try:
            t1 = await tm.get_token()
            await tm.force_refresh()
            t2 = await tm.get_token()
            assert t1 != t2
            assert call_count == 2
        finally:
            await tm.close()


async def test_token_exchange_failure():
    with respx.mock(base_url=HERA_URL) as router:
        router.post("/auth/token").respond(status_code=401, json={"error": "invalid_credentials"})

        tm = TokenManager(HERA_URL, "bad-user", "bad-pass")
        await tm.open()
        try:
            with pytest.raises(AuthError):
                await tm.get_token()
        finally:
            await tm.close()


async def test_token_exchange_connection_error_is_clean(monkeypatch):
    """Network failure → typed ConnectionError, no chained traceback by default."""
    monkeypatch.delenv("FERMATA_DEBUG", raising=False)

    with respx.mock(base_url=HERA_URL) as router:
        request = httpx.Request("POST", f"{HERA_URL}/auth/token")
        router.post("/auth/token").mock(side_effect=httpx.ConnectTimeout("boom", request=request))

        tm = TokenManager(HERA_URL, "user", "pass")
        await tm.open()
        try:
            with pytest.raises(ConnectionError) as exc_info:
                await tm.get_token()
        finally:
            await tm.close()

    exc = exc_info.value
    assert "timed out" in str(exc)
    assert HERA_URL in str(exc)
    # Chained traceback suppressed for end users
    assert exc.__cause__ is None
    assert exc.__suppress_context__ is True
    # Original still preserved on __context__ for debuggers
    assert isinstance(exc.__context__, httpx.ConnectTimeout)


async def test_token_exchange_connection_error_debug_mode(monkeypatch):
    """FERMATA_DEBUG=1 exposes the chained traceback for debugging."""
    monkeypatch.setenv("FERMATA_DEBUG", "1")

    with respx.mock(base_url=HERA_URL) as router:
        request = httpx.Request("POST", f"{HERA_URL}/auth/token")
        router.post("/auth/token").mock(side_effect=httpx.ConnectError("refused", request=request))

        tm = TokenManager(HERA_URL, "user", "pass")
        await tm.open()
        try:
            with pytest.raises(ConnectionError) as exc_info:
                await tm.get_token()
        finally:
            await tm.close()

    exc = exc_info.value
    # Full chain exposed: explicit __cause__ makes the default traceback printer
    # render "The above exception was the direct cause of the following exception".
    assert isinstance(exc.__cause__, httpx.ConnectError)
