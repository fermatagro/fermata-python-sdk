from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.create_or_update_report import CreateOrUpdateReport
from typing import cast
from uuid import UUID



def _get_kwargs(
    report_id: UUID,
    *,
    body: CreateOrUpdateReport,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/reports/{report_id}".format(report_id=quote(str(report_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | CommonErrorsApiError | None:
    if response.status_code == 201:
        response_201 = cast(Any, None)
        return response_201

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | CommonErrorsApiError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    report_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateOrUpdateReport,

) -> Response[Any | CommonErrorsApiError]:
    """  Generate a new report

    Args:
        report_id (UUID): UUID identifier
        body (CreateOrUpdateReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
     """


    kwargs = _get_kwargs(
        report_id=report_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    report_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateOrUpdateReport,

) -> Any | CommonErrorsApiError | None:
    """  Generate a new report

    Args:
        report_id (UUID): UUID identifier
        body (CreateOrUpdateReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
     """


    return sync_detailed(
        report_id=report_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    report_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateOrUpdateReport,

) -> Response[Any | CommonErrorsApiError]:
    """  Generate a new report

    Args:
        report_id (UUID): UUID identifier
        body (CreateOrUpdateReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
     """


    kwargs = _get_kwargs(
        report_id=report_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    report_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateOrUpdateReport,

) -> Any | CommonErrorsApiError | None:
    """  Generate a new report

    Args:
        report_id (UUID): UUID identifier
        body (CreateOrUpdateReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
     """


    return (await asyncio_detailed(
        report_id=report_id,
client=client,
body=body,

    )).parsed
