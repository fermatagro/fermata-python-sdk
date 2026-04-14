from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.common_types_grid_rect import CommonTypesGridRect


T = TypeVar("T", bound="ModelsGrowingCycleRegion")


@_attrs_define
class ModelsGrowingCycleRegion:
    """A rectangular region within a growing cycle

    Attributes:
        id (UUID): UUID identifier
        growing_cycle_id (UUID): UUID identifier
        rect (CommonTypesGridRect): Rectangular area on the greenhouse grid
    """

    id: UUID
    growing_cycle_id: UUID
    rect: CommonTypesGridRect
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        growing_cycle_id = str(self.growing_cycle_id)

        rect = self.rect.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "growingCycleId": growing_cycle_id,
                "rect": rect,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_rect import CommonTypesGridRect

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        growing_cycle_id = UUID(d.pop("growingCycleId"))

        rect = CommonTypesGridRect.from_dict(d.pop("rect"))

        models_growing_cycle_region = cls(
            id=id,
            growing_cycle_id=growing_cycle_id,
            rect=rect,
        )

        models_growing_cycle_region.additional_properties = d
        return models_growing_cycle_region

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
