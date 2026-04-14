from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.update_schedule_scope_body import UpdateScheduleScopeBody
from ...types import Response


def _get_kwargs(
    schedule_id: UUID,
    *,
    body: UpdateScheduleScopeBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/pipelines/schedules/{schedule_id}/scope".format(
            schedule_id=quote(str(schedule_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | CommonErrorsApiError | None:
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


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | CommonErrorsApiError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    schedule_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateScheduleScopeBody,
) -> Response[Any | CommonErrorsApiError]:
    """Update schedule scope binding

    Args:
        schedule_id (UUID): UUID identifier
        body (UpdateScheduleScopeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
    """

    kwargs = _get_kwargs(
        schedule_id=schedule_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    schedule_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateScheduleScopeBody,
) -> Any | CommonErrorsApiError | None:
    """Update schedule scope binding

    Args:
        schedule_id (UUID): UUID identifier
        body (UpdateScheduleScopeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
    """

    return sync_detailed(
        schedule_id=schedule_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    schedule_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateScheduleScopeBody,
) -> Response[Any | CommonErrorsApiError]:
    """Update schedule scope binding

    Args:
        schedule_id (UUID): UUID identifier
        body (UpdateScheduleScopeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
    """

    kwargs = _get_kwargs(
        schedule_id=schedule_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    schedule_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateScheduleScopeBody,
) -> Any | CommonErrorsApiError | None:
    """Update schedule scope binding

    Args:
        schedule_id (UUID): UUID identifier
        body (UpdateScheduleScopeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
    """

    return (
        await asyncio_detailed(
            schedule_id=schedule_id,
            client=client,
            body=body,
        )
    ).parsed
