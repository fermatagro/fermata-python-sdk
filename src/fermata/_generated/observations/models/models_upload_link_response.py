from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ModelsUploadLinkResponse")


@_attrs_define
class ModelsUploadLinkResponse:
    """Response with presigned upload URL

    Attributes:
        photo_id (UUID): UUID identifier
        upload_url (str): Presigned S3 URL for direct upload (PUT)
        download_url (str): Presigned S3 URL for direct download (GET) - use for preview before metadata is created
        delete_url (str): Presigned S3 URL for direct delete (DELETE) - use to cleanup orphan files on retake/cancel
        expires_at (datetime.datetime): When the presigned URL expires
    """

    photo_id: UUID
    upload_url: str
    download_url: str
    delete_url: str
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        photo_id = str(self.photo_id)

        upload_url = self.upload_url

        download_url = self.download_url

        delete_url = self.delete_url

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "photoId": photo_id,
                "uploadUrl": upload_url,
                "downloadUrl": download_url,
                "deleteUrl": delete_url,
                "expiresAt": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        photo_id = UUID(d.pop("photoId"))

        upload_url = d.pop("uploadUrl")

        download_url = d.pop("downloadUrl")

        delete_url = d.pop("deleteUrl")

        expires_at = isoparse(d.pop("expiresAt"))

        models_upload_link_response = cls(
            photo_id=photo_id,
            upload_url=upload_url,
            download_url=download_url,
            delete_url=delete_url,
            expires_at=expires_at,
        )

        models_upload_link_response.additional_properties = d
        return models_upload_link_response

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
