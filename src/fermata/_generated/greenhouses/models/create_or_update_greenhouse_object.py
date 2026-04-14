from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.models_greenhouse_object_type import ModelsGreenhouseObjectType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
    from ..models.common_types_grid_rect import CommonTypesGridRect


T = TypeVar("T", bound="CreateOrUpdateGreenhouseObject")


@_attrs_define
class CreateOrUpdateGreenhouseObject:
    """
    Attributes:
        kind (ModelsGreenhouseObjectType): Type of object within a greenhouse
        description (str | Unset):
        pos (CommonTypesFlatGridPos | Unset): Position on the flat greenhouse grid
        height (float | Unset):
        rect (CommonTypesGridRect | Unset): Rectangular area on the greenhouse grid
    """

    kind: ModelsGreenhouseObjectType
    description: str | Unset = UNSET
    pos: CommonTypesFlatGridPos | Unset = UNSET
    height: float | Unset = UNSET
    rect: CommonTypesGridRect | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        description = self.description

        pos: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pos, Unset):
            pos = self.pos.to_dict()

        height = self.height

        rect: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rect, Unset):
            rect = self.rect.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if pos is not UNSET:
            field_dict["pos"] = pos
        if height is not UNSET:
            field_dict["height"] = height
        if rect is not UNSET:
            field_dict["rect"] = rect

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
        from ..models.common_types_grid_rect import CommonTypesGridRect

        d = dict(src_dict)
        kind = ModelsGreenhouseObjectType(d.pop("kind"))

        description = d.pop("description", UNSET)

        _pos = d.pop("pos", UNSET)
        pos: CommonTypesFlatGridPos | Unset
        if isinstance(_pos, Unset):
            pos = UNSET
        else:
            pos = CommonTypesFlatGridPos.from_dict(_pos)

        height = d.pop("height", UNSET)

        _rect = d.pop("rect", UNSET)
        rect: CommonTypesGridRect | Unset
        if isinstance(_rect, Unset):
            rect = UNSET
        else:
            rect = CommonTypesGridRect.from_dict(_rect)

        create_or_update_greenhouse_object = cls(
            kind=kind,
            description=description,
            pos=pos,
            height=height,
            rect=rect,
        )

        create_or_update_greenhouse_object.additional_properties = d
        return create_or_update_greenhouse_object

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
