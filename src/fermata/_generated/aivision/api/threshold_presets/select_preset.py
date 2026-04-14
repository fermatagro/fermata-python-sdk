from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from typing import cast
from uuid import UUID



def _get_kwargs(
    preset_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/presets/{preset_id}/select".format(preset_id=quote(str(preset_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | CommonErrorsApiError | None:
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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | CommonErrorsApiError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    preset_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Any | CommonErrorsApiError]:
    """  Select this preset as the active one for its scope (level + external_id + model_name)

    Args:
        preset_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
     """


    kwargs = _get_kwargs(
        preset_id=preset_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    preset_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Any | CommonErrorsApiError | None:
    """  Select this preset as the active one for its scope (level + external_id + model_name)

    Args:
        preset_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
     """


    return sync_detailed(
        preset_id=preset_id,
client=client,

    ).parsed

async def asyncio_detailed(
    preset_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Any | CommonErrorsApiError]:
    """  Select this preset as the active one for its scope (level + external_id + model_name)

    Args:
        preset_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CommonErrorsApiError]
     """


    kwargs = _get_kwargs(
        preset_id=preset_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    preset_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Any | CommonErrorsApiError | None:
    """  Select this preset as the active one for its scope (level + external_id + model_name)

    Args:
        preset_id (UUID): UUID identifier

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CommonErrorsApiError
     """


    return (await asyncio_detailed(
        preset_id=preset_id,
client=client,

    )).parsed
