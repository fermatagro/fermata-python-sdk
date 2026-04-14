from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.common_types_grid_rect import CommonTypesGridRect


T = TypeVar("T", bound="CreateOrUpdateGrowingCycleRegion")


@_attrs_define
class CreateOrUpdateGrowingCycleRegion:
    """
    Attributes:
        rect (CommonTypesGridRect): Rectangular area on the greenhouse grid
    """

    rect: CommonTypesGridRect
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rect = self.rect.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rect": rect,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_rect import CommonTypesGridRect

        d = dict(src_dict)
        rect = CommonTypesGridRect.from_dict(d.pop("rect"))

        create_or_update_growing_cycle_region = cls(
            rect=rect,
        )

        create_or_update_growing_cycle_region.additional_properties = d
        return create_or_update_growing_cycle_region

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
