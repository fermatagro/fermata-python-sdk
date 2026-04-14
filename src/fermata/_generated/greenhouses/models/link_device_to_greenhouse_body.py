from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
    from ..models.common_types_orientation_vector import CommonTypesOrientationVector


T = TypeVar("T", bound="LinkDeviceToGreenhouseBody")


@_attrs_define
class LinkDeviceToGreenhouseBody:
    """
    Attributes:
        pos (CommonTypesFlatGridPos): Position on the flat greenhouse grid
        height (float):
        orientation_vector (CommonTypesOrientationVector | Unset): 3D orientation vector (radians)
    """

    pos: CommonTypesFlatGridPos
    height: float
    orientation_vector: CommonTypesOrientationVector | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pos = self.pos.to_dict()

        height = self.height

        orientation_vector: dict[str, Any] | Unset = UNSET
        if not isinstance(self.orientation_vector, Unset):
            orientation_vector = self.orientation_vector.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pos": pos,
                "height": height,
            }
        )
        if orientation_vector is not UNSET:
            field_dict["orientationVector"] = orientation_vector

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
        from ..models.common_types_orientation_vector import CommonTypesOrientationVector

        d = dict(src_dict)
        pos = CommonTypesFlatGridPos.from_dict(d.pop("pos"))

        height = d.pop("height")

        _orientation_vector = d.pop("orientationVector", UNSET)
        orientation_vector: CommonTypesOrientationVector | Unset
        if isinstance(_orientation_vector, Unset):
            orientation_vector = UNSET
        else:
            orientation_vector = CommonTypesOrientationVector.from_dict(_orientation_vector)

        link_device_to_greenhouse_body = cls(
            pos=pos,
            height=height,
            orientation_vector=orientation_vector,
        )

        link_device_to_greenhouse_body.additional_properties = d
        return link_device_to_greenhouse_body

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
