from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateOrUpdateGreenhouse")


@_attrs_define
class CreateOrUpdateGreenhouse:
    """
    Attributes:
        description (str): Human-readable name/description
        width (float):
        height (float):
        tz (str): IANA timezone identifier (e.g., 'Europe/Moscow')
    """

    description: str
    width: float
    height: float
    tz: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        width = self.width

        height = self.height

        tz = self.tz

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "width": width,
                "height": height,
                "tz": tz,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        width = d.pop("width")

        height = d.pop("height")

        tz = d.pop("tz")

        create_or_update_greenhouse = cls(
            description=description,
            width=width,
            height=height,
            tz=tz,
        )

        create_or_update_greenhouse.additional_properties = d
        return create_or_update_greenhouse

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
