import datetime
from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_panoramas_response_200 import ListPanoramasResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    from_: datetime.datetime,
    to: datetime.datetime,
    greenhouse_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    base_x: int | Unset = UNSET,
    base_y: int | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    json_greenhouse_id: str | Unset = UNSET
    if not isinstance(greenhouse_id, Unset):
        json_greenhouse_id = str(greenhouse_id)
    params["greenhouseId"] = json_greenhouse_id

    json_pipeline_id: str | Unset = UNSET
    if not isinstance(pipeline_id, Unset):
        json_pipeline_id = str(pipeline_id)
    params["pipelineId"] = json_pipeline_id

    json_device_id: str | Unset = UNSET
    if not isinstance(device_id, Unset):
        json_device_id = str(device_id)
    params["deviceId"] = json_device_id

    params["baseX"] = base_x

    params["baseY"] = base_y

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/panoramas",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ListPanoramasResponse200 | None:
    if response.status_code == 200:
        response_200 = ListPanoramasResponse200.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ListPanoramasResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    from_: datetime.datetime,
    to: datetime.datetime,
    greenhouse_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    base_x: int | Unset = UNSET,
    base_y: int | Unset = UNSET,
) -> Response[CommonErrorsApiError | ListPanoramasResponse200]:
    """List panoramas with pagination

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.
        from_ (datetime.datetime):
        to (datetime.datetime):
        greenhouse_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        device_id (UUID | Unset): UUID identifier
        base_x (int | Unset):
        base_y (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListPanoramasResponse200]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        greenhouse_id=greenhouse_id,
        pipeline_id=pipeline_id,
        device_id=device_id,
        base_x=base_x,
        base_y=base_y,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    from_: datetime.datetime,
    to: datetime.datetime,
    greenhouse_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    base_x: int | Unset = UNSET,
    base_y: int | Unset = UNSET,
) -> CommonErrorsApiError | ListPanoramasResponse200 | None:
    """List panoramas with pagination

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.
        from_ (datetime.datetime):
        to (datetime.datetime):
        greenhouse_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        device_id (UUID | Unset): UUID identifier
        base_x (int | Unset):
        base_y (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListPanoramasResponse200
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        greenhouse_id=greenhouse_id,
        pipeline_id=pipeline_id,
        device_id=device_id,
        base_x=base_x,
        base_y=base_y,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    from_: datetime.datetime,
    to: datetime.datetime,
    greenhouse_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    base_x: int | Unset = UNSET,
    base_y: int | Unset = UNSET,
) -> Response[CommonErrorsApiError | ListPanoramasResponse200]:
    """List panoramas with pagination

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.
        from_ (datetime.datetime):
        to (datetime.datetime):
        greenhouse_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        device_id (UUID | Unset): UUID identifier
        base_x (int | Unset):
        base_y (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListPanoramasResponse200]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        from_=from_,
        to=to,
        greenhouse_id=greenhouse_id,
        pipeline_id=pipeline_id,
        device_id=device_id,
        base_x=base_x,
        base_y=base_y,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
    from_: datetime.datetime,
    to: datetime.datetime,
    greenhouse_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    base_x: int | Unset = UNSET,
    base_y: int | Unset = UNSET,
) -> CommonErrorsApiError | ListPanoramasResponse200 | None:
    """List panoramas with pagination

    Args:
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.
        from_ (datetime.datetime):
        to (datetime.datetime):
        greenhouse_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        device_id (UUID | Unset): UUID identifier
        base_x (int | Unset):
        base_y (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListPanoramasResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            from_=from_,
            to=to,
            greenhouse_id=greenhouse_id,
            pipeline_id=pipeline_id,
            device_id=device_id,
            base_x=base_x,
            base_y=base_y,
        )
    ).parsed
