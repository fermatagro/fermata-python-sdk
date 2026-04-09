from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.models_tile_face import ModelsTileFace
from ..models.models_tile_level import ModelsTileLevel

T = TypeVar("T", bound="ModelsTile")


@_attrs_define
class ModelsTile:
    """Panorama tile metadata

    Attributes:
        panorama_id (UUID): UUID identifier
        face (ModelsTileFace): Panorama tile face options
        level (ModelsTileLevel): Tile size options
        row (int): Tile row
        column (int): Tile column
        created_at (datetime.datetime): Tile creation timestamp
    """

    panorama_id: UUID
    face: ModelsTileFace
    level: ModelsTileLevel
    row: int
    column: int
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        panorama_id = str(self.panorama_id)

        face = self.face.value

        level = self.level.value

        row = self.row

        column = self.column

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "panoramaId": panorama_id,
                "face": face,
                "level": level,
                "row": row,
                "column": column,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        panorama_id = UUID(d.pop("panoramaId"))

        face = ModelsTileFace(d.pop("face"))

        level = ModelsTileLevel(d.pop("level"))

        row = d.pop("row")

        column = d.pop("column")

        created_at = isoparse(d.pop("createdAt"))

        models_tile = cls(
            panorama_id=panorama_id,
            face=face,
            level=level,
            row=row,
            column=column,
            created_at=created_at,
        )

        models_tile.additional_properties = d
        return models_tile

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
