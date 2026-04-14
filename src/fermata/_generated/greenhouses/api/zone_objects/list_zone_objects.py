from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_zone_objects_response_200 import ListZoneObjectsResponse200
from ...models.models_zone_object_status import ModelsZoneObjectStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    device_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    status: ModelsZoneObjectStatus | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_device_id: str | Unset = UNSET
    if not isinstance(device_id, Unset):
        json_device_id = str(device_id)
    params["deviceId"] = json_device_id

    json_greenhouse_id: str | Unset = UNSET
    if not isinstance(greenhouse_id, Unset):
        json_greenhouse_id = str(greenhouse_id)
    params["greenhouseId"] = json_greenhouse_id

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["xmin"] = xmin

    params["ymin"] = ymin

    params["xmax"] = xmax

    params["ymax"] = ymax

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/zone-objects",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ListZoneObjectsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListZoneObjectsResponse200.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ListZoneObjectsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    device_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    status: ModelsZoneObjectStatus | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListZoneObjectsResponse200]:
    """List zone objects

    Args:
        device_id (UUID | Unset): UUID identifier
        greenhouse_id (UUID | Unset): UUID identifier
        status (ModelsZoneObjectStatus | Unset): Status of a zone object
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListZoneObjectsResponse200]
    """

    kwargs = _get_kwargs(
        device_id=device_id,
        greenhouse_id=greenhouse_id,
        status=status,
        xmin=xmin,
        ymin=ymin,
        xmax=xmax,
        ymax=ymax,
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
    device_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    status: ModelsZoneObjectStatus | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListZoneObjectsResponse200 | None:
    """List zone objects

    Args:
        device_id (UUID | Unset): UUID identifier
        greenhouse_id (UUID | Unset): UUID identifier
        status (ModelsZoneObjectStatus | Unset): Status of a zone object
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListZoneObjectsResponse200
    """

    return sync_detailed(
        client=client,
        device_id=device_id,
        greenhouse_id=greenhouse_id,
        status=status,
        xmin=xmin,
        ymin=ymin,
        xmax=xmax,
        ymax=ymax,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    device_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    status: ModelsZoneObjectStatus | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListZoneObjectsResponse200]:
    """List zone objects

    Args:
        device_id (UUID | Unset): UUID identifier
        greenhouse_id (UUID | Unset): UUID identifier
        status (ModelsZoneObjectStatus | Unset): Status of a zone object
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListZoneObjectsResponse200]
    """

    kwargs = _get_kwargs(
        device_id=device_id,
        greenhouse_id=greenhouse_id,
        status=status,
        xmin=xmin,
        ymin=ymin,
        xmax=xmax,
        ymax=ymax,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    device_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    status: ModelsZoneObjectStatus | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListZoneObjectsResponse200 | None:
    """List zone objects

    Args:
        device_id (UUID | Unset): UUID identifier
        greenhouse_id (UUID | Unset): UUID identifier
        status (ModelsZoneObjectStatus | Unset): Status of a zone object
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListZoneObjectsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            device_id=device_id,
            greenhouse_id=greenhouse_id,
            status=status,
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
