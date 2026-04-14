from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_zone_object import ModelsZoneObject
from ...types import Response


def _get_kwargs(
    zone_object_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/zone-objects/{zone_object_id}".format(
            zone_object_id=quote(str(zone_object_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ModelsZoneObject | None:
    if response.status_code == 200:
        response_200 = ModelsZoneObject.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ModelsZoneObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    zone_object_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | ModelsZoneObject]:
    """Get a specific zone object

    Args:
        zone_object_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsZoneObject]
    """

    kwargs = _get_kwargs(
        zone_object_id=zone_object_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    zone_object_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | ModelsZoneObject | None:
    """Get a specific zone object

    Args:
        zone_object_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsZoneObject
    """

    return sync_detailed(
        zone_object_id=zone_object_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    zone_object_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | ModelsZoneObject]:
    """Get a specific zone object

    Args:
        zone_object_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsZoneObject]
    """

    kwargs = _get_kwargs(
        zone_object_id=zone_object_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    zone_object_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | ModelsZoneObject | None:
    """Get a specific zone object

    Args:
        zone_object_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsZoneObject
    """

    return (
        await asyncio_detailed(
            zone_object_id=zone_object_id,
            client=client,
        )
    ).parsed
