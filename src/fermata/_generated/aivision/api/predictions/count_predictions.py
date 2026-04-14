from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_prediction_count import ModelsPredictionCount
from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    *,
    cycle_id: UUID,
    classes: list[str] | Unset = UNSET,
    photo_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    include_hidden: bool | Unset = UNSET,
    include_empty: bool | Unset = UNSET,
    ignore_threshold: bool | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_cycle_id = str(cycle_id)
    params["cycleId"] = json_cycle_id

    json_classes: list[str] | Unset = UNSET
    if not isinstance(classes, Unset):
        json_classes = classes


    params["classes"] = json_classes

    json_photo_id: str | Unset = UNSET
    if not isinstance(photo_id, Unset):
        json_photo_id = str(photo_id)
    params["photoId"] = json_photo_id

    json_pipeline_id: str | Unset = UNSET
    if not isinstance(pipeline_id, Unset):
        json_pipeline_id = str(pipeline_id)
    params["pipelineId"] = json_pipeline_id

    params["includeHidden"] = include_hidden

    params["includeEmpty"] = include_empty

    params["ignoreThreshold"] = ignore_threshold

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


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/predictions/count",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CommonErrorsApiError | ModelsPredictionCount | None:
    if response.status_code == 200:
        response_200 = ModelsPredictionCount.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CommonErrorsApiError | ModelsPredictionCount]:
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
    photo_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    include_hidden: bool | Unset = UNSET,
    include_empty: bool | Unset = UNSET,
    ignore_threshold: bool | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> Response[CommonErrorsApiError | ModelsPredictionCount]:
    """  Count predictions matching filters

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        photo_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        include_hidden (bool | Unset):
        include_empty (bool | Unset):
        ignore_threshold (bool | Unset):
        captured_from (datetime.datetime | Unset):
        captured_to (datetime.datetime | Unset):
        from_ (datetime.datetime):
        to (datetime.datetime):
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsPredictionCount]
     """


    kwargs = _get_kwargs(
        cycle_id=cycle_id,
classes=classes,
photo_id=photo_id,
pipeline_id=pipeline_id,
include_hidden=include_hidden,
include_empty=include_empty,
ignore_threshold=ignore_threshold,
captured_from=captured_from,
captured_to=captured_to,
from_=from_,
to=to,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,

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
    photo_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    include_hidden: bool | Unset = UNSET,
    include_empty: bool | Unset = UNSET,
    ignore_threshold: bool | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> CommonErrorsApiError | ModelsPredictionCount | None:
    """  Count predictions matching filters

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        photo_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        include_hidden (bool | Unset):
        include_empty (bool | Unset):
        ignore_threshold (bool | Unset):
        captured_from (datetime.datetime | Unset):
        captured_to (datetime.datetime | Unset):
        from_ (datetime.datetime):
        to (datetime.datetime):
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsPredictionCount
     """


    return sync_detailed(
        client=client,
cycle_id=cycle_id,
classes=classes,
photo_id=photo_id,
pipeline_id=pipeline_id,
include_hidden=include_hidden,
include_empty=include_empty,
ignore_threshold=ignore_threshold,
captured_from=captured_from,
captured_to=captured_to,
from_=from_,
to=to,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    cycle_id: UUID,
    classes: list[str] | Unset = UNSET,
    photo_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    include_hidden: bool | Unset = UNSET,
    include_empty: bool | Unset = UNSET,
    ignore_threshold: bool | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> Response[CommonErrorsApiError | ModelsPredictionCount]:
    """  Count predictions matching filters

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        photo_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        include_hidden (bool | Unset):
        include_empty (bool | Unset):
        ignore_threshold (bool | Unset):
        captured_from (datetime.datetime | Unset):
        captured_to (datetime.datetime | Unset):
        from_ (datetime.datetime):
        to (datetime.datetime):
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsPredictionCount]
     """


    kwargs = _get_kwargs(
        cycle_id=cycle_id,
classes=classes,
photo_id=photo_id,
pipeline_id=pipeline_id,
include_hidden=include_hidden,
include_empty=include_empty,
ignore_threshold=ignore_threshold,
captured_from=captured_from,
captured_to=captured_to,
from_=from_,
to=to,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    cycle_id: UUID,
    classes: list[str] | Unset = UNSET,
    photo_id: UUID | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    include_hidden: bool | Unset = UNSET,
    include_empty: bool | Unset = UNSET,
    ignore_threshold: bool | Unset = UNSET,
    captured_from: datetime.datetime | Unset = UNSET,
    captured_to: datetime.datetime | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> CommonErrorsApiError | ModelsPredictionCount | None:
    """  Count predictions matching filters

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        photo_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        include_hidden (bool | Unset):
        include_empty (bool | Unset):
        ignore_threshold (bool | Unset):
        captured_from (datetime.datetime | Unset):
        captured_to (datetime.datetime | Unset):
        from_ (datetime.datetime):
        to (datetime.datetime):
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsPredictionCount
     """


    return (await asyncio_detailed(
        client=client,
cycle_id=cycle_id,
classes=classes,
photo_id=photo_id,
pipeline_id=pipeline_id,
include_hidden=include_hidden,
include_empty=include_empty,
ignore_threshold=ignore_threshold,
captured_from=captured_from,
captured_to=captured_to,
from_=from_,
to=to,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,

    )).parsed
