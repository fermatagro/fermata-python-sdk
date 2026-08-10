from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.models_pipeline_status import ModelsPipelineStatus
from ...types import Response


def _get_kwargs(
    pipeline_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/inference/pipeline/{pipeline_id}/status".format(
            pipeline_id=quote(str(pipeline_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ModelsPipelineStatus | None:
    if response.status_code == 200:
        response_200 = ModelsPipelineStatus.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ModelsPipelineStatus]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pipeline_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | ModelsPipelineStatus]:
    """Aggregate status of all inference tasks submitted with a given pipeline id.
    Returns the number of tasks that have not yet reached a terminal state;
    poll until `pending` reaches zero. Responds 404 when no photos with this
    pipeline id exist in the caller's organization.

    Args:
        pipeline_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsPipelineStatus]
    """

    kwargs = _get_kwargs(
        pipeline_id=pipeline_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    pipeline_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | ModelsPipelineStatus | None:
    """Aggregate status of all inference tasks submitted with a given pipeline id.
    Returns the number of tasks that have not yet reached a terminal state;
    poll until `pending` reaches zero. Responds 404 when no photos with this
    pipeline id exist in the caller's organization.

    Args:
        pipeline_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsPipelineStatus
    """

    return sync_detailed(
        pipeline_id=pipeline_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    pipeline_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[CommonErrorsApiError | ModelsPipelineStatus]:
    """Aggregate status of all inference tasks submitted with a given pipeline id.
    Returns the number of tasks that have not yet reached a terminal state;
    poll until `pending` reaches zero. Responds 404 when no photos with this
    pipeline id exist in the caller's organization.

    Args:
        pipeline_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ModelsPipelineStatus]
    """

    kwargs = _get_kwargs(
        pipeline_id=pipeline_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    pipeline_id: UUID,
    *,
    client: AuthenticatedClient,
) -> CommonErrorsApiError | ModelsPipelineStatus | None:
    """Aggregate status of all inference tasks submitted with a given pipeline id.
    Returns the number of tasks that have not yet reached a terminal state;
    poll until `pending` reaches zero. Responds 404 when no photos with this
    pipeline id exist in the caller's organization.

    Args:
        pipeline_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ModelsPipelineStatus
    """

    return (
        await asyncio_detailed(
            pipeline_id=pipeline_id,
            client=client,
        )
    ).parsed
