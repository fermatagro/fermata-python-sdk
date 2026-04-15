from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_create_upload_link import ModelsCreateUploadLink
from ...models.models_upload_link_response import ModelsUploadLinkResponse
from ...types import Response


def _get_kwargs(
    photo_id: UUID,
    *,
    body: ModelsCreateUploadLink,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/photos/{photo_id}/upload-link".format(
            photo_id=quote(str(photo_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ModelsUploadLinkResponse | None:
    if response.status_code == 200:
        response_200 = ModelsUploadLinkResponse.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ModelsUploadLinkResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    photo_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ModelsCreateUploadLink,
) -> Response[CommonErrorsApiError | ModelsUploadLinkResponse]:
    """Get a presigned URL for direct S3 upload

    Args:
        photo_id (UUID): UUID identifier
        body (ModelsCreateUploadLink): Request to create upload link for a photo

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsUploadLinkResponse]
    """

    kwargs = _get_kwargs(
        photo_id=photo_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    photo_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ModelsCreateUploadLink,
) -> CommonErrorsApiError | ModelsUploadLinkResponse | None:
    """Get a presigned URL for direct S3 upload

    Args:
        photo_id (UUID): UUID identifier
        body (ModelsCreateUploadLink): Request to create upload link for a photo

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsUploadLinkResponse
    """

    return sync_detailed(
        photo_id=photo_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    photo_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ModelsCreateUploadLink,
) -> Response[CommonErrorsApiError | ModelsUploadLinkResponse]:
    """Get a presigned URL for direct S3 upload

    Args:
        photo_id (UUID): UUID identifier
        body (ModelsCreateUploadLink): Request to create upload link for a photo

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsUploadLinkResponse]
    """

    kwargs = _get_kwargs(
        photo_id=photo_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    photo_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ModelsCreateUploadLink,
) -> CommonErrorsApiError | ModelsUploadLinkResponse | None:
    """Get a presigned URL for direct S3 upload

    Args:
        photo_id (UUID): UUID identifier
        body (ModelsCreateUploadLink): Request to create upload link for a photo

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsUploadLinkResponse
    """

    return (
        await asyncio_detailed(
            photo_id=photo_id,
            client=client,
            body=body,
        )
    ).parsed
