from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_device_in_greenhouse import ModelsDeviceInGreenhouse
from ...types import Response


def _get_kwargs(
    greenhouse_id: UUID,
    device_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/greenhouses/{greenhouse_id}/devices/{device_id}".format(
            greenhouse_id=quote(str(greenhouse_id), safe=""),
            device_id=quote(str(device_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ModelsDeviceInGreenhouse | None:
    if response.status_code == 200:
        response_200 = ModelsDeviceInGreenhouse.from_dict(response.json())

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


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CommonErrorsApiError | ModelsDeviceInGreenhouse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    greenhouse_id: UUID,
    device_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | ModelsDeviceInGreenhouse]:
    """Get device in greenhouse. For M2M tokens, pass X-Organization-Id header.

    Args:
        greenhouse_id (UUID): UUID identifier
        device_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsDeviceInGreenhouse]
    """

    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
        device_id=device_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    greenhouse_id: UUID,
    device_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | ModelsDeviceInGreenhouse | None:
    """Get device in greenhouse. For M2M tokens, pass X-Organization-Id header.

    Args:
        greenhouse_id (UUID): UUID identifier
        device_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsDeviceInGreenhouse
    """

    return sync_detailed(
        greenhouse_id=greenhouse_id,
        device_id=device_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    greenhouse_id: UUID,
    device_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | ModelsDeviceInGreenhouse]:
    """Get device in greenhouse. For M2M tokens, pass X-Organization-Id header.

    Args:
        greenhouse_id (UUID): UUID identifier
        device_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsDeviceInGreenhouse]
    """

    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
        device_id=device_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    greenhouse_id: UUID,
    device_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | ModelsDeviceInGreenhouse | None:
    """Get device in greenhouse. For M2M tokens, pass X-Organization-Id header.

    Args:
        greenhouse_id (UUID): UUID identifier
        device_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsDeviceInGreenhouse
    """

    return (
        await asyncio_detailed(
            greenhouse_id=greenhouse_id,
            device_id=device_id,
            client=client,
        )
    ).parsed
