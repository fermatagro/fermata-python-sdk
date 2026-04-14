from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_treatment import ModelsTreatment
from ...types import Response


def _get_kwargs(
    cycle_id: UUID,
    treatment_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/cycles/{cycle_id}/treatments/{treatment_id}".format(
            cycle_id=quote(str(cycle_id), safe=""),
            treatment_id=quote(str(treatment_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ModelsTreatment | None:
    if response.status_code == 200:
        response_200 = ModelsTreatment.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ModelsTreatment]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    cycle_id: UUID,
    treatment_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | ModelsTreatment]:
    """Get a specific treatment

    Args:
        cycle_id (UUID): UUID identifier
        treatment_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsTreatment]
    """

    kwargs = _get_kwargs(
        cycle_id=cycle_id,
        treatment_id=treatment_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    cycle_id: UUID,
    treatment_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | ModelsTreatment | None:
    """Get a specific treatment

    Args:
        cycle_id (UUID): UUID identifier
        treatment_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsTreatment
    """

    return sync_detailed(
        cycle_id=cycle_id,
        treatment_id=treatment_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    cycle_id: UUID,
    treatment_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | ModelsTreatment]:
    """Get a specific treatment

    Args:
        cycle_id (UUID): UUID identifier
        treatment_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsTreatment]
    """

    kwargs = _get_kwargs(
        cycle_id=cycle_id,
        treatment_id=treatment_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cycle_id: UUID,
    treatment_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | ModelsTreatment | None:
    """Get a specific treatment

    Args:
        cycle_id (UUID): UUID identifier
        treatment_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsTreatment
    """

    return (
        await asyncio_detailed(
            cycle_id=cycle_id,
            treatment_id=treatment_id,
            client=client,
        )
    ).parsed
