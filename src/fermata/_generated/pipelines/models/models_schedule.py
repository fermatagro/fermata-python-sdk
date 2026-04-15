from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.models_schedule_scope import ModelsScheduleScope
from ..models.models_schedule_state import ModelsScheduleState
from ..models.models_schedule_type import ModelsScheduleType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.models_schedule_arguments import ModelsScheduleArguments


T = TypeVar("T", bound="ModelsSchedule")


@_attrs_define
class ModelsSchedule:
    """A schedule that triggers pipeline execution on a cron basis

    Attributes:
        id (UUID): UUID identifier
        organization_id (str): Organization identifier (opaque string)
        template_id (UUID): UUID identifier
        scope (ModelsScheduleScope): Scope type for schedule binding
        type_ (ModelsScheduleType): Schedule type indicating where the schedule is executed
        scope_id (UUID): UUID identifier
        state (ModelsScheduleState): Schedule state
        cron_expr_utc (str): Cron expression in UTC timezone
        arguments (ModelsScheduleArguments): Arguments to pass to the pipeline
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        start_at (datetime.datetime | Unset): When the schedule becomes active (optional)
    """

    id: UUID
    organization_id: str
    template_id: UUID
    scope: ModelsScheduleScope
    type_: ModelsScheduleType
    scope_id: UUID
    state: ModelsScheduleState
    cron_expr_utc: str
    arguments: ModelsScheduleArguments
    created_at: datetime.datetime
    updated_at: datetime.datetime
    start_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = self.organization_id

        template_id = str(self.template_id)

        scope = self.scope.value

        type_ = self.type_.value

        scope_id = str(self.scope_id)

        state = self.state.value

        cron_expr_utc = self.cron_expr_utc

        arguments = self.arguments.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        start_at: str | Unset = UNSET
        if not isinstance(self.start_at, Unset):
            start_at = self.start_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organizationId": organization_id,
                "templateId": template_id,
                "scope": scope,
                "type": type_,
                "scopeId": scope_id,
                "state": state,
                "cronExprUTC": cron_expr_utc,
                "arguments": arguments,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if start_at is not UNSET:
            field_dict["startAt"] = start_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_schedule_arguments import ModelsScheduleArguments

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        organization_id = d.pop("organizationId")

        template_id = UUID(d.pop("templateId"))

        scope = ModelsScheduleScope(d.pop("scope"))

        type_ = ModelsScheduleType(d.pop("type"))

        scope_id = UUID(d.pop("scopeId"))

        state = ModelsScheduleState(d.pop("state"))

        cron_expr_utc = d.pop("cronExprUTC")

        arguments = ModelsScheduleArguments.from_dict(d.pop("arguments"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        _start_at = d.pop("startAt", UNSET)
        start_at: datetime.datetime | Unset
        if isinstance(_start_at, Unset):
            start_at = UNSET
        else:
            start_at = isoparse(_start_at)

        models_schedule = cls(
            id=id,
            organization_id=organization_id,
            template_id=template_id,
            scope=scope,
            type_=type_,
            scope_id=scope_id,
            state=state,
            cron_expr_utc=cron_expr_utc,
            arguments=arguments,
            created_at=created_at,
            updated_at=updated_at,
            start_at=start_at,
        )

        models_schedule.additional_properties = d
        return models_schedule

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
