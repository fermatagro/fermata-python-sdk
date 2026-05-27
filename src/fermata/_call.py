"""Unwrap generated API responses into typed results or exceptions."""

from __future__ import annotations

from collections.abc import Awaitable
from typing import Any

import httpx

from fermata.exceptions import (
    AuthError,
    ConflictError,
    FermataError,
    NotFoundError,
    ServerError,
    ValidationError,
    _reraise_as_connection_error,
)

_STATUS_MAP: dict[int, type[FermataError]] = {
    400: ValidationError,
    401: AuthError,
    403: AuthError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
}

def _unwrap(resp: Any) -> Any:
    """Extract success result from a generated Response, raising on errors.

    Generated ``*_detailed`` functions return ``Response`` with:
    - ``.status_code`` — ``HTTPStatus`` enum
    - ``.parsed`` — success model or ``CommonErrorsApiError`` or ``None``
    """
    status = resp.status_code.value
    if 200 <= status < 300:
        return resp.parsed

    # Try parsed error model first, fall back to raw response body
    parsed = resp.parsed
    message = f"HTTP {status}"
    request_id: str | None = None
    if hasattr(parsed, "message"):
        message = parsed.message
        request_id = getattr(parsed, "request_id", None)
    elif resp.content:
        try:
            import json
            body = json.loads(resp.content)
            message = body.get("message", message)
            request_id = body.get("request_id")
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    exc_class = _STATUS_MAP.get(status, ServerError if status >= 500 else FermataError)
    raise exc_class(message, status_code=status, request_id=request_id)


async def call_async(coro: Awaitable[Any]) -> Any:
    """Await a generated ``asyncio_detailed`` call and unwrap the response."""
    try:
        resp = await coro
    except httpx.RequestError as exc:
        _reraise_as_connection_error(exc)
    return _unwrap(resp)
