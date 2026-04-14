import datetime
from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.common_errors_api_error import CommonErrorsApiError
from ...models.list_fires_response_200 import ListFiresResponse200
from ...models.models_fire_status import ModelsFireStatus
from ...models.models_schedule_scope import ModelsScheduleScope
from ...models.models_trigger_type import ModelsTriggerType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    pipeline_template_id: UUID | Unset = UNSET,
    trigger_type: ModelsTriggerType | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    status: ModelsFireStatus | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_pipeline_template_id: str | Unset = UNSET
    if not isinstance(pipeline_template_id, Unset):
        json_pipeline_template_id = str(pipeline_template_id)
    params["pipelineTemplateId"] = json_pipeline_template_id

    json_trigger_type: str | Unset = UNSET
    if not isinstance(trigger_type, Unset):
        json_trigger_type = trigger_type.value

    params["triggerType"] = json_trigger_type

    json_trigger_id: str | Unset = UNSET
    if not isinstance(trigger_id, Unset):
        json_trigger_id = str(trigger_id)
    params["triggerId"] = json_trigger_id

    json_scope: str | Unset = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value

    params["scope"] = json_scope

    json_scope_id: str | Unset = UNSET
    if not isinstance(scope_id, Unset):
        json_scope_id = str(scope_id)
    params["scopeId"] = json_scope_id

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/pipelines/fires",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommonErrorsApiError | ListFiresResponse200 | None:
    if response.status_code == 200:
        response_200 = ListFiresResponse200.from_dict(response.json())

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
) -> Response[CommonErrorsApiError | ListFiresResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    pipeline_template_id: UUID | Unset = UNSET,
    trigger_type: ModelsTriggerType | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    status: ModelsFireStatus | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListFiresResponse200]:
    """List fires with optional filtering.

    Supports filtering by template, trigger, status, and time window.
    Time filters apply to scheduledAt field.

    Args:
        pipeline_template_id (UUID | Unset): UUID identifier
        trigger_type (ModelsTriggerType | Unset): What triggered the fire
        trigger_id (UUID | Unset): UUID identifier
        scope (ModelsScheduleScope | Unset): Scope type for schedule binding
        scope_id (UUID | Unset): UUID identifier
        status (ModelsFireStatus | Unset): Current status of the fire.

            State transitions:
            - pending → running → completed|partial|failed
            - pending|running → cancelled|skipped
            - failed|cancelled → running (retry)
        from_ (datetime.datetime):
        to (datetime.datetime):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListFiresResponse200]
    """

    kwargs = _get_kwargs(
        pipeline_template_id=pipeline_template_id,
        trigger_type=trigger_type,
        trigger_id=trigger_id,
        scope=scope,
        scope_id=scope_id,
        status=status,
        from_=from_,
        to=to,
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
    pipeline_template_id: UUID | Unset = UNSET,
    trigger_type: ModelsTriggerType | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    status: ModelsFireStatus | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListFiresResponse200 | None:
    """List fires with optional filtering.

    Supports filtering by template, trigger, status, and time window.
    Time filters apply to scheduledAt field.

    Args:
        pipeline_template_id (UUID | Unset): UUID identifier
        trigger_type (ModelsTriggerType | Unset): What triggered the fire
        trigger_id (UUID | Unset): UUID identifier
        scope (ModelsScheduleScope | Unset): Scope type for schedule binding
        scope_id (UUID | Unset): UUID identifier
        status (ModelsFireStatus | Unset): Current status of the fire.

            State transitions:
            - pending → running → completed|partial|failed
            - pending|running → cancelled|skipped
            - failed|cancelled → running (retry)
        from_ (datetime.datetime):
        to (datetime.datetime):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListFiresResponse200
    """

    return sync_detailed(
        client=client,
        pipeline_template_id=pipeline_template_id,
        trigger_type=trigger_type,
        trigger_id=trigger_id,
        scope=scope,
        scope_id=scope_id,
        status=status,
        from_=from_,
        to=to,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    pipeline_template_id: UUID | Unset = UNSET,
    trigger_type: ModelsTriggerType | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    status: ModelsFireStatus | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[CommonErrorsApiError | ListFiresResponse200]:
    """List fires with optional filtering.

    Supports filtering by template, trigger, status, and time window.
    Time filters apply to scheduledAt field.

    Args:
        pipeline_template_id (UUID | Unset): UUID identifier
        trigger_type (ModelsTriggerType | Unset): What triggered the fire
        trigger_id (UUID | Unset): UUID identifier
        scope (ModelsScheduleScope | Unset): Scope type for schedule binding
        scope_id (UUID | Unset): UUID identifier
        status (ModelsFireStatus | Unset): Current status of the fire.

            State transitions:
            - pending → running → completed|partial|failed
            - pending|running → cancelled|skipped
            - failed|cancelled → running (retry)
        from_ (datetime.datetime):
        to (datetime.datetime):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommonErrorsApiError | ListFiresResponse200]
    """

    kwargs = _get_kwargs(
        pipeline_template_id=pipeline_template_id,
        trigger_type=trigger_type,
        trigger_id=trigger_id,
        scope=scope,
        scope_id=scope_id,
        status=status,
        from_=from_,
        to=to,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    pipeline_template_id: UUID | Unset = UNSET,
    trigger_type: ModelsTriggerType | Unset = UNSET,
    trigger_id: UUID | Unset = UNSET,
    scope: ModelsScheduleScope | Unset = UNSET,
    scope_id: UUID | Unset = UNSET,
    status: ModelsFireStatus | Unset = UNSET,
    from_: datetime.datetime,
    to: datetime.datetime,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,
) -> CommonErrorsApiError | ListFiresResponse200 | None:
    """List fires with optional filtering.

    Supports filtering by template, trigger, status, and time window.
    Time filters apply to scheduledAt field.

    Args:
        pipeline_template_id (UUID | Unset): UUID identifier
        trigger_type (ModelsTriggerType | Unset): What triggered the fire
        trigger_id (UUID | Unset): UUID identifier
        scope (ModelsScheduleScope | Unset): Scope type for schedule binding
        scope_id (UUID | Unset): UUID identifier
        status (ModelsFireStatus | Unset): Current status of the fire.

            State transitions:
            - pending → running → completed|partial|failed
            - pending|running → cancelled|skipped
            - failed|cancelled → running (retry)
        from_ (datetime.datetime):
        to (datetime.datetime):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommonErrorsApiError | ListFiresResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            pipeline_template_id=pipeline_template_id,
            trigger_type=trigger_type,
            trigger_id=trigger_id,
            scope=scope,
            scope_id=scope_id,
            status=status,
            from_=from_,
            to=to,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
