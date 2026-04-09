from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ModelsSubmitPanoramaStitchRequest")


@_attrs_define
class ModelsSubmitPanoramaStitchRequest:
    """Request to submit a panorama stitching task

    Attributes:
        fire_id (UUID): UUID identifier
        greenhouse_id (UUID): UUID identifier
        device_id (UUID): UUID identifier
        captured_at (datetime.datetime): When the base images were captured
        x (float): The X coordinate of the camera position
        y (float): The Y coordinate of the camera position
        height (float): The height of the camera
        pts_template (str): PTGui template name to use for stitching
    """

    fire_id: UUID
    greenhouse_id: UUID
    device_id: UUID
    captured_at: datetime.datetime
    x: float
    y: float
    height: float
    pts_template: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fire_id = str(self.fire_id)

        greenhouse_id = str(self.greenhouse_id)

        device_id = str(self.device_id)

        captured_at = self.captured_at.isoformat()

        x = self.x

        y = self.y

        height = self.height

        pts_template = self.pts_template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fireId": fire_id,
                "greenhouseId": greenhouse_id,
                "deviceId": device_id,
                "capturedAt": captured_at,
                "x": x,
                "y": y,
                "height": height,
                "ptsTemplate": pts_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fire_id = UUID(d.pop("fireId"))

        greenhouse_id = UUID(d.pop("greenhouseId"))

        device_id = UUID(d.pop("deviceId"))

        captured_at = isoparse(d.pop("capturedAt"))

        x = d.pop("x")

        y = d.pop("y")

        height = d.pop("height")

        pts_template = d.pop("ptsTemplate")

        models_submit_panorama_stitch_request = cls(
            fire_id=fire_id,
            greenhouse_id=greenhouse_id,
            device_id=device_id,
            captured_at=captured_at,
            x=x,
            y=y,
            height=height,
            pts_template=pts_template,
        )

        models_submit_panorama_stitch_request.additional_properties = d
        return models_submit_panorama_stitch_request

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
