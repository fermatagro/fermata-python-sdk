"""Unwrap generated API responses into typed results or exceptions."""

from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, TypeVar

from fermata.exceptions import (
    AuthError,
    ConflictError,
    FermataError,
    NotFoundError,
    ServerError,
    ValidationError,
)

_STATUS_MAP: dict[int, type[FermataError]] = {
    400: ValidationError,
    401: AuthError,
    403: AuthError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
}

T = TypeVar("T")


def _unwrap(resp: Any) -> Any:
    """Extract success result from a generated Response, raising on errors.

    Generated ``*_detailed`` functions return ``Response`` with:
    - ``.status_code`` — ``HTTPStatus`` enum
    - ``.parsed`` — success model or ``CommonErrorsApiError`` or ``None``
    """
    status = resp.status_code.value
    if 200 <= status < 300:
        return resp.parsed

    parsed = resp.parsed
    message = parsed.message if hasattr(parsed, "message") else f"HTTP {status}"
    request_id = parsed.request_id if hasattr(parsed, "request_id") else None
    exc_class = _STATUS_MAP.get(status, ServerError if status >= 500 else FermataError)
    raise exc_class(message, status_code=status, request_id=request_id)


async def call_async(coro: Awaitable[Any]) -> Any:
    """Await a generated ``asyncio_detailed`` call and unwrap the response."""
    return _unwrap(await coro)


def call_sync(resp: Any) -> Any:
    """Unwrap a generated ``sync_detailed`` response."""
    return _unwrap(resp)
