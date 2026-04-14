from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_start_fire_request import ModelsStartFireRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    fire_id: UUID,
    *,
    body: ModelsStartFireRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/pipelines/fires/{fire_id}/start".format(fire_id=quote(str(fire_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | CommonErrorsApiError | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | CommonErrorsApiError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    fire_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ModelsStartFireRequest,

) -> Response[Any | CommonErrorsApiError]:
    """  Start a fire.

    Transitions status from pending to running.
    Sets startedAt=now and stores externalRunId (Prefect flow_run_id).
    externalRunId is immutable once set.

    Args:
        fire_id (UUID): UUID identifier
        body (ModelsStartFireRequest): Request to start a fire

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
     """


    kwargs = _get_kwargs(
        fire_id=fire_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    fire_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ModelsStartFireRequest,

) -> Any | CommonErrorsApiError | None:
    """  Start a fire.

    Transitions status from pending to running.
    Sets startedAt=now and stores externalRunId (Prefect flow_run_id).
    externalRunId is immutable once set.

    Args:
        fire_id (UUID): UUID identifier
        body (ModelsStartFireRequest): Request to start a fire

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
     """


    return sync_detailed(
        fire_id=fire_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    fire_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ModelsStartFireRequest,

) -> Response[Any | CommonErrorsApiError]:
    """  Start a fire.

    Transitions status from pending to running.
    Sets startedAt=now and stores externalRunId (Prefect flow_run_id).
    externalRunId is immutable once set.

    Args:
        fire_id (UUID): UUID identifier
        body (ModelsStartFireRequest): Request to start a fire

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
     """


    kwargs = _get_kwargs(
        fire_id=fire_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    fire_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ModelsStartFireRequest,

) -> Any | CommonErrorsApiError | None:
    """  Start a fire.

    Transitions status from pending to running.
    Sets startedAt=now and stores externalRunId (Prefect flow_run_id).
    externalRunId is immutable once set.

    Args:
        fire_id (UUID): UUID identifier
        body (ModelsStartFireRequest): Request to start a fire

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
     """


    return (await asyncio_detailed(
        fire_id=fire_id,
client=client,
body=body,

    )).parsed
