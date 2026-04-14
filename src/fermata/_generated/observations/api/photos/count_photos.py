from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_photo_count import ModelsPhotoCount
from ...models.models_photo_source import ModelsPhotoSource
from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    *,
    from_: datetime.datetime,
    to: datetime.datetime,
    growing_cycle_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    zone_object_id: UUID | Unset = UNSET,
    source: ModelsPhotoSource | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    hmin: float | Unset = UNSET,
    hmax: float | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    json_growing_cycle_id: str | Unset = UNSET
    if not isinstance(growing_cycle_id, Unset):
        json_growing_cycle_id = str(growing_cycle_id)
    params["growingCycleId"] = json_growing_cycle_id

    json_greenhouse_id: str | Unset = UNSET
    if not isinstance(greenhouse_id, Unset):
        json_greenhouse_id = str(greenhouse_id)
    params["greenhouseId"] = json_greenhouse_id

    json_device_id: str | Unset = UNSET
    if not isinstance(device_id, Unset):
        json_device_id = str(device_id)
    params["deviceId"] = json_device_id

    json_zone_object_id: str | Unset = UNSET
    if not isinstance(zone_object_id, Unset):
        json_zone_object_id = str(zone_object_id)
    params["zoneObjectId"] = json_zone_object_id

    json_source: str | Unset = UNSET
    if not isinstance(source, Unset):
        json_source = source.value

    params["source"] = json_source

    json_pipeline_id: str | Unset = UNSET
    if not isinstance(pipeline_id, Unset):
        json_pipeline_id = str(pipeline_id)
    params["pipelineId"] = json_pipeline_id

    params["xmin"] = xmin

    params["ymin"] = ymin

    params["xmax"] = xmax

    params["ymax"] = ymax

    params["hmin"] = hmin

    params["hmax"] = hmax


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/photos/count",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CommonErrorsApiError | ModelsPhotoCount | None:
    if response.status_code == 200:
        response_200 = ModelsPhotoCount.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CommonErrorsApiError | ModelsPhotoCount]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime,
    to: datetime.datetime,
    growing_cycle_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    zone_object_id: UUID | Unset = UNSET,
    source: ModelsPhotoSource | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    hmin: float | Unset = UNSET,
    hmax: float | Unset = UNSET,

) -> Response[CommonErrorsApiError | ModelsPhotoCount]:
    """  Count photos matching filters

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        growing_cycle_id (UUID | Unset): UUID identifier
        greenhouse_id (UUID | Unset): UUID identifier
        device_id (UUID | Unset): UUID identifier
        zone_object_id (UUID | Unset): UUID identifier
        source (ModelsPhotoSource | Unset): Source of the photo capture
        pipeline_id (UUID | Unset): UUID identifier
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):
        hmin (float | Unset):
        hmax (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsPhotoCount]
     """


    kwargs = _get_kwargs(
        from_=from_,
to=to,
growing_cycle_id=growing_cycle_id,
greenhouse_id=greenhouse_id,
device_id=device_id,
zone_object_id=zone_object_id,
source=source,
pipeline_id=pipeline_id,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,
hmin=hmin,
hmax=hmax,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime,
    to: datetime.datetime,
    growing_cycle_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    zone_object_id: UUID | Unset = UNSET,
    source: ModelsPhotoSource | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    hmin: float | Unset = UNSET,
    hmax: float | Unset = UNSET,

) -> CommonErrorsApiError | ModelsPhotoCount | None:
    """  Count photos matching filters

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        growing_cycle_id (UUID | Unset): UUID identifier
        greenhouse_id (UUID | Unset): UUID identifier
        device_id (UUID | Unset): UUID identifier
        zone_object_id (UUID | Unset): UUID identifier
        source (ModelsPhotoSource | Unset): Source of the photo capture
        pipeline_id (UUID | Unset): UUID identifier
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):
        hmin (float | Unset):
        hmax (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsPhotoCount
     """


    return sync_detailed(
        client=client,
from_=from_,
to=to,
growing_cycle_id=growing_cycle_id,
greenhouse_id=greenhouse_id,
device_id=device_id,
zone_object_id=zone_object_id,
source=source,
pipeline_id=pipeline_id,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,
hmin=hmin,
hmax=hmax,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime,
    to: datetime.datetime,
    growing_cycle_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    zone_object_id: UUID | Unset = UNSET,
    source: ModelsPhotoSource | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    hmin: float | Unset = UNSET,
    hmax: float | Unset = UNSET,

) -> Response[CommonErrorsApiError | ModelsPhotoCount]:
    """  Count photos matching filters

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        growing_cycle_id (UUID | Unset): UUID identifier
        greenhouse_id (UUID | Unset): UUID identifier
        device_id (UUID | Unset): UUID identifier
        zone_object_id (UUID | Unset): UUID identifier
        source (ModelsPhotoSource | Unset): Source of the photo capture
        pipeline_id (UUID | Unset): UUID identifier
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):
        hmin (float | Unset):
        hmax (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsPhotoCount]
     """


    kwargs = _get_kwargs(
        from_=from_,
to=to,
growing_cycle_id=growing_cycle_id,
greenhouse_id=greenhouse_id,
device_id=device_id,
zone_object_id=zone_object_id,
source=source,
pipeline_id=pipeline_id,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,
hmin=hmin,
hmax=hmax,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime,
    to: datetime.datetime,
    growing_cycle_id: UUID | Unset = UNSET,
    greenhouse_id: UUID | Unset = UNSET,
    device_id: UUID | Unset = UNSET,
    zone_object_id: UUID | Unset = UNSET,
    source: ModelsPhotoSource | Unset = UNSET,
    pipeline_id: UUID | Unset = UNSET,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,
    hmin: float | Unset = UNSET,
    hmax: float | Unset = UNSET,

) -> CommonErrorsApiError | ModelsPhotoCount | None:
    """  Count photos matching filters

    Args:
        from_ (datetime.datetime):
        to (datetime.datetime):
        growing_cycle_id (UUID | Unset): UUID identifier
        greenhouse_id (UUID | Unset): UUID identifier
        device_id (UUID | Unset): UUID identifier
        zone_object_id (UUID | Unset): UUID identifier
        source (ModelsPhotoSource | Unset): Source of the photo capture
        pipeline_id (UUID | Unset): UUID identifier
        xmin (float | Unset):
        ymin (float | Unset):
        xmax (float | Unset):
        ymax (float | Unset):
        hmin (float | Unset):
        hmax (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsPhotoCount
     """


    return (await asyncio_detailed(
        client=client,
from_=from_,
to=to,
growing_cycle_id=growing_cycle_id,
greenhouse_id=greenhouse_id,
device_id=device_id,
zone_object_id=zone_object_id,
source=source,
pipeline_id=pipeline_id,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,
hmin=hmin,
hmax=hmax,

    )).parsed
