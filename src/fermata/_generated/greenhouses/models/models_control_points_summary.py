from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ModelsControlPointsSummary")


@_attrs_define
class ModelsControlPointsSummary:
    """Control points count per device grouped by type

    Attributes:
        device_id (UUID): UUID identifier
        reference_count (int):
        control_count (int):
    """

    device_id: UUID
    reference_count: int
    control_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        device_id = str(self.device_id)

        reference_count = self.reference_count

        control_count = self.control_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deviceId": device_id,
                "referenceCount": reference_count,
                "controlCount": control_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        device_id = UUID(d.pop("deviceId"))

        reference_count = d.pop("referenceCount")

        control_count = d.pop("controlCount")

        models_control_points_summary = cls(
            device_id=device_id,
            reference_count=reference_count,
            control_count=control_count,
        )

        models_control_points_summary.additional_properties = d
        return models_control_points_summary

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
