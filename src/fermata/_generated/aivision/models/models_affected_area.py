from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.common_types_time_range import CommonTypesTimeRange
  from ..models.models_affecting_class import ModelsAffectingClass





T = TypeVar("T", bound="ModelsAffectedArea")



@_attrs_define
class ModelsAffectedArea:
    """ 
        Attributes:
            range_ (CommonTypesTimeRange): Time range with start and end timestamps
            classes (list[ModelsAffectingClass]): Class codes
     """

    range_: CommonTypesTimeRange
    classes: list[ModelsAffectingClass]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.common_types_time_range import CommonTypesTimeRange
        from ..models.models_affecting_class import ModelsAffectingClass
        range_ = self.range_.to_dict()

        classes = []
        for classes_item_data in self.classes:
            classes_item = classes_item_data.to_dict()
            classes.append(classes_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "range": range_,
            "classes": classes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_time_range import CommonTypesTimeRange
        from ..models.models_affecting_class import ModelsAffectingClass
        d = dict(src_dict)
        range_ = CommonTypesTimeRange.from_dict(d.pop("range"))




        classes = []
        _classes = d.pop("classes")
        for classes_item_data in (_classes):
            classes_item = ModelsAffectingClass.from_dict(classes_item_data)



            classes.append(classes_item)


        models_affected_area = cls(
            range_=range_,
            classes=classes,
        )


        models_affected_area.additional_properties = d
        return models_affected_area

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
