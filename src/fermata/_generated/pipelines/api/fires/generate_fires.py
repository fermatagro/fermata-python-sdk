from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_generate_fires_result import ModelsGenerateFiresResult
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/pipelines/fires/generate",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CommonErrorsApiError | ModelsGenerateFiresResult | None:
    if response.status_code == 200:
        response_200 = ModelsGenerateFiresResult.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CommonErrorsApiError | ModelsGenerateFiresResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[CommonErrorsApiError | ModelsGenerateFiresResult]:
    """  Generate missing schedule-triggered fires.

    Scheduler/system operation that creates Fire records for all enabled schedules
    up to the current time.

    Idempotent via deduplicationKey uniqueness - if a fire already exists for a
    given schedule+scheduledAt combination, it is counted as skipped.

    Returns counts of created/skipped fires.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsGenerateFiresResult]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> CommonErrorsApiError | ModelsGenerateFiresResult | None:
    """  Generate missing schedule-triggered fires.

    Scheduler/system operation that creates Fire records for all enabled schedules
    up to the current time.

    Idempotent via deduplicationKey uniqueness - if a fire already exists for a
    given schedule+scheduledAt combination, it is counted as skipped.

    Returns counts of created/skipped fires.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsGenerateFiresResult
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[CommonErrorsApiError | ModelsGenerateFiresResult]:
    """  Generate missing schedule-triggered fires.

    Scheduler/system operation that creates Fire records for all enabled schedules
    up to the current time.

    Idempotent via deduplicationKey uniqueness - if a fire already exists for a
    given schedule+scheduledAt combination, it is counted as skipped.

    Returns counts of created/skipped fires.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsGenerateFiresResult]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> CommonErrorsApiError | ModelsGenerateFiresResult | None:
    """  Generate missing schedule-triggered fires.

    Scheduler/system operation that creates Fire records for all enabled schedules
    up to the current time.

    Idempotent via deduplicationKey uniqueness - if a fire already exists for a
    given schedule+scheduledAt combination, it is counted as skipped.

    Returns counts of created/skipped fires.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsGenerateFiresResult
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
