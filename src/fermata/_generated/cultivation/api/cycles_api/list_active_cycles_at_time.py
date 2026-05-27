import datetime
from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_active_cycles_at_time_response_200 import ListActiveCyclesAtTimeResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    greenhouse_id: UUID,
    at_time: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_greenhouse_id = str(greenhouse_id)
    params["greenhouseId"] = json_greenhouse_id

    json_at_time = at_time.isoformat()
    params["atTime"] = json_at_time

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/cycles/active",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ListActiveCyclesAtTimeResponse200 | None:
    if response.status_code == 200:
        response_200 = ListActiveCyclesAtTimeResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = CommonErrorsApiError.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = CommonErrorsApiError.from_dict(response.json())

        return response_403

    if response.status_code == 500:
        response_500 = CommonErrorsApiError.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CommonErrorsApiError | ListActiveCyclesAtTimeResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    greenhouse_id: UUID,
    at_time: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListActiveCyclesAtTimeResponse200]:
    """List active growing cycles at a specific time

    Args:
        greenhouse_id (UUID): UUID identifier
        at_time (datetime.datetime):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListActiveCyclesAtTimeResponse200]
    """

    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
        at_time=at_time,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    greenhouse_id: UUID,
    at_time: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListActiveCyclesAtTimeResponse200 | None:
    """List active growing cycles at a specific time

    Args:
        greenhouse_id (UUID): UUID identifier
        at_time (datetime.datetime):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListActiveCyclesAtTimeResponse200
    """

    return sync_detailed(
        client=client,
        greenhouse_id=greenhouse_id,
        at_time=at_time,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    greenhouse_id: UUID,
    at_time: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListActiveCyclesAtTimeResponse200]:
    """List active growing cycles at a specific time

    Args:
        greenhouse_id (UUID): UUID identifier
        at_time (datetime.datetime):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListActiveCyclesAtTimeResponse200]
    """

    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
        at_time=at_time,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    greenhouse_id: UUID,
    at_time: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListActiveCyclesAtTimeResponse200 | None:
    """List active growing cycles at a specific time

    Args:
        greenhouse_id (UUID): UUID identifier
        at_time (datetime.datetime):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListActiveCyclesAtTimeResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            greenhouse_id=greenhouse_id,
            at_time=at_time,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
