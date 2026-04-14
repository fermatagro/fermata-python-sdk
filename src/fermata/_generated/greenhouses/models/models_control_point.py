from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.models_control_point_type import ModelsControlPointType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_grid_pos import CommonTypesGridPos
    from ..models.models_pan_tilt import ModelsPanTilt


T = TypeVar("T", bound="ModelsControlPoint")


@_attrs_define
class ModelsControlPoint:
    """Reference point for camera calibration. Links a known world position to camera pan/tilt angles.

    Attributes:
        id (UUID): UUID identifier
        device_id (UUID): UUID identifier
        greenhouse_id (UUID): UUID identifier
        pos (CommonTypesGridPos): Position in 3D grid space within the greenhouse
        cam_pos (CommonTypesGridPos): Position in 3D grid space within the greenhouse
        pt (ModelsPanTilt): Pan-Tilt result from world coordinate transformation
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        name (str | Unset): Human-readable label (e.g. 'Pillar 4', 'Palette R9')
        type_ (ModelsControlPointType | Unset): Type of control point
    """

    id: UUID
    device_id: UUID
    greenhouse_id: UUID
    pos: CommonTypesGridPos
    cam_pos: CommonTypesGridPos
    pt: ModelsPanTilt
    created_at: datetime.datetime
    updated_at: datetime.datetime
    name: str | Unset = UNSET
    type_: ModelsControlPointType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        device_id = str(self.device_id)

        greenhouse_id = str(self.greenhouse_id)

        pos = self.pos.to_dict()

        cam_pos = self.cam_pos.to_dict()

        pt = self.pt.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        name = self.name

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "deviceId": device_id,
                "greenhouseId": greenhouse_id,
                "pos": pos,
                "camPos": cam_pos,
                "pt": pt,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_pos import CommonTypesGridPos
        from ..models.models_pan_tilt import ModelsPanTilt

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        device_id = UUID(d.pop("deviceId"))

        greenhouse_id = UUID(d.pop("greenhouseId"))

        pos = CommonTypesGridPos.from_dict(d.pop("pos"))

        cam_pos = CommonTypesGridPos.from_dict(d.pop("camPos"))

        pt = ModelsPanTilt.from_dict(d.pop("pt"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        name = d.pop("name", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: ModelsControlPointType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ModelsControlPointType(_type_)

        models_control_point = cls(
            id=id,
            device_id=device_id,
            greenhouse_id=greenhouse_id,
            pos=pos,
            cam_pos=cam_pos,
            pt=pt,
            created_at=created_at,
            updated_at=updated_at,
            name=name,
            type_=type_,
        )

        models_control_point.additional_properties = d
        return models_control_point

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
