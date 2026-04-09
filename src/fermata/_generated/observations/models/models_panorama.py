from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelsPanorama")


@_attrs_define
class ModelsPanorama:
    """360-degree panorama composed of multiple photos

    Attributes:
        id (UUID): UUID identifier
        organization_id (str): Organization identifier (opaque string)
        greenhouse_id (UUID): UUID identifier
        device_id (UUID): UUID identifier
        x (float): The X coordinate of the panorama
        y (float): The Y coordinate of the panorama
        height (float): The height at which the panorama was taken
        base_x (int): The base X grid coordinate
        base_y (int): The base Y grid coordinate
        base_url (str): The cdnUrl prefix for accessing panorama tiles
        captured_at (datetime.datetime): The timestamp when the panorama was captured
        created_at (datetime.datetime): The timestamp when the panorama was created
        pipeline_id (UUID | Unset): UUID identifier
        deleted_at (datetime.datetime | Unset): The timestamp when the panorama was soft-deleted
    """

    id: UUID
    organization_id: str
    greenhouse_id: UUID
    device_id: UUID
    x: float
    y: float
    height: float
    base_x: int
    base_y: int
    base_url: str
    captured_at: datetime.datetime
    created_at: datetime.datetime
    pipeline_id: UUID | Unset = UNSET
    deleted_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = self.organization_id

        greenhouse_id = str(self.greenhouse_id)

        device_id = str(self.device_id)

        x = self.x

        y = self.y

        height = self.height

        base_x = self.base_x

        base_y = self.base_y

        base_url = self.base_url

        captured_at = self.captured_at.isoformat()

        created_at = self.created_at.isoformat()

        pipeline_id: str | Unset = UNSET
        if not isinstance(self.pipeline_id, Unset):
            pipeline_id = str(self.pipeline_id)

        deleted_at: str | Unset = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organizationId": organization_id,
                "greenhouseId": greenhouse_id,
                "deviceId": device_id,
                "x": x,
                "y": y,
                "height": height,
                "baseX": base_x,
                "baseY": base_y,
                "baseUrl": base_url,
                "capturedAt": captured_at,
                "createdAt": created_at,
            }
        )
        if pipeline_id is not UNSET:
            field_dict["pipelineId"] = pipeline_id
        if deleted_at is not UNSET:
            field_dict["deletedAt"] = deleted_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        organization_id = d.pop("organizationId")

        greenhouse_id = UUID(d.pop("greenhouseId"))

        device_id = UUID(d.pop("deviceId"))

        x = d.pop("x")

        y = d.pop("y")

        height = d.pop("height")

        base_x = d.pop("baseX")

        base_y = d.pop("baseY")

        base_url = d.pop("baseUrl")

        captured_at = isoparse(d.pop("capturedAt"))

        created_at = isoparse(d.pop("createdAt"))

        _pipeline_id = d.pop("pipelineId", UNSET)
        pipeline_id: UUID | Unset
        if isinstance(_pipeline_id, Unset):
            pipeline_id = UNSET
        else:
            pipeline_id = UUID(_pipeline_id)

        _deleted_at = d.pop("deletedAt", UNSET)
        deleted_at: datetime.datetime | Unset
        if isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = isoparse(_deleted_at)

        models_panorama = cls(
            id=id,
            organization_id=organization_id,
            greenhouse_id=greenhouse_id,
            device_id=device_id,
            x=x,
            y=y,
            height=height,
            base_x=base_x,
            base_y=base_y,
            base_url=base_url,
            captured_at=captured_at,
            created_at=created_at,
            pipeline_id=pipeline_id,
            deleted_at=deleted_at,
        )

        models_panorama.additional_properties = d
        return models_panorama

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
