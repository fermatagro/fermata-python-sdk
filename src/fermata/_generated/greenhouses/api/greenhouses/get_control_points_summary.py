from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.get_control_points_summary_response_200 import GetControlPointsSummaryResponse200
from ...types import Response


def _get_kwargs(
    greenhouse_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/greenhouses/{greenhouse_id}/control-points".format(
            greenhouse_id=quote(str(greenhouse_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | GetControlPointsSummaryResponse200 | None:
    if response.status_code == 200:
        response_200 = GetControlPointsSummaryResponse200.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | GetControlPointsSummaryResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    greenhouse_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | GetControlPointsSummaryResponse200]:
    """Get control points count per device grouped by type

    Args:
        greenhouse_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | GetControlPointsSummaryResponse200]
    """

    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    greenhouse_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | GetControlPointsSummaryResponse200 | None:
    """Get control points count per device grouped by type

    Args:
        greenhouse_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | GetControlPointsSummaryResponse200
    """

    return sync_detailed(
        greenhouse_id=greenhouse_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    greenhouse_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | GetControlPointsSummaryResponse200]:
    """Get control points count per device grouped by type

    Args:
        greenhouse_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | GetControlPointsSummaryResponse200]
    """

    kwargs = _get_kwargs(
        greenhouse_id=greenhouse_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    greenhouse_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | GetControlPointsSummaryResponse200 | None:
    """Get control points count per device grouped by type

    Args:
        greenhouse_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | GetControlPointsSummaryResponse200
    """

    return (
        await asyncio_detailed(
            greenhouse_id=greenhouse_id,
            client=client,
        )
    ).parsed
