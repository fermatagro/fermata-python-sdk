from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ModelsGetRawCaptureUploadLinkResponse")


@_attrs_define
class ModelsGetRawCaptureUploadLinkResponse:
    """Response with single presigned upload URL for raw capture

    Attributes:
        upload_url (str): Presigned S3 URL for direct upload
        expires_at (datetime.datetime): When the presigned URL expires
    """

    upload_url: str
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        upload_url = self.upload_url

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uploadUrl": upload_url,
                "expiresAt": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        upload_url = d.pop("uploadUrl")

        expires_at = isoparse(d.pop("expiresAt"))

        models_get_raw_capture_upload_link_response = cls(
            upload_url=upload_url,
            expires_at=expires_at,
        )

        models_get_raw_capture_upload_link_response.additional_properties = d
        return models_get_raw_capture_upload_link_response

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
