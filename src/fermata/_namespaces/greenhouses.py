from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from fermata._transport import Transport

T = TypeVar("T", bound="Greenhouse")


@_attrs_define
class Greenhouse:
    """Greenhouse model.

    Attributes:
        id (str): Unique identifier
        organization_id (str): Organization that owns this greenhouse
        description (str): Human-readable name/description
        width (float): Width in meters
        height (float): Height in meters
        tz (str): IANA timezone identifier
    """

    id: str
    organization_id: str
    description: str
    width: float
    height: float
    tz: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": self.id,
                "organizationId": self.organization_id,
                "description": self.description,
                "width": self.width,
                "height": self.height,
                "tz": self.tz,
            }
        )
        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id_ = d.pop("id")
        organization_id = d.pop("organizationId")
        description = d.pop("description")
        width = d.pop("width")
        height = d.pop("height")
        tz = d.pop("tz")

        greenhouse = cls(
            id=id_,
            organization_id=organization_id,
            description=description,
            width=width,
            height=height,
            tz=tz,
        )
        greenhouse.additional_properties = d
        return greenhouse


class AsyncGreenhouses:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    async def list(self) -> list[Greenhouse]:
        resp = await self._t.request("GET", "/api/v1/greenhouses")
        body = resp.json()
        return [Greenhouse.from_dict(item) for item in body["items"]]
