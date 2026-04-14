import datetime
from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_predictions_for_gallery_response_200 import ListPredictionsForGalleryResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cycle_id: UUID,
    classes: list[str] | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_cycle_id = str(cycle_id)
    params["cycleId"] = json_cycle_id

    json_classes: list[str] | Unset = UNSET
    if not isinstance(classes, Unset):
        json_classes = classes

    params["classes"] = json_classes

    json_pipeline_id: str | Unset = UNSET
    if not isinstance(pipeline_id, Unset):
        json_pipeline_id = str(pipeline_id)
    params["pipelineId"] = json_pipeline_id

    json_captured_from: str | Unset = UNSET
    if not isinstance(captured_from, Unset):
        json_captured_from = captured_from.isoformat()
    params["capturedFrom"] = json_captured_from

    json_captured_to: str | Unset = UNSET
    if not isinstance(captured_to, Unset):
        json_captured_to = captured_to.isoformat()
    params["capturedTo"] = json_captured_to

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    params["xmin"] = xmin

    params["ymin"] = ymin

    params["xmax"] = xmax

    params["ymax"] = ymax

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/predictions/gallery",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ListPredictionsForGalleryResponse200 | None:
    if response.status_code == 200:
        response_200 = ListPredictionsForGalleryResponse200.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ListPredictionsForGalleryResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    cycle_id: UUID,
    classes: list[str] | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListPredictionsForGalleryResponse200]:
    """Query predictions with filters for gallery view

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        pipeline_id (UUID | Unset): UUID identifier
        captured_from (datetime.datetime | Unset):
        captured_to (datetime.datetime | Unset):
        from_ (datetime.datetime):
        to (datetime.datetime):
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
        Response[CommonErrorsApiError | ListPredictionsForGalleryResponse200]
    """

    kwargs = _get_kwargs(
        cycle_id=cycle_id,
        classes=classes,
        pipeline_id=pipeline_id,
        captured_from=captured_from,
        captured_to=captured_to,
        from_=from_,
        to=to,
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
    cycle_id: UUID,
    classes: list[str] | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListPredictionsForGalleryResponse200 | None:
    """Query predictions with filters for gallery view

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        pipeline_id (UUID | Unset): UUID identifier
        captured_from (datetime.datetime | Unset):
        captured_to (datetime.datetime | Unset):
        from_ (datetime.datetime):
        to (datetime.datetime):
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
        CommonErrorsApiError | ListPredictionsForGalleryResponse200
    """

    return sync_detailed(
        client=client,
        cycle_id=cycle_id,
        classes=classes,
        pipeline_id=pipeline_id,
        captured_from=captured_from,
        captured_to=captured_to,
        from_=from_,
        to=to,
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
    cycle_id: UUID,
    classes: list[str] | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListPredictionsForGalleryResponse200]:
    """Query predictions with filters for gallery view

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        pipeline_id (UUID | Unset): UUID identifier
        captured_from (datetime.datetime | Unset):
        captured_to (datetime.datetime | Unset):
        from_ (datetime.datetime):
        to (datetime.datetime):
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
        Response[CommonErrorsApiError | ListPredictionsForGalleryResponse200]
    """

    kwargs = _get_kwargs(
        cycle_id=cycle_id,
        classes=classes,
        pipeline_id=pipeline_id,
        captured_from=captured_from,
        captured_to=captured_to,
        from_=from_,
        to=to,
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
    cycle_id: UUID,
    classes: list[str] | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListPredictionsForGalleryResponse200 | None:
    """Query predictions with filters for gallery view

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        pipeline_id (UUID | Unset): UUID identifier
        captured_from (datetime.datetime | Unset):
        captured_to (datetime.datetime | Unset):
        from_ (datetime.datetime):
        to (datetime.datetime):
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
        CommonErrorsApiError | ListPredictionsForGalleryResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            cycle_id=cycle_id,
            classes=classes,
            pipeline_id=pipeline_id,
            captured_from=captured_from,
            captured_to=captured_to,
            from_=from_,
            to=to,
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
