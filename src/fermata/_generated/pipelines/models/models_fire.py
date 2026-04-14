from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.models_fire_status import ModelsFireStatus
from ..models.models_schedule_scope import ModelsScheduleScope
from ..models.models_trigger_type import ModelsTriggerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.models_fire_arguments import ModelsFireArguments


T = TypeVar("T", bound="ModelsFire")


@_attrs_define
class ModelsFire:
    """A Fire represents a single scheduled occurrence/execution instance for a pipeline template.

    Immutable planning fields: pipelineTemplateId, triggerType, triggerId, scheduledAt, deduplicationKey, arguments.
    Mutable execution fields: status, externalRunId, errorMessage, startedAt, finishedAt.

    Deduplication rules (unique constraint on deduplicationKey):
    - For triggerType="request": deduplicationKey = "request:{triggerId}"
    - For triggerType="schedule": deduplicationKey = "schedule:{triggerId}:{scheduledAtISO}"

    POST /fires is idempotent: if deduplicationKey exists, returns existing Fire.

        Attributes:
            id (UUID): UUID identifier
            organization_id (str): Organization identifier (opaque string)
            pipeline_template_id (UUID): UUID identifier
            trigger_type (ModelsTriggerType): What triggered the fire
            trigger_id (UUID): UUID identifier
            scope (ModelsScheduleScope): Scope type for schedule binding
            scope_id (UUID): UUID identifier
            deduplication_key (str): Unique key for deduplication (server-generated, see model docs for format)
            status (ModelsFireStatus): Current status of the fire.

                State transitions:
                - pending → running → completed|partial|failed
                - pending|running → cancelled|skipped
                - failed|cancelled → running (retry)
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            scheduled_at (datetime.datetime | Unset): When the pipeline is scheduled to run (defaults to server time if
                omitted)
            external_run_id (str | Unset): Prefect flow_run_id, set at start (immutable once set)
            error_message (str | Unset): Error message (present when status=failed or status=partial)
            arguments (ModelsFireArguments | Unset): Arguments passed to the pipeline execution
            started_at (datetime.datetime | Unset): When execution actually started (status changed to running)
            finished_at (datetime.datetime | Unset): When execution finished (terminal status reached)
    """

    id: UUID
    organization_id: str
    pipeline_template_id: UUID
    trigger_type: ModelsTriggerType
    trigger_id: UUID
    scope: ModelsScheduleScope
    scope_id: UUID
    deduplication_key: str
    status: ModelsFireStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    scheduled_at: datetime.datetime | Unset = UNSET
    external_run_id: str | Unset = UNSET
    error_message: str | Unset = UNSET
    arguments: ModelsFireArguments | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    finished_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = self.organization_id

        pipeline_template_id = str(self.pipeline_template_id)

        trigger_type = self.trigger_type.value

        trigger_id = str(self.trigger_id)

        scope = self.scope.value

        scope_id = str(self.scope_id)

        deduplication_key = self.deduplication_key

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        scheduled_at: str | Unset = UNSET
        if not isinstance(self.scheduled_at, Unset):
            scheduled_at = self.scheduled_at.isoformat()

        external_run_id = self.external_run_id

        error_message = self.error_message

        arguments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        finished_at: str | Unset = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organizationId": organization_id,
                "pipelineTemplateId": pipeline_template_id,
                "triggerType": trigger_type,
                "triggerId": trigger_id,
                "scope": scope,
                "scopeId": scope_id,
                "deduplicationKey": deduplication_key,
                "status": status,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if scheduled_at is not UNSET:
            field_dict["scheduledAt"] = scheduled_at
        if external_run_id is not UNSET:
            field_dict["externalRunId"] = external_run_id
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if arguments is not UNSET:
            field_dict["arguments"] = arguments
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_fire_arguments import ModelsFireArguments

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        organization_id = d.pop("organizationId")

        pipeline_template_id = UUID(d.pop("pipelineTemplateId"))

        trigger_type = ModelsTriggerType(d.pop("triggerType"))

        trigger_id = UUID(d.pop("triggerId"))

        scope = ModelsScheduleScope(d.pop("scope"))

        scope_id = UUID(d.pop("scopeId"))

        deduplication_key = d.pop("deduplicationKey")

        status = ModelsFireStatus(d.pop("status"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        _scheduled_at = d.pop("scheduledAt", UNSET)
        scheduled_at: datetime.datetime | Unset
        if isinstance(_scheduled_at, Unset):
            scheduled_at = UNSET
        else:
            scheduled_at = isoparse(_scheduled_at)

        external_run_id = d.pop("externalRunId", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        _arguments = d.pop("arguments", UNSET)
        arguments: ModelsFireArguments | Unset
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = ModelsFireArguments.from_dict(_arguments)

        _started_at = d.pop("startedAt", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        _finished_at = d.pop("finishedAt", UNSET)
        finished_at: datetime.datetime | Unset
        if isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        models_fire = cls(
            id=id,
            organization_id=organization_id,
            pipeline_template_id=pipeline_template_id,
            trigger_type=trigger_type,
            trigger_id=trigger_id,
            scope=scope,
            scope_id=scope_id,
            deduplication_key=deduplication_key,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            scheduled_at=scheduled_at,
            external_run_id=external_run_id,
            error_message=error_message,
            arguments=arguments,
            started_at=started_at,
            finished_at=finished_at,
        )

        models_fire.additional_properties = d
        return models_fire

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
