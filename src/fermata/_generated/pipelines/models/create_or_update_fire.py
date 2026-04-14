from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.models_fire_status import ModelsFireStatus
from ..models.models_schedule_scope import ModelsScheduleScope
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.create_or_update_fire_arguments import CreateOrUpdateFireArguments





T = TypeVar("T", bound="CreateOrUpdateFire")



@_attrs_define
class CreateOrUpdateFire:
    """ 
        Attributes:
            organization_id (str): Organization identifier (opaque string)
            pipeline_template_id (UUID): UUID identifier
            trigger_id (UUID): UUID identifier
            scope (ModelsScheduleScope): Scope type for schedule binding
            scope_id (UUID): UUID identifier
            status (ModelsFireStatus): Current status of the fire.

                State transitions:
                - pending → running → completed|partial|failed
                - pending|running → cancelled|skipped
                - failed|cancelled → running (retry)
            scheduled_at (datetime.datetime | Unset): When the pipeline is scheduled to run (defaults to server time if
                omitted)
            external_run_id (str | Unset): Prefect flow_run_id, set at start (immutable once set)
            error_message (str | Unset): Error message (present when status=failed or status=partial)
            arguments (CreateOrUpdateFireArguments | Unset): Arguments passed to the pipeline execution
            started_at (datetime.datetime | Unset): When execution actually started (status changed to running)
            finished_at (datetime.datetime | Unset): When execution finished (terminal status reached)
     """

    organization_id: str
    pipeline_template_id: UUID
    trigger_id: UUID
    scope: ModelsScheduleScope
    scope_id: UUID
    status: ModelsFireStatus
    scheduled_at: datetime.datetime | Unset = UNSET
    external_run_id: str | Unset = UNSET
    error_message: str | Unset = UNSET
    arguments: CreateOrUpdateFireArguments | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    finished_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_or_update_fire_arguments import CreateOrUpdateFireArguments
        organization_id = self.organization_id

        pipeline_template_id = str(self.pipeline_template_id)

        trigger_id = str(self.trigger_id)

        scope = self.scope.value

        scope_id = str(self.scope_id)

        status = self.status.value

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
        field_dict.update({
            "organizationId": organization_id,
            "pipelineTemplateId": pipeline_template_id,
            "triggerId": trigger_id,
            "scope": scope,
            "scopeId": scope_id,
            "status": status,
        })
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
        from ..models.create_or_update_fire_arguments import CreateOrUpdateFireArguments
        d = dict(src_dict)
        organization_id = d.pop("organizationId")

        pipeline_template_id = UUID(d.pop("pipelineTemplateId"))




        trigger_id = UUID(d.pop("triggerId"))




        scope = ModelsScheduleScope(d.pop("scope"))




        scope_id = UUID(d.pop("scopeId"))




        status = ModelsFireStatus(d.pop("status"))




        _scheduled_at = d.pop("scheduledAt", UNSET)
        scheduled_at: datetime.datetime | Unset
        if isinstance(_scheduled_at,  Unset):
            scheduled_at = UNSET
        else:
            scheduled_at = isoparse(_scheduled_at)




        external_run_id = d.pop("externalRunId", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        _arguments = d.pop("arguments", UNSET)
        arguments: CreateOrUpdateFireArguments | Unset
        if isinstance(_arguments,  Unset):
            arguments = UNSET
        else:
            arguments = CreateOrUpdateFireArguments.from_dict(_arguments)




        _started_at = d.pop("startedAt", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)




        _finished_at = d.pop("finishedAt", UNSET)
        finished_at: datetime.datetime | Unset
        if isinstance(_finished_at,  Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)




        create_or_update_fire = cls(
            organization_id=organization_id,
            pipeline_template_id=pipeline_template_id,
            trigger_id=trigger_id,
            scope=scope,
            scope_id=scope_id,
            status=status,
            scheduled_at=scheduled_at,
            external_run_id=external_run_id,
            error_message=error_message,
            arguments=arguments,
            started_at=started_at,
            finished_at=finished_at,
        )


        create_or_update_fire.additional_properties = d
        return create_or_update_fire

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
