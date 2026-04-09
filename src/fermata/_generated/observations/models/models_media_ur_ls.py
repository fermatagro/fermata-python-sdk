from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelsMediaURLs")


@_attrs_define
class ModelsMediaURLs:
    """
    Attributes:
        media_url (str | Unset): Permanent URL to download the media (Authorization required)
        cdn_url (str | Unset): URL to download the media from CDN (CDN cookie required)
        thumbnail_url (str | Unset): URL to download the thumbnail media
    """

    media_url: str | Unset = UNSET
    cdn_url: str | Unset = UNSET
    thumbnail_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        media_url = self.media_url

        cdn_url = self.cdn_url

        thumbnail_url = self.thumbnail_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if media_url is not UNSET:
            field_dict["mediaUrl"] = media_url
        if cdn_url is not UNSET:
            field_dict["cdnUrl"] = cdn_url
        if thumbnail_url is not UNSET:
            field_dict["thumbnailUrl"] = thumbnail_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        media_url = d.pop("mediaUrl", UNSET)

        cdn_url = d.pop("cdnUrl", UNSET)

        thumbnail_url = d.pop("thumbnailUrl", UNSET)

        models_media_ur_ls = cls(
            media_url=media_url,
            cdn_url=cdn_url,
            thumbnail_url=thumbnail_url,
        )

        models_media_ur_ls.additional_properties = d
        return models_media_ur_ls

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
