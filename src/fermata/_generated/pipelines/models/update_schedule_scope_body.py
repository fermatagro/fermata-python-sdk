from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.models_schedule_scope import ModelsScheduleScope

T = TypeVar("T", bound="UpdateScheduleScopeBody")


@_attrs_define
class UpdateScheduleScopeBody:
    """
    Attributes:
        scope (ModelsScheduleScope): Scope type for schedule binding
        scope_id (UUID): UUID identifier
    """

    scope: ModelsScheduleScope
    scope_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope.value

        scope_id = str(self.scope_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope": scope,
                "scopeId": scope_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scope = ModelsScheduleScope(d.pop("scope"))

        scope_id = UUID(d.pop("scopeId"))

        update_schedule_scope_body = cls(
            scope=scope,
            scope_id=scope_id,
        )

        update_schedule_scope_body.additional_properties = d
        return update_schedule_scope_body

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
