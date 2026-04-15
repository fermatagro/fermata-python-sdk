"""HTTP infrastructure: auth flow, retry, and API client adapter."""

from __future__ import annotations

import asyncio
import time
import typing

import httpx

from fermata._auth import TokenManager

_RETRYABLE = {502, 503}
_BACKOFF = [0.5, 1.0, 2.0]


class FermataAuth(httpx.Auth):
    """httpx Auth flow: injects Bearer + org-id, retries on 401 + 502/503.

    Uses httpx's built-in auth flow mechanism — each ``yield request``
    sends one HTTP request and receives the response back into the generator.
    Multiple yields = retries.
    """

    requires_response_body = False

    def __init__(self, token_manager: TokenManager, *, max_retries: int = 3) -> None:
        self._tm = token_manager
        self._max_retries = max_retries

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> typing.AsyncGenerator[httpx.Request, httpx.Response]:
        # Inject auth headers
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

    def sync_auth_flow(
        self, request: httpx.Request
    ) -> typing.Generator[httpx.Request, httpx.Response, None]:
        # Inject auth headers
        request.headers["Authorization"] = f"Bearer {self._tm.get_token_sync()}"
        if self._tm.org_id:
            request.headers["X-Organization-Id"] = self._tm.org_id

        response = yield request

        # 401: refresh + retry once
        if response.status_code == 401:
            self._tm.force_refresh_sync()
            request.headers["Authorization"] = f"Bearer {self._tm.get_token_sync()}"
            response = yield request

        # 502/503: backoff retry
        for attempt in range(self._max_retries):
            if response.status_code not in _RETRYABLE:
                break
            time.sleep(_BACKOFF[min(attempt, len(_BACKOFF) - 1)])
            response = yield request


class ApiClient:
    """Async API client that duck-types the generated AuthenticatedClient interface.

    Generated API functions only use ``client.get_async_httpx_client()`` and
    ``client.raise_on_unexpected_status``.
    """

    raise_on_unexpected_status = False

    def __init__(self, base_url: str, auth: FermataAuth, *, timeout: float = 30.0) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, auth=auth, timeout=timeout)

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        return self._client

    async def aclose(self) -> None:
        await self._client.aclose()


class SyncApiClient:
    """Sync API client that duck-types the generated AuthenticatedClient interface.

    Generated API functions only use ``client.get_httpx_client()`` and
    ``client.raise_on_unexpected_status``.
    """

    raise_on_unexpected_status = False

    def __init__(self, base_url: str, auth: FermataAuth, *, timeout: float = 30.0) -> None:
        self._client = httpx.Client(base_url=base_url, auth=auth, timeout=timeout)

    def get_httpx_client(self) -> httpx.Client:
        return self._client

    def close(self) -> None:
        self._client.close()
