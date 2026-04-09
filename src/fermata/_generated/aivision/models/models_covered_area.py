from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.common_types_time_range import CommonTypesTimeRange


T = TypeVar("T", bound="ModelsCoveredArea")


@_attrs_define
class ModelsCoveredArea:
    """
    Attributes:
        range_ (CommonTypesTimeRange): Time range with start and end timestamps
        value (int): Covered area, in 1x1sqm cells
    """

    range_: CommonTypesTimeRange
    value: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        range_ = self.range_.to_dict()

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "range": range_,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_time_range import CommonTypesTimeRange

        d = dict(src_dict)
        range_ = CommonTypesTimeRange.from_dict(d.pop("range"))

        value = d.pop("value")

        models_covered_area = cls(
            range_=range_,
            value=value,
        )

        models_covered_area.additional_properties = d
        return models_covered_area

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
