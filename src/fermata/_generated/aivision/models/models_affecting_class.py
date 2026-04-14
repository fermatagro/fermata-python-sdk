from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ModelsAffectingClass")



@_attrs_define
class ModelsAffectingClass:
    """ 
        Attributes:
            class_ (str): Class code
            value (int): Affected area, in 1x1sqm cells
            detection_count (int): Total number of detections for this class in this time bucket
            box_count (int): Total number of prediction boxes for this class in this time bucket
     """

    class_: str
    value: int
    detection_count: int
    box_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        class_ = self.class_

        value = self.value

        detection_count = self.detection_count

        box_count = self.box_count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "class": class_,
            "value": value,
            "detectionCount": detection_count,
            "boxCount": box_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        class_ = d.pop("class")

        value = d.pop("value")

        detection_count = d.pop("detectionCount")

        box_count = d.pop("boxCount")

        models_affecting_class = cls(
            class_=class_,
            value=value,
            detection_count=detection_count,
            box_count=box_count,
        )


        models_affecting_class.additional_properties = d
        return models_affecting_class

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
