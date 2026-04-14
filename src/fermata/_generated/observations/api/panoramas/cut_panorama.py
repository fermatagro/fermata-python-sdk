from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_cut_panorama_request import ModelsCutPanoramaRequest
from ...models.models_cut_panorama_response import ModelsCutPanoramaResponse
from typing import cast



def _get_kwargs(
    *,
    body: ModelsCutPanoramaRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/panoramas/cut",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CommonErrorsApiError | ModelsCutPanoramaResponse | None:
    if response.status_code == 202:
        response_202 = ModelsCutPanoramaResponse.from_dict(response.json())



        return response_202

    if response.status_code == 400:
        response_400 = CommonErrorsApiError.from_dict(response.json())



        return response_400

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CommonErrorsApiError | ModelsCutPanoramaResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ModelsCutPanoramaRequest,

) -> Response[CommonErrorsApiError | ModelsCutPanoramaResponse]:
    """  Submit a cut-only tile generation job for an existing panorama

    Args:
        body (ModelsCutPanoramaRequest): Request to submit a cut-only tile generation job for an
            existing panorama

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsCutPanoramaResponse]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: ModelsCutPanoramaRequest,

) -> CommonErrorsApiError | ModelsCutPanoramaResponse | None:
    """  Submit a cut-only tile generation job for an existing panorama

    Args:
        body (ModelsCutPanoramaRequest): Request to submit a cut-only tile generation job for an
            existing panorama

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsCutPanoramaResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ModelsCutPanoramaRequest,

) -> Response[CommonErrorsApiError | ModelsCutPanoramaResponse]:
    """  Submit a cut-only tile generation job for an existing panorama

    Args:
        body (ModelsCutPanoramaRequest): Request to submit a cut-only tile generation job for an
            existing panorama

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsCutPanoramaResponse]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ModelsCutPanoramaRequest,

) -> CommonErrorsApiError | ModelsCutPanoramaResponse | None:
    """  Submit a cut-only tile generation job for an existing panorama

    Args:
        body (ModelsCutPanoramaRequest): Request to submit a cut-only tile generation job for an
            existing panorama

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsCutPanoramaResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
