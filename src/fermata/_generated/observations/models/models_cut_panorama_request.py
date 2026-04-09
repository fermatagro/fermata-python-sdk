from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ModelsCutPanoramaRequest")


@_attrs_define
class ModelsCutPanoramaRequest:
    """Request to submit a cut-only tile generation job for an existing panorama

    Attributes:
        panorama_id (UUID): UUID identifier
    """

    panorama_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        panorama_id = str(self.panorama_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "panoramaId": panorama_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        panorama_id = UUID(d.pop("panoramaId"))

        models_cut_panorama_request = cls(
            panorama_id=panorama_id,
        )

        models_cut_panorama_request.additional_properties = d
        return models_cut_panorama_request

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
