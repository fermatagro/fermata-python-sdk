from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.devices_models_device_type import DevicesModelsDeviceType
from ..models.models_photo_source import ModelsPhotoSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_grid_pos import CommonTypesGridPos
    from ..models.models_photo_metadata import ModelsPhotoMetadata


T = TypeVar("T", bound="ModelsPhoto")


@_attrs_define
class ModelsPhoto:
    """A photograph captured in the greenhouse

    Attributes:
        id (UUID): UUID identifier
        user_id (str): User identifier (opaque string)
        greenhouse_id (UUID): UUID identifier
        culture_id (str):
        growing_cycle_id (UUID): UUID identifier
        captured_at (datetime.datetime):
        source (ModelsPhotoSource): Source of the photo capture
        pos (CommonTypesGridPos): Position in 3D grid space within the greenhouse
        ptz (list[float]): Camera pan/tilt/zoom settings. Array of 3 elements: [pan (radians, -π to π), tilt (radians, 0
            to π/2), zoom (level)]
        created_at (datetime.datetime):
        media_url (str | Unset): Permanent URL to download the media (Authorization required)
        cdn_url (str | Unset): URL to download the media from CDN (CDN cookie required)
        thumbnail_url (str | Unset): URL to download the thumbnail media
        organization_id (str | Unset): Organization identifier (opaque string)
        s_3_key (str | Unset): S3 key for the photo. Auto-generated if not provided. Use for migrating existing photos.
        device_id (UUID | Unset): UUID identifier
        device_type (DevicesModelsDeviceType | Unset): Device type
        zone_object_id (UUID | Unset): UUID identifier
        pipeline_id (UUID | Unset): UUID identifier
        metadata (ModelsPhotoMetadata | Unset): Additional metadata (resolution, format, etc.)
    """

    id: UUID
    user_id: str
    greenhouse_id: UUID
    culture_id: str
    growing_cycle_id: UUID
    captured_at: datetime.datetime
    source: ModelsPhotoSource
    pos: CommonTypesGridPos
    ptz: list[float]
    created_at: datetime.datetime
    media_url: str | Unset = UNSET
    cdn_url: str | Unset = UNSET
    thumbnail_url: str | Unset = UNSET
    organization_id: str | Unset = UNSET
    s_3_key: str | Unset = UNSET
    device_id: UUID | Unset = UNSET
    device_type: DevicesModelsDeviceType | Unset = UNSET
    zone_object_id: UUID | Unset = UNSET
    pipeline_id: UUID | Unset = UNSET
    metadata: ModelsPhotoMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        user_id = self.user_id

        greenhouse_id = str(self.greenhouse_id)

        culture_id = self.culture_id

        growing_cycle_id = str(self.growing_cycle_id)

        captured_at = self.captured_at.isoformat()

        source = self.source.value

        pos = self.pos.to_dict()

        ptz = self.ptz

        created_at = self.created_at.isoformat()

        media_url = self.media_url

        cdn_url = self.cdn_url

        thumbnail_url = self.thumbnail_url

        organization_id = self.organization_id

        s_3_key = self.s_3_key

        device_id: str | Unset = UNSET
        if not isinstance(self.device_id, Unset):
            device_id = str(self.device_id)

        device_type: str | Unset = UNSET
        if not isinstance(self.device_type, Unset):
            device_type = self.device_type.value

        zone_object_id: str | Unset = UNSET
        if not isinstance(self.zone_object_id, Unset):
            zone_object_id = str(self.zone_object_id)

        pipeline_id: str | Unset = UNSET
        if not isinstance(self.pipeline_id, Unset):
            pipeline_id = str(self.pipeline_id)

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "userId": user_id,
                "greenhouseId": greenhouse_id,
                "cultureId": culture_id,
                "growingCycleId": growing_cycle_id,
                "capturedAt": captured_at,
                "source": source,
                "pos": pos,
                "ptz": ptz,
                "createdAt": created_at,
            }
        )
        if media_url is not UNSET:
            field_dict["mediaUrl"] = media_url
        if cdn_url is not UNSET:
            field_dict["cdnUrl"] = cdn_url
        if thumbnail_url is not UNSET:
            field_dict["thumbnailUrl"] = thumbnail_url
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if s_3_key is not UNSET:
            field_dict["s3Key"] = s_3_key
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if device_type is not UNSET:
            field_dict["deviceType"] = device_type
        if zone_object_id is not UNSET:
            field_dict["zoneObjectId"] = zone_object_id
        if pipeline_id is not UNSET:
            field_dict["pipelineId"] = pipeline_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_pos import CommonTypesGridPos
        from ..models.models_photo_metadata import ModelsPhotoMetadata

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        user_id = d.pop("userId")

        greenhouse_id = UUID(d.pop("greenhouseId"))

        culture_id = d.pop("cultureId")

        growing_cycle_id = UUID(d.pop("growingCycleId"))

        captured_at = isoparse(d.pop("capturedAt"))

        source = ModelsPhotoSource(d.pop("source"))

        pos = CommonTypesGridPos.from_dict(d.pop("pos"))

        ptz = cast(list[float], d.pop("ptz"))

        created_at = isoparse(d.pop("createdAt"))

        media_url = d.pop("mediaUrl", UNSET)

        cdn_url = d.pop("cdnUrl", UNSET)

        thumbnail_url = d.pop("thumbnailUrl", UNSET)

        organization_id = d.pop("organizationId", UNSET)

        s_3_key = d.pop("s3Key", UNSET)

        _device_id = d.pop("deviceId", UNSET)
        device_id: UUID | Unset
        if isinstance(_device_id, Unset):
            device_id = UNSET
        else:
            device_id = UUID(_device_id)

        _device_type = d.pop("deviceType", UNSET)
        device_type: DevicesModelsDeviceType | Unset
        if isinstance(_device_type, Unset):
            device_type = UNSET
        else:
            device_type = DevicesModelsDeviceType(_device_type)

        _zone_object_id = d.pop("zoneObjectId", UNSET)
        zone_object_id: UUID | Unset
        if isinstance(_zone_object_id, Unset):
            zone_object_id = UNSET
        else:
            zone_object_id = UUID(_zone_object_id)

        _pipeline_id = d.pop("pipelineId", UNSET)
        pipeline_id: UUID | Unset
        if isinstance(_pipeline_id, Unset):
            pipeline_id = UNSET
        else:
            pipeline_id = UUID(_pipeline_id)

        _metadata = d.pop("metadata", UNSET)
        metadata: ModelsPhotoMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ModelsPhotoMetadata.from_dict(_metadata)

        models_photo = cls(
            id=id,
            user_id=user_id,
            greenhouse_id=greenhouse_id,
            culture_id=culture_id,
            growing_cycle_id=growing_cycle_id,
            captured_at=captured_at,
            source=source,
            pos=pos,
            ptz=ptz,
            created_at=created_at,
            media_url=media_url,
            cdn_url=cdn_url,
            thumbnail_url=thumbnail_url,
            organization_id=organization_id,
            s_3_key=s_3_key,
            device_id=device_id,
            device_type=device_type,
            zone_object_id=zone_object_id,
            pipeline_id=pipeline_id,
            metadata=metadata,
        )

        models_photo.additional_properties = d
        return models_photo

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
