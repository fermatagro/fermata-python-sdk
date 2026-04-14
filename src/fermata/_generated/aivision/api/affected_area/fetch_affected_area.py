from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_affected_area import ModelsAffectedArea
from ...models.models_time_bucket import ModelsTimeBucket
from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    cycle_id: UUID,
    *,
    classes: list[str] | Unset = UNSET,
    time_bucket: ModelsTimeBucket,
    ignore_threshold: bool | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_classes: list[str] | Unset = UNSET
    if not isinstance(classes, Unset):
        json_classes = classes


    params["classes"] = json_classes

    json_time_bucket = time_bucket.value
    params["timeBucket"] = json_time_bucket

    params["ignoreThreshold"] = ignore_threshold

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
        "url": "/api/v1/affected-area/{cycle_id}".format(cycle_id=quote(str(cycle_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CommonErrorsApiError | list[ModelsAffectedArea] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = ModelsAffectedArea.from_dict(response_200_item_data)



            response_200.append(response_200_item)

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CommonErrorsApiError | list[ModelsAffectedArea]]:
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
    classes: list[str] | Unset = UNSET,
    time_bucket: ModelsTimeBucket,
    ignore_threshold: bool | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> Response[CommonErrorsApiError | list[ModelsAffectedArea]]:
    """  Fetch affected area

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        time_bucket (ModelsTimeBucket): Aggregation period time
        ignore_threshold (bool | Unset):
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
        Response[CommonErrorsApiError | list[ModelsAffectedArea]]
     """


    kwargs = _get_kwargs(
        cycle_id=cycle_id,
classes=classes,
time_bucket=time_bucket,
ignore_threshold=ignore_threshold,
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
    cycle_id: UUID,
    *,
    client: AuthenticatedClient,
    classes: list[str] | Unset = UNSET,
    time_bucket: ModelsTimeBucket,
    ignore_threshold: bool | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> CommonErrorsApiError | list[ModelsAffectedArea] | None:
    """  Fetch affected area

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        time_bucket (ModelsTimeBucket): Aggregation period time
        ignore_threshold (bool | Unset):
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
        CommonErrorsApiError | list[ModelsAffectedArea]
     """


    return sync_detailed(
        cycle_id=cycle_id,
client=client,
classes=classes,
time_bucket=time_bucket,
ignore_threshold=ignore_threshold,
from_=from_,
to=to,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,

    ).parsed

async def asyncio_detailed(
    cycle_id: UUID,
    *,
    client: AuthenticatedClient,
    classes: list[str] | Unset = UNSET,
    time_bucket: ModelsTimeBucket,
    ignore_threshold: bool | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> Response[CommonErrorsApiError | list[ModelsAffectedArea]]:
    """  Fetch affected area

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        time_bucket (ModelsTimeBucket): Aggregation period time
        ignore_threshold (bool | Unset):
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
        Response[CommonErrorsApiError | list[ModelsAffectedArea]]
     """


    kwargs = _get_kwargs(
        cycle_id=cycle_id,
classes=classes,
time_bucket=time_bucket,
ignore_threshold=ignore_threshold,
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
    cycle_id: UUID,
    *,
    client: AuthenticatedClient,
    classes: list[str] | Unset = UNSET,
    time_bucket: ModelsTimeBucket,
    ignore_threshold: bool | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    xmin: float | Unset = UNSET,
    ymin: float | Unset = UNSET,
    xmax: float | Unset = UNSET,
    ymax: float | Unset = UNSET,

) -> CommonErrorsApiError | list[ModelsAffectedArea] | None:
    """  Fetch affected area

    Args:
        cycle_id (UUID): UUID identifier
        classes (list[str] | Unset):
        time_bucket (ModelsTimeBucket): Aggregation period time
        ignore_threshold (bool | Unset):
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
        CommonErrorsApiError | list[ModelsAffectedArea]
     """


    return (await asyncio_detailed(
        cycle_id=cycle_id,
client=client,
classes=classes,
time_bucket=time_bucket,
ignore_threshold=ignore_threshold,
from_=from_,
to=to,
xmin=xmin,
ymin=ymin,
xmax=xmax,
ymax=ymax,

    )).parsed
