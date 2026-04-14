from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.common_types_grid_rect import CommonTypesGridRect


T = TypeVar("T", bound="ModelsNote")


@_attrs_define
class ModelsNote:
    """A note attached to a location in a growing cycle

    Attributes:
        id (UUID): UUID identifier
        organization_id (str): Organization identifier (opaque string)
        growing_cycle_id (UUID): UUID identifier
        author_id (str): User identifier (opaque string)
        text (str):
        rect (CommonTypesGridRect): Rectangular area on the greenhouse grid
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: UUID
    organization_id: str
    growing_cycle_id: UUID
    author_id: str
    text: str
    rect: CommonTypesGridRect
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = self.organization_id

        growing_cycle_id = str(self.growing_cycle_id)

        author_id = self.author_id

        text = self.text

        rect = self.rect.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organizationId": organization_id,
                "growingCycleId": growing_cycle_id,
                "authorId": author_id,
                "text": text,
                "rect": rect,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_rect import CommonTypesGridRect

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        organization_id = d.pop("organizationId")

        growing_cycle_id = UUID(d.pop("growingCycleId"))

        author_id = d.pop("authorId")

        text = d.pop("text")

        rect = CommonTypesGridRect.from_dict(d.pop("rect"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        models_note = cls(
            id=id,
            organization_id=organization_id,
            growing_cycle_id=growing_cycle_id,
            author_id=author_id,
            text=text,
            rect=rect,
            created_at=created_at,
            updated_at=updated_at,
        )

        models_note.additional_properties = d
        return models_note

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
