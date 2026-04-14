from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ModelsGreenhouse")


@_attrs_define
class ModelsGreenhouse:
    """A greenhouse structure within an organization

    Attributes:
        id (UUID): UUID identifier
        organization_id (str): Organization identifier (opaque string)
        description (str): Human-readable name/description
        width (float):
        height (float):
        tz (str): IANA timezone identifier (e.g., 'Europe/Moscow')
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: UUID
    organization_id: str
    description: str
    width: float
    height: float
    tz: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = self.organization_id

        description = self.description

        width = self.width

        height = self.height

        tz = self.tz

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organizationId": organization_id,
                "description": description,
                "width": width,
                "height": height,
                "tz": tz,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        organization_id = d.pop("organizationId")

        description = d.pop("description")

        width = d.pop("width")

        height = d.pop("height")

        tz = d.pop("tz")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        models_greenhouse = cls(
            id=id,
            organization_id=organization_id,
            description=description,
            width=width,
            height=height,
            tz=tz,
            created_at=created_at,
            updated_at=updated_at,
        )

        models_greenhouse.additional_properties = d
        return models_greenhouse

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
