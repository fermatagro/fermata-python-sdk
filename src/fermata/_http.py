"""HTTP infrastructure: auth flow and API client adapter."""

from __future__ import annotations

import asyncio
import typing

import httpx

from fermata._auth import TokenManager

_RETRYABLE = {502, 503}
_BACKOFF = [0.5, 1.0, 2.0]


class FermataAuth(httpx.Auth):
    """httpx Auth flow: injects Bearer + org-id, retries on 401 + 502/503.

    Async-only — sync client wraps the async client via event loop.
    """

    requires_response_body = False

    def __init__(self, token_manager: TokenManager, *, max_retries: int = 3) -> None:
        self._tm = token_manager
        self._max_retries = max_retries

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> typing.AsyncGenerator[httpx.Request, httpx.Response]:
        request.headers["Authorization"] = f"Bearer {await self._tm.get_token()}"
        if self._tm.org_id:
            request.headers["X-Organization-Id"] = self._tm.org_id

        response = yield request

        # 401: refresh + retry once
        if response.status_code == 401:
            await self._tm.force_refresh()
            request.headers["Authorization"] = f"Bearer {await self._tm.get_token()}"
            response = yield request

        # 502/503: backoff retry
        for attempt in range(self._max_retries):
            if response.status_code not in _RETRYABLE:
                break
            await asyncio.sleep(_BACKOFF[min(attempt, len(_BACKOFF) - 1)])
            response = yield request


class ApiClient:
    """Async API client that duck-types the generated AuthenticatedClient interface."""

    raise_on_unexpected_status = False

    def __init__(self, base_url: str, auth: FermataAuth, *, timeout: float = 30.0) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, auth=auth, timeout=timeout)

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        return self._client

    async def aclose(self) -> None:
        await self._client.aclose()
