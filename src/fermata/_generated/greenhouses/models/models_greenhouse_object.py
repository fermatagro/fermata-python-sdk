from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.models_greenhouse_object_type import ModelsGreenhouseObjectType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
    from ..models.common_types_grid_rect import CommonTypesGridRect


T = TypeVar("T", bound="ModelsGreenhouseObject")


@_attrs_define
class ModelsGreenhouseObject:
    """Physical object (row, block) within a greenhouse

    Attributes:
        id (int):
        greenhouse_id (UUID): UUID identifier
        kind (ModelsGreenhouseObjectType): Type of object within a greenhouse
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        description (str | Unset):
        pos (CommonTypesFlatGridPos | Unset): Position on the flat greenhouse grid
        height (float | Unset):
        rect (CommonTypesGridRect | Unset): Rectangular area on the greenhouse grid
    """

    id: int
    greenhouse_id: UUID
    kind: ModelsGreenhouseObjectType
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: str | Unset = UNSET
    pos: CommonTypesFlatGridPos | Unset = UNSET
    height: float | Unset = UNSET
    rect: CommonTypesGridRect | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        greenhouse_id = str(self.greenhouse_id)

        kind = self.kind.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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
                "id": id,
                "greenhouseId": greenhouse_id,
                "kind": kind,
                "createdAt": created_at,
                "updatedAt": updated_at,
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
        id = d.pop("id")

        greenhouse_id = UUID(d.pop("greenhouseId"))

        kind = ModelsGreenhouseObjectType(d.pop("kind"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

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

        models_greenhouse_object = cls(
            id=id,
            greenhouse_id=greenhouse_id,
            kind=kind,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
            pos=pos,
            height=height,
            rect=rect,
        )

        models_greenhouse_object.additional_properties = d
        return models_greenhouse_object

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
