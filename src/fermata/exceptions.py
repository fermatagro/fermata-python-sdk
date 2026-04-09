from __future__ import annotations

import httpx


class FermataError(Exception):
    """Base exception for all Fermata SDK errors."""

    def __init__(self, message: str, *, status_code: int | None = None, request_id: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id


class AuthError(FermataError):
    """Authentication failed (401 or token exchange failure)."""


class NotFoundError(FermataError):
    """Resource not found (404)."""


class ConflictError(FermataError):
    """Resource conflict (409)."""


class ValidationError(FermataError):
    """Invalid request (400/422)."""


class ServerError(FermataError):
    """Server error (500+)."""


class ConnectionError(FermataError):  # noqa: A001
    """Network unreachable, timeout, or DNS failure."""


_STATUS_MAP: dict[int, type[FermataError]] = {
    400: ValidationError,
    401: AuthError,
    403: AuthError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
}


def raise_for_status(response: httpx.Response) -> None:
    """Raise a typed FermataError for non-2xx responses."""
    if response.is_success:
        return

    request_id: str | None = response.headers.get("x-request-id")
    message = f"HTTP {response.status_code}"

    try:
        body = response.json()
        if isinstance(body, dict) and "message" in body:
            message = body["message"]
    except Exception:
        if response.text:
            message = response.text[:200]

    exc_class = _STATUS_MAP.get(response.status_code)
    if exc_class is None:
        exc_class = ServerError if response.status_code >= 500 else FermataError

    raise exc_class(message, status_code=response.status_code, request_id=request_id)
