from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="ModelsGetStitchDownloadLinksRequest")



@_attrs_define
class ModelsGetStitchDownloadLinksRequest:
    """ Request for download links for all raw panorama input images

        Attributes:
            fire_id (UUID): UUID identifier
            device_id (UUID): UUID identifier
     """

    fire_id: UUID
    device_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        fire_id = str(self.fire_id)

        device_id = str(self.device_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fireId": fire_id,
            "deviceId": device_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fire_id = UUID(d.pop("fireId"))




        device_id = UUID(d.pop("deviceId"))




        models_get_stitch_download_links_request = cls(
            fire_id=fire_id,
            device_id=device_id,
        )


        models_get_stitch_download_links_request.additional_properties = d
        return models_get_stitch_download_links_request

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
