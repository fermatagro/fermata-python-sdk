from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_upload_predictions_request import ModelsUploadPredictionsRequest
from ...models.models_upload_predictions_response import ModelsUploadPredictionsResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ModelsUploadPredictionsRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/predictions/upload",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ModelsUploadPredictionsResponse | None:
    if response.status_code == 201:
        response_201 = ModelsUploadPredictionsResponse.from_dict(response.json())

        return response_201

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


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CommonErrorsApiError | ModelsUploadPredictionsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ModelsUploadPredictionsRequest,
) -> Response[CommonErrorsApiError | ModelsUploadPredictionsResponse]:
    """Upload pre-computed predictions for a photo. Stores predictions directly without ML API processing.

    Args:
        body (ModelsUploadPredictionsRequest): Request to upload pre-computed predictions for a
            photo

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsUploadPredictionsResponse]
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
    body: ModelsUploadPredictionsRequest,
) -> CommonErrorsApiError | ModelsUploadPredictionsResponse | None:
    """Upload pre-computed predictions for a photo. Stores predictions directly without ML API processing.

    Args:
        body (ModelsUploadPredictionsRequest): Request to upload pre-computed predictions for a
            photo

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsUploadPredictionsResponse
    """

    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ModelsUploadPredictionsRequest,
) -> Response[CommonErrorsApiError | ModelsUploadPredictionsResponse]:
    """Upload pre-computed predictions for a photo. Stores predictions directly without ML API processing.

    Args:
        body (ModelsUploadPredictionsRequest): Request to upload pre-computed predictions for a
            photo

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsUploadPredictionsResponse]
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
    body: ModelsUploadPredictionsRequest,
) -> CommonErrorsApiError | ModelsUploadPredictionsResponse | None:
    """Upload pre-computed predictions for a photo. Stores predictions directly without ML API processing.

    Args:
        body (ModelsUploadPredictionsRequest): Request to upload pre-computed predictions for a
            photo

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsUploadPredictionsResponse
    """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
