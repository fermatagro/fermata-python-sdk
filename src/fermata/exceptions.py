from __future__ import annotations

import logging
import os
import typing

import httpx

_logger = logging.getLogger("fermata")


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


def _build_connection_error(exc: httpx.RequestError) -> ConnectionError:
    """Build a ConnectionError with a clear message from an httpx transport exception."""
    request = getattr(exc, "request", None)
    url = getattr(request, "url", None)
    target = str(url) if url is not None else "Fermata"

    if isinstance(exc, httpx.ConnectTimeout):
        detail = "connection timed out"
    elif isinstance(exc, httpx.ConnectError):
        detail = "connection refused or host unreachable"
    elif isinstance(exc, httpx.ReadTimeout):
        detail = "no response (read timeout)"
    elif isinstance(exc, httpx.WriteTimeout):
        detail = "write timed out"
    elif isinstance(exc, httpx.TimeoutException):
        detail = f"timeout ({type(exc).__name__})"
    else:
        detail = type(exc).__name__

    return ConnectionError(f"Cannot reach {target}: {detail}")


def _reraise_as_connection_error(exc: httpx.RequestError) -> typing.NoReturn:
    """Re-raise an httpx transport exception as a ConnectionError.

    Default: suppresses the chained httpcore→httpx traceback for clean output.
    The original is still reachable via the new exception's ``__context__``.
    Set ``FERMATA_DEBUG=1`` to expose the full chain (``raise ... from exc``).
    The original is always logged at DEBUG on the ``fermata`` logger.
    """
    _logger.debug("httpx transport error: %r", exc, exc_info=exc)
    new_exc = _build_connection_error(exc)
    if os.environ.get("FERMATA_DEBUG", "").lower() in ("1", "true", "yes"):
        raise new_exc from exc
    raise new_exc from None


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
