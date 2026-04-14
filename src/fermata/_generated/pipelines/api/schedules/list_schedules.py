from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_schedules_response_200 import ListSchedulesResponse200
from ...models.models_schedule_scope import ModelsScheduleScope
from ...models.models_schedule_state import ModelsScheduleState
from ...models.models_schedule_type import ModelsScheduleType
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    template_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    state: ModelsScheduleState | Unset = UNSET,
    type_: ModelsScheduleType | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_template_id: str | Unset = UNSET
    if not isinstance(template_id, Unset):
        json_template_id = str(template_id)
    params["templateId"] = json_template_id

    json_scope: str | Unset = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    json_scope_id: str | Unset = UNSET
    if not isinstance(scope_id, Unset):
        json_scope_id = str(scope_id)
    params["scopeId"] = json_scope_id

    json_state: str | Unset = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    json_type_: str | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params["cursor"] = cursor

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/pipelines/schedules",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CommonErrorsApiError | ListSchedulesResponse200 | None:
    if response.status_code == 200:
        response_200 = ListSchedulesResponse200.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CommonErrorsApiError | ListSchedulesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    template_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    state: ModelsScheduleState | Unset = UNSET,
    type_: ModelsScheduleType | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> Response[CommonErrorsApiError | ListSchedulesResponse200]:
    """  List schedules with optional filtering

    Args:
        template_id (UUID | Unset): UUID identifier
        scope (ModelsScheduleScope | Unset): Scope type for schedule binding
        scope_id (UUID | Unset): UUID identifier
        state (ModelsScheduleState | Unset): Schedule state
        type_ (ModelsScheduleType | Unset): Schedule type indicating where the schedule is
            executed
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListSchedulesResponse200]
     """


    kwargs = _get_kwargs(
        template_id=template_id,
scope=scope,
scope_id=scope_id,
state=state,
type_=type_,
cursor=cursor,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    template_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    state: ModelsScheduleState | Unset = UNSET,
    type_: ModelsScheduleType | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> CommonErrorsApiError | ListSchedulesResponse200 | None:
    """  List schedules with optional filtering

    Args:
        template_id (UUID | Unset): UUID identifier
        scope (ModelsScheduleScope | Unset): Scope type for schedule binding
        scope_id (UUID | Unset): UUID identifier
        state (ModelsScheduleState | Unset): Schedule state
        type_ (ModelsScheduleType | Unset): Schedule type indicating where the schedule is
            executed
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListSchedulesResponse200
     """


    return sync_detailed(
        client=client,
template_id=template_id,
scope=scope,
scope_id=scope_id,
state=state,
type_=type_,
cursor=cursor,
limit=limit,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    template_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    state: ModelsScheduleState | Unset = UNSET,
    type_: ModelsScheduleType | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> Response[CommonErrorsApiError | ListSchedulesResponse200]:
    """  List schedules with optional filtering

    Args:
        template_id (UUID | Unset): UUID identifier
        scope (ModelsScheduleScope | Unset): Scope type for schedule binding
        scope_id (UUID | Unset): UUID identifier
        state (ModelsScheduleState | Unset): Schedule state
        type_ (ModelsScheduleType | Unset): Schedule type indicating where the schedule is
            executed
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListSchedulesResponse200]
     """


    kwargs = _get_kwargs(
        template_id=template_id,
scope=scope,
scope_id=scope_id,
state=state,
type_=type_,
cursor=cursor,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    template_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    state: ModelsScheduleState | Unset = UNSET,
    type_: ModelsScheduleType | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> CommonErrorsApiError | ListSchedulesResponse200 | None:
    """  List schedules with optional filtering

    Args:
        template_id (UUID | Unset): UUID identifier
        scope (ModelsScheduleScope | Unset): Scope type for schedule binding
        scope_id (UUID | Unset): UUID identifier
        state (ModelsScheduleState | Unset): Schedule state
        type_ (ModelsScheduleType | Unset): Schedule type indicating where the schedule is
            executed
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListSchedulesResponse200
     """


    return (await asyncio_detailed(
        client=client,
template_id=template_id,
scope=scope,
scope_id=scope_id,
state=state,
type_=type_,
cursor=cursor,
limit=limit,

    )).parsed
