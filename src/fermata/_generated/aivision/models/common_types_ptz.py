from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CommonTypesPTZ")



@_attrs_define
class CommonTypesPTZ:
    """ Pan-Tilt-Zoom camera position. Pan and tilt are in radians.

        Attributes:
            pan (float): Pan angle in radians (-π to π)
            tilt (float): Tilt angle in radians (0 to π/2)
            zoom (float): Zoom level (camera-specific, e.g., 1-25)
     """

    pan: float
    tilt: float
    zoom: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        pan = self.pan

        tilt = self.tilt

        zoom = self.zoom


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "pan": pan,
            "tilt": tilt,
            "zoom": zoom,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pan = d.pop("pan")

        tilt = d.pop("tilt")

        zoom = d.pop("zoom")

        common_types_ptz = cls(
            pan=pan,
            tilt=tilt,
            zoom=zoom,
        )


        common_types_ptz.additional_properties = d
        return common_types_ptz

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
