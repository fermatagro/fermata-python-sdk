from __future__ import annotations

import base64
import json
import time

import httpx

from fermata.exceptions import AuthError


def _extract_org_id(token: str) -> str | None:
    """Extract organization_id from JWT payload without verification."""
    try:
        payload = token.split(".")[1]
        payload += "=" * (4 - len(payload) % 4)
        claims = json.loads(base64.b64decode(payload))
        return claims.get("organization_id")
    except Exception:
        return None


class TokenManager:
    """Manages auth token lifecycle for SDK -> Hera communication.

    Self-contained: owns its own httpx clients for token exchange.
    Supports both async and sync usage.
    """

    def __init__(self, base_url: str, username: str, password: str) -> None:
        self._base_url = base_url
        self._username = username
        self._password = password
        self._token: str | None = None
        self._org_id: str | None = None
        self._expires_at: float = 0.0
        self._async_client: httpx.AsyncClient | None = None
        self._sync_client: httpx.Client | None = None

    @property
    def org_id(self) -> str | None:
        """Organization ID extracted from the JWT token."""
        return self._org_id

    # --- Lifecycle ---

    async def open(self) -> None:
        self._async_client = httpx.AsyncClient()

    async def close(self) -> None:
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None

    def open_sync(self) -> None:
        self._sync_client = httpx.Client()

    def close_sync(self) -> None:
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None

    # --- Async ---

    async def get_token(self) -> str:
        """Return a valid token, refreshing if within 60s of expiry."""
        if self._token is None or time.monotonic() > self._expires_at - 60:
            await self._refresh_async()
        assert self._token is not None
        return self._token

    async def force_refresh(self) -> None:
        """Force token refresh (e.g., after 401)."""
        await self._refresh_async()

    async def _refresh_async(self) -> None:
        assert self._async_client is not None, "Call open() before using async methods"
        try:
            response = await self._async_client.post(
                f"{self._base_url}/auth/token",
                data={"client_id": self._username, "client_secret": self._password},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        except httpx.HTTPError as exc:
            raise AuthError(f"Token exchange failed: {exc}") from exc
        self._parse_token_response(response)

    # --- Sync ---

    def get_token_sync(self) -> str:
        """Return a valid token, refreshing if within 60s of expiry."""
        if self._token is None or time.monotonic() > self._expires_at - 60:
            self._refresh_sync()
        assert self._token is not None
        return self._token

    def force_refresh_sync(self) -> None:
        """Force token refresh (e.g., after 401)."""
        self._refresh_sync()

    def _refresh_sync(self) -> None:
        assert self._sync_client is not None, "Call open_sync() before using sync methods"
        try:
            response = self._sync_client.post(
                f"{self._base_url}/auth/token",
                data={"client_id": self._username, "client_secret": self._password},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        except httpx.HTTPError as exc:
            raise AuthError(f"Token exchange failed: {exc}") from exc
        self._parse_token_response(response)

    # --- Shared ---

    def _parse_token_response(self, response: httpx.Response) -> None:
        if not response.is_success:
            raise AuthError(
                f"Token exchange failed: HTTP {response.status_code}",
                status_code=response.status_code,
            )
        body = response.json()
        self._token = body["access_token"]
        if self._token is None:
            raise AuthError("Token exchange failed: no access_token in response")
        self._org_id = _extract_org_id(self._token)
        expires_in = body.get("expires_in", 3600)
        self._expires_at = time.monotonic() + expires_in
