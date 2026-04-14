from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_cycle_regions_response_200 import ListCycleRegionsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    cycle_id: UUID,
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/cycles/{cycle_id}/regions".format(
            cycle_id=quote(str(cycle_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ListCycleRegionsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListCycleRegionsResponse200.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ListCycleRegionsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    cycle_id: UUID,
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListCycleRegionsResponse200]:
    """List all regions in a growing cycle

    Args:
        cycle_id (UUID): UUID identifier
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListCycleRegionsResponse200]
    """

    kwargs = _get_kwargs(
        cycle_id=cycle_id,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    cycle_id: UUID,
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListCycleRegionsResponse200 | None:
    """List all regions in a growing cycle

    Args:
        cycle_id (UUID): UUID identifier
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListCycleRegionsResponse200
    """

    return sync_detailed(
        cycle_id=cycle_id,
        client=client,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    cycle_id: UUID,
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListCycleRegionsResponse200]:
    """List all regions in a growing cycle

    Args:
        cycle_id (UUID): UUID identifier
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListCycleRegionsResponse200]
    """

    kwargs = _get_kwargs(
        cycle_id=cycle_id,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cycle_id: UUID,
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListCycleRegionsResponse200 | None:
    """List all regions in a growing cycle

    Args:
        cycle_id (UUID): UUID identifier
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListCycleRegionsResponse200
    """

    return (
        await asyncio_detailed(
            cycle_id=cycle_id,
            client=client,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
