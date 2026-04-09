from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...types import Response


def _get_kwargs(
    org_id: str,
    media_type: str,
    year: int,
    month: int,
    day: int,
    media_id: UUID,
    thumb_code: str,
    thumb_ext: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cloudfront/{org_id}/thumb/{media_type}/{year}/{month}/{day}/{media_id}/{thumb_code}.{thumb_ext}".format(
            org_id=quote(str(org_id), safe=""),
            media_type=quote(str(media_type), safe=""),
            year=quote(str(year), safe=""),
            month=quote(str(month), safe=""),
            day=quote(str(day), safe=""),
            media_id=quote(str(media_id), safe=""),
            thumb_code=quote(str(thumb_code), safe=""),
            thumb_ext=quote(str(thumb_ext), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | CommonErrorsApiError | None:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200

    if response.status_code == 401:
        response_401 = CommonErrorsApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CommonErrorsApiError.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = CommonErrorsApiError.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = CommonErrorsApiError.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | CommonErrorsApiError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    media_type: str,
    year: int,
    month: int,
    day: int,
    media_id: UUID,
    thumb_code: str,
    thumb_ext: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | CommonErrorsApiError]:
    """Get dynamic thumbnail ThumbCode format: w{width}h{height}dpr{dpr}q{quality}, e.g.,
    w320h180dpr2q75.jpeg

    Args:
        org_id (str): Organization identifier (opaque string)
        media_type (str):
        year (int):
        month (int):
        day (int):
        media_id (UUID): UUID identifier
        thumb_code (str): Dynamic thumbnail specification code. Format:
            w{width}h{height}dpr{dpr}q{quality}, e.g., w320h180dpr2q75
        thumb_ext (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        media_type=media_type,
        year=year,
        month=month,
        day=day,
        media_id=media_id,
        thumb_code=thumb_code,
        thumb_ext=thumb_ext,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    media_type: str,
    year: int,
    month: int,
    day: int,
    media_id: UUID,
    thumb_code: str,
    thumb_ext: str,
    *,
    client: AuthenticatedClient,
) -> Any | CommonErrorsApiError | None:
    """Get dynamic thumbnail ThumbCode format: w{width}h{height}dpr{dpr}q{quality}, e.g.,
    w320h180dpr2q75.jpeg

    Args:
        org_id (str): Organization identifier (opaque string)
        media_type (str):
        year (int):
        month (int):
        day (int):
        media_id (UUID): UUID identifier
        thumb_code (str): Dynamic thumbnail specification code. Format:
            w{width}h{height}dpr{dpr}q{quality}, e.g., w320h180dpr2q75
        thumb_ext (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
    """

    return sync_detailed(
        org_id=org_id,
        media_type=media_type,
        year=year,
        month=month,
        day=day,
        media_id=media_id,
        thumb_code=thumb_code,
        thumb_ext=thumb_ext,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    media_type: str,
    year: int,
    month: int,
    day: int,
    media_id: UUID,
    thumb_code: str,
    thumb_ext: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | CommonErrorsApiError]:
    """Get dynamic thumbnail ThumbCode format: w{width}h{height}dpr{dpr}q{quality}, e.g.,
    w320h180dpr2q75.jpeg

    Args:
        org_id (str): Organization identifier (opaque string)
        media_type (str):
        year (int):
        month (int):
        day (int):
        media_id (UUID): UUID identifier
        thumb_code (str): Dynamic thumbnail specification code. Format:
            w{width}h{height}dpr{dpr}q{quality}, e.g., w320h180dpr2q75
        thumb_ext (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        media_type=media_type,
        year=year,
        month=month,
        day=day,
        media_id=media_id,
        thumb_code=thumb_code,
        thumb_ext=thumb_ext,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    media_type: str,
    year: int,
    month: int,
    day: int,
    media_id: UUID,
    thumb_code: str,
    thumb_ext: str,
    *,
    client: AuthenticatedClient,
) -> Any | CommonErrorsApiError | None:
    """Get dynamic thumbnail ThumbCode format: w{width}h{height}dpr{dpr}q{quality}, e.g.,
    w320h180dpr2q75.jpeg

    Args:
        org_id (str): Organization identifier (opaque string)
        media_type (str):
        year (int):
        month (int):
        day (int):
        media_id (UUID): UUID identifier
        thumb_code (str): Dynamic thumbnail specification code. Format:
            w{width}h{height}dpr{dpr}q{quality}, e.g., w320h180dpr2q75
        thumb_ext (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            media_type=media_type,
            year=year,
            month=month,
            day=day,
            media_id=media_id,
            thumb_code=thumb_code,
            thumb_ext=thumb_ext,
            client=client,
        )
    ).parsed
