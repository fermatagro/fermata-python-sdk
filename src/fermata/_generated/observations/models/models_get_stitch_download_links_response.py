from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.models_get_stitch_download_links_response_download_urls import (
        ModelsGetStitchDownloadLinksResponseDownloadUrls,
    )


T = TypeVar("T", bound="ModelsGetStitchDownloadLinksResponse")


@_attrs_define
class ModelsGetStitchDownloadLinksResponse:
    """Response with presigned download URLs for all raw panorama input images (72 total)

    Attributes:
        download_urls (ModelsGetStitchDownloadLinksResponseDownloadUrls): Map of level_index to presigned download URL.
            Keys: '0_0', '0_1', ..., '7_1'
        expires_at (datetime.datetime): When the presigned URLs expire
    """

    download_urls: ModelsGetStitchDownloadLinksResponseDownloadUrls
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        download_urls = self.download_urls.to_dict()

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "downloadUrls": download_urls,
                "expiresAt": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_get_stitch_download_links_response_download_urls import (
            ModelsGetStitchDownloadLinksResponseDownloadUrls,
        )

        d = dict(src_dict)
        download_urls = ModelsGetStitchDownloadLinksResponseDownloadUrls.from_dict(d.pop("downloadUrls"))

        expires_at = isoparse(d.pop("expiresAt"))

        models_get_stitch_download_links_response = cls(
            download_urls=download_urls,
            expires_at=expires_at,
        )

        models_get_stitch_download_links_response.additional_properties = d
        return models_get_stitch_download_links_response

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
