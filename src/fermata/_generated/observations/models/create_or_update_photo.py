from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.devices_models_device_type import DevicesModelsDeviceType
from ..models.models_photo_source import ModelsPhotoSource
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.common_types_grid_pos import CommonTypesGridPos
  from ..models.create_or_update_photo_metadata import CreateOrUpdatePhotoMetadata





T = TypeVar("T", bound="CreateOrUpdatePhoto")



@_attrs_define
class CreateOrUpdatePhoto:
    """ 
        Attributes:
            id (UUID): UUID identifier
            greenhouse_id (UUID): UUID identifier
            culture_id (str):
            growing_cycle_id (UUID): UUID identifier
            captured_at (datetime.datetime):
            source (ModelsPhotoSource): Source of the photo capture
            pos (CommonTypesGridPos): Position in 3D grid space within the greenhouse
            ptz (list[float]): Camera pan/tilt/zoom settings. Array of 3 elements: [pan (radians, -π to π), tilt (radians, 0
                to π/2), zoom (level)]
            s_3_key (str | Unset): S3 key for the photo. Auto-generated if not provided. Use for migrating existing photos.
            device_id (UUID | Unset): UUID identifier
            device_type (DevicesModelsDeviceType | Unset): Device type
            zone_object_id (UUID | Unset): UUID identifier
            pipeline_id (UUID | Unset): UUID identifier
            metadata (CreateOrUpdatePhotoMetadata | Unset): Additional metadata (resolution, format, etc.)
     """

    id: UUID
    greenhouse_id: UUID
    culture_id: str
    growing_cycle_id: UUID
    captured_at: datetime.datetime
    source: ModelsPhotoSource
    pos: CommonTypesGridPos
    ptz: list[float]
    s_3_key: str | Unset = UNSET
    device_id: UUID | Unset = UNSET
    device_type: DevicesModelsDeviceType | Unset = UNSET
    zone_object_id: UUID | Unset = UNSET
    pipeline_id: UUID | Unset = UNSET
    metadata: CreateOrUpdatePhotoMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.common_types_grid_pos import CommonTypesGridPos
        from ..models.create_or_update_photo_metadata import CreateOrUpdatePhotoMetadata
        id = str(self.id)

        greenhouse_id = str(self.greenhouse_id)

        culture_id = self.culture_id

        growing_cycle_id = str(self.growing_cycle_id)

        captured_at = self.captured_at.isoformat()

        source = self.source.value

        pos = self.pos.to_dict()

        ptz = self.ptz



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
        field_dict.update({
            "id": id,
            "greenhouseId": greenhouse_id,
            "cultureId": culture_id,
            "growingCycleId": growing_cycle_id,
            "capturedAt": captured_at,
            "source": source,
            "pos": pos,
            "ptz": ptz,
        })
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
        from ..models.create_or_update_photo_metadata import CreateOrUpdatePhotoMetadata
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        greenhouse_id = UUID(d.pop("greenhouseId"))




        culture_id = d.pop("cultureId")

        growing_cycle_id = UUID(d.pop("growingCycleId"))




        captured_at = isoparse(d.pop("capturedAt"))




        source = ModelsPhotoSource(d.pop("source"))




        pos = CommonTypesGridPos.from_dict(d.pop("pos"))




        ptz = cast(list[float], d.pop("ptz"))


        s_3_key = d.pop("s3Key", UNSET)

        _device_id = d.pop("deviceId", UNSET)
        device_id: UUID | Unset
        if isinstance(_device_id,  Unset):
            device_id = UNSET
        else:
            device_id = UUID(_device_id)




        _device_type = d.pop("deviceType", UNSET)
        device_type: DevicesModelsDeviceType | Unset
        if isinstance(_device_type,  Unset):
            device_type = UNSET
        else:
            device_type = DevicesModelsDeviceType(_device_type)




        _zone_object_id = d.pop("zoneObjectId", UNSET)
        zone_object_id: UUID | Unset
        if isinstance(_zone_object_id,  Unset):
            zone_object_id = UNSET
        else:
            zone_object_id = UUID(_zone_object_id)




        _pipeline_id = d.pop("pipelineId", UNSET)
        pipeline_id: UUID | Unset
        if isinstance(_pipeline_id,  Unset):
            pipeline_id = UNSET
        else:
            pipeline_id = UUID(_pipeline_id)




        _metadata = d.pop("metadata", UNSET)
        metadata: CreateOrUpdatePhotoMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = CreateOrUpdatePhotoMetadata.from_dict(_metadata)




        create_or_update_photo = cls(
            id=id,
            greenhouse_id=greenhouse_id,
            culture_id=culture_id,
            growing_cycle_id=growing_cycle_id,
            captured_at=captured_at,
            source=source,
            pos=pos,
            ptz=ptz,
            s_3_key=s_3_key,
            device_id=device_id,
            device_type=device_type,
            zone_object_id=zone_object_id,
            pipeline_id=pipeline_id,
            metadata=metadata,
        )


        create_or_update_photo.additional_properties = d
        return create_or_update_photo

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
