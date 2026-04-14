from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TransformToWorldBody")


@_attrs_define
class TransformToWorldBody:
    """
    Attributes:
        pan (float): Pan angle in radians (-π to π)
        tilt (float): Tilt angle in radians (0 to π/2)
        plane_h (float): Height of the target plane (must be non-negative)
    """

    pan: float
    tilt: float
    plane_h: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pan = self.pan

        tilt = self.tilt

        plane_h = self.plane_h

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pan": pan,
                "tilt": tilt,
                "planeH": plane_h,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pan = d.pop("pan")

        tilt = d.pop("tilt")

        plane_h = d.pop("planeH")

        transform_to_world_body = cls(
            pan=pan,
            tilt=tilt,
            plane_h=plane_h,
        )

        transform_to_world_body.additional_properties = d
        return transform_to_world_body

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
