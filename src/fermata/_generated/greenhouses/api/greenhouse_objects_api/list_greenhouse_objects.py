from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_greenhouse_objects_response_200 import ListGreenhouseObjectsResponse200
from ...models.models_greenhouse_object_type import ModelsGreenhouseObjectType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    greenhouse_id: UUID,
    *,
    kind: ModelsGreenhouseObjectType | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_kind: str | Unset = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value

    params["kind"] = json_kind

    params["xmin"] = xmin

    params["ymin"] = ymin

    params["xmax"] = xmax

    params["ymax"] = ymax

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/greenhouses/{greenhouse_id}/objects".format(
            greenhouse_id=quote(str(greenhouse_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ListGreenhouseObjectsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListGreenhouseObjectsResponse200.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ListGreenhouseObjectsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    greenhouse_id: UUID,
    *,
    client: AuthenticatedClient,
    kind: ModelsGreenhouseObjectType | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListGreenhouseObjectsResponse200]:
    """List all greenhouse objects, optionally only those of one kind and/or overlapping a grid rect

    Args:
        greenhouse_id (UUID): UUID identifier
        kind (ModelsGreenhouseObjectType | Unset): Type of object within a greenhouse
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
        Response[CommonErrorsApiError | ListGreenhouseObjectsResponse200]
    """

    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
        kind=kind,
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
    greenhouse_id: UUID,
    *,
    client: AuthenticatedClient,
    kind: ModelsGreenhouseObjectType | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListGreenhouseObjectsResponse200 | None:
    """List all greenhouse objects, optionally only those of one kind and/or overlapping a grid rect

    Args:
        greenhouse_id (UUID): UUID identifier
        kind (ModelsGreenhouseObjectType | Unset): Type of object within a greenhouse
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
        CommonErrorsApiError | ListGreenhouseObjectsResponse200
    """

    return sync_detailed(
        greenhouse_id=greenhouse_id,
        client=client,
        kind=kind,
        xmin=xmin,
        ymin=ymin,
        xmax=xmax,
        ymax=ymax,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    greenhouse_id: UUID,
    *,
    client: AuthenticatedClient,
    kind: ModelsGreenhouseObjectType | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListGreenhouseObjectsResponse200]:
    """List all greenhouse objects, optionally only those of one kind and/or overlapping a grid rect

    Args:
        greenhouse_id (UUID): UUID identifier
        kind (ModelsGreenhouseObjectType | Unset): Type of object within a greenhouse
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
        Response[CommonErrorsApiError | ListGreenhouseObjectsResponse200]
    """

    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
        kind=kind,
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
    greenhouse_id: UUID,
    *,
    client: AuthenticatedClient,
    kind: ModelsGreenhouseObjectType | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListGreenhouseObjectsResponse200 | None:
    """List all greenhouse objects, optionally only those of one kind and/or overlapping a grid rect

    Args:
        greenhouse_id (UUID): UUID identifier
        kind (ModelsGreenhouseObjectType | Unset): Type of object within a greenhouse
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
        CommonErrorsApiError | ListGreenhouseObjectsResponse200
    """

    return (
        await asyncio_detailed(
            greenhouse_id=greenhouse_id,
            client=client,
            kind=kind,
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
