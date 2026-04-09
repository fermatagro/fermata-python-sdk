from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_photo_batch import ModelsPhotoBatch
from ...types import UNSET, Response


def _get_kwargs(
    *,
    photo_ids: list[UUID],
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_photo_ids = []
    for photo_ids_item_data in photo_ids:
        photo_ids_item = str(photo_ids_item_data)
        json_photo_ids.append(photo_ids_item)

    params["photoIds"] = json_photo_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/photos/batch",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ModelsPhotoBatch | None:
    if response.status_code == 200:
        response_200 = ModelsPhotoBatch.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ModelsPhotoBatch]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    photo_ids: list[UUID],
) -> Response[CommonErrorsApiError | ModelsPhotoBatch]:
    """Get a batch of photos by IDs

    Args:
        photo_ids (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsPhotoBatch]
    """

    kwargs = _get_kwargs(
        photo_ids=photo_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    photo_ids: list[UUID],
) -> CommonErrorsApiError | ModelsPhotoBatch | None:
    """Get a batch of photos by IDs

    Args:
        photo_ids (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsPhotoBatch
    """

    return sync_detailed(
        client=client,
        photo_ids=photo_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    photo_ids: list[UUID],
) -> Response[CommonErrorsApiError | ModelsPhotoBatch]:
    """Get a batch of photos by IDs

    Args:
        photo_ids (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsPhotoBatch]
    """

    kwargs = _get_kwargs(
        photo_ids=photo_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    photo_ids: list[UUID],
) -> CommonErrorsApiError | ModelsPhotoBatch | None:
    """Get a batch of photos by IDs

    Args:
        photo_ids (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsPhotoBatch
    """

    return (
        await asyncio_detailed(
            client=client,
            photo_ids=photo_ids,
        )
    ).parsed
