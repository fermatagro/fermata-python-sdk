from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_reports_response_200 import ListReportsResponse200
from ...models.models_report_kind import ModelsReportKind
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    greenhouse_id: UUID | Unset = UNSET,
    kind: ModelsReportKind | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_greenhouse_id: str | Unset = UNSET
    if not isinstance(greenhouse_id, Unset):
        json_greenhouse_id = str(greenhouse_id)
    params["greenhouseId"] = json_greenhouse_id

    json_kind: str | Unset = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value

    params["kind"] = json_kind

    params["cursor"] = cursor

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/reports",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CommonErrorsApiError | ListReportsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListReportsResponse200.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CommonErrorsApiError | ListReportsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    greenhouse_id: UUID | Unset = UNSET,
    kind: ModelsReportKind | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> Response[CommonErrorsApiError | ListReportsResponse200]:
    """  List reports

    Args:
        greenhouse_id (UUID | Unset): UUID identifier
        kind (ModelsReportKind | Unset): Type of AI vision report
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListReportsResponse200]
     """


    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
kind=kind,
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
    greenhouse_id: UUID | Unset = UNSET,
    kind: ModelsReportKind | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> CommonErrorsApiError | ListReportsResponse200 | None:
    """  List reports

    Args:
        greenhouse_id (UUID | Unset): UUID identifier
        kind (ModelsReportKind | Unset): Type of AI vision report
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListReportsResponse200
     """


    return sync_detailed(
        client=client,
greenhouse_id=greenhouse_id,
kind=kind,
cursor=cursor,
limit=limit,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    greenhouse_id: UUID | Unset = UNSET,
    kind: ModelsReportKind | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> Response[CommonErrorsApiError | ListReportsResponse200]:
    """  List reports

    Args:
        greenhouse_id (UUID | Unset): UUID identifier
        kind (ModelsReportKind | Unset): Type of AI vision report
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListReportsResponse200]
     """


    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
kind=kind,
cursor=cursor,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    greenhouse_id: UUID | Unset = UNSET,
    kind: ModelsReportKind | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> CommonErrorsApiError | ListReportsResponse200 | None:
    """  List reports

    Args:
        greenhouse_id (UUID | Unset): UUID identifier
        kind (ModelsReportKind | Unset): Type of AI vision report
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListReportsResponse200
     """


    return (await asyncio_detailed(
        client=client,
greenhouse_id=greenhouse_id,
kind=kind,
cursor=cursor,
limit=limit,

    )).parsed
