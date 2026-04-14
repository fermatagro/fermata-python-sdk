from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
    from ..models.common_types_grid_rect import CommonTypesGridRect


T = TypeVar("T", bound="RelocateGreenhouseObjectBody")


@_attrs_define
class RelocateGreenhouseObjectBody:
    """
    Attributes:
        height (float):
        pos (CommonTypesFlatGridPos | Unset): Position on the flat greenhouse grid
        rect (CommonTypesGridRect | Unset): Rectangular area on the greenhouse grid
    """

    height: float
    pos: CommonTypesFlatGridPos | Unset = UNSET
    rect: CommonTypesGridRect | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        height = self.height

        pos: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pos, Unset):
            pos = self.pos.to_dict()

        rect: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rect, Unset):
            rect = self.rect.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "height": height,
            }
        )
        if pos is not UNSET:
            field_dict["pos"] = pos
        if rect is not UNSET:
            field_dict["rect"] = rect

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
        from ..models.common_types_grid_rect import CommonTypesGridRect

        d = dict(src_dict)
        height = d.pop("height")

        _pos = d.pop("pos", UNSET)
        pos: CommonTypesFlatGridPos | Unset
        if isinstance(_pos, Unset):
            pos = UNSET
        else:
            pos = CommonTypesFlatGridPos.from_dict(_pos)

        _rect = d.pop("rect", UNSET)
        rect: CommonTypesGridRect | Unset
        if isinstance(_rect, Unset):
            rect = UNSET
        else:
            rect = CommonTypesGridRect.from_dict(_rect)

        relocate_greenhouse_object_body = cls(
            height=height,
            pos=pos,
            rect=rect,
        )

        relocate_greenhouse_object_body.additional_properties = d
        return relocate_greenhouse_object_body

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
