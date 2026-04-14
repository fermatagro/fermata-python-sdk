from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.models_tile_face import ModelsTileFace
from ..models.models_tile_level import ModelsTileLevel
from uuid import UUID






T = TypeVar("T", bound="ModelsTileID")



@_attrs_define
class ModelsTileID:
    """ Identifier of a panorama tile

        Attributes:
            panorama_id (UUID): UUID identifier
            face (ModelsTileFace): Panorama tile face options
            level (ModelsTileLevel): Tile size options
            row (int): Row of the chosen tile
            column (int): Column of the chosen tile
     """

    panorama_id: UUID
    face: ModelsTileFace
    level: ModelsTileLevel
    row: int
    column: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        panorama_id = str(self.panorama_id)

        face = self.face.value

        level = self.level.value

        row = self.row

        column = self.column


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "panoramaId": panorama_id,
            "face": face,
            "level": level,
            "row": row,
            "column": column,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        panorama_id = UUID(d.pop("panoramaId"))




        face = ModelsTileFace(d.pop("face"))




        level = ModelsTileLevel(d.pop("level"))




        row = d.pop("row")

        column = d.pop("column")

        models_tile_id = cls(
            panorama_id=panorama_id,
            face=face,
            level=level,
            row=row,
            column=column,
        )


        models_tile_id.additional_properties = d
        return models_tile_id

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
