from __future__ import annotations

import asyncio
from typing import Any, Self

import httpx

from fermata._auth import TokenManager
from fermata.exceptions import AuthError, ConnectionError, raise_for_status

_RETRYABLE_STATUS = {502, 503}
_BACKOFF_SCHEDULE = [0.5, 1.0, 2.0]


class Transport:
    """HTTP transport with auth injection, retry, and error mapping.

    Owns a shared httpx.AsyncClient used by all namespace methods.
    """

    def __init__(
        self,
        base_url: str,
        token_manager: TokenManager,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._base_url = base_url
        self._token_manager = token_manager
        self._timeout = timeout
        self._max_retries = max_retries
        self._client: httpx.AsyncClient | None = None
        self._raw_client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
        )
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._raw_client is not None:
            await self._raw_client.aclose()
            self._raw_client = None
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Transport not initialized — use 'async with' context manager")
        return self._client

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        content: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Make an authenticated request with retry logic."""
        last_exc: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                token = await self._token_manager.get_token(self.client)
                req_headers = {"Authorization": f"Bearer {token}"}
                org_id = self._token_manager.org_id
                if org_id:
                    req_headers["X-Organization-Id"] = org_id
                if headers:
                    req_headers.update(headers)

                # Filter out None values from params
                clean_params = {k: v for k, v in (params or {}).items() if v is not None}

                response = await self.client.request(
                    method,
                    path,
                    json=json,
                    content=content,
                    params=clean_params or None,
                    headers=req_headers,
                )

                # 401: force token refresh and retry once
                if response.status_code == 401 and attempt == 0:
                    await self._token_manager.force_refresh(self.client)
                    continue

                # Retryable server errors
                if response.status_code in _RETRYABLE_STATUS and attempt < self._max_retries:
                    await asyncio.sleep(_BACKOFF_SCHEDULE[min(attempt, len(_BACKOFF_SCHEDULE) - 1)])
                    continue

                raise_for_status(response)
                return response

            except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.PoolTimeout) as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    await asyncio.sleep(_BACKOFF_SCHEDULE[min(attempt, len(_BACKOFF_SCHEDULE) - 1)])
                    continue
                raise ConnectionError(f"Connection failed after {self._max_retries + 1} attempts: {exc}") from exc

            except AuthError:
                raise

        # Should not reach here, but just in case
        if last_exc is not None:
            raise ConnectionError(str(last_exc)) from last_exc
        raise RuntimeError("Unexpected retry loop exit")

    async def request_raw(
        self,
        method: str,
        url: str,
        *,
        content: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Make an unauthenticated request to an arbitrary URL (e.g., presigned MinIO upload).

        Uses a separate httpx client without base_url since the target URL
        is typically a presigned MinIO URL on a different host.
        """
        if self._raw_client is None:
            self._raw_client = httpx.AsyncClient(timeout=self._timeout)
        response = await self._raw_client.request(
            method,
            url,
            content=content,
            headers=headers or {},
        )
        if not response.is_success:
            raise_for_status(response)
        return response
