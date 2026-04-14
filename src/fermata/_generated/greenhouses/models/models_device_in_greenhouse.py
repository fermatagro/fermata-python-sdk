from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.devices_models_device_type import DevicesModelsDeviceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
    from ..models.common_types_orientation_vector import CommonTypesOrientationVector


T = TypeVar("T", bound="ModelsDeviceInGreenhouse")


@_attrs_define
class ModelsDeviceInGreenhouse:
    """Device placement within a greenhouse

    Attributes:
        device_id (UUID): UUID identifier
        greenhouse_id (UUID): UUID identifier
        device_type (DevicesModelsDeviceType): Device type
        pos (CommonTypesFlatGridPos): Position on the flat greenhouse grid
        height (float):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        orientation_vector (CommonTypesOrientationVector | Unset): 3D orientation vector (radians)
        conversion_matrix (list[float] | Unset): 3x3 rotation matrix (row-major, 9 elements) for converting between
            camera and world coordinates. Calculated automatically from reference control points.
        coverage_radius (float | Unset): Maximum Euclidean distance from camera to its Zone Objects. Only for cameras
            with ZOs.
    """

    device_id: UUID
    greenhouse_id: UUID
    device_type: DevicesModelsDeviceType
    pos: CommonTypesFlatGridPos
    height: float
    created_at: datetime.datetime
    updated_at: datetime.datetime
    orientation_vector: CommonTypesOrientationVector | Unset = UNSET
    conversion_matrix: list[float] | Unset = UNSET
    coverage_radius: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        device_id = str(self.device_id)

        greenhouse_id = str(self.greenhouse_id)

        device_type = self.device_type.value

        pos = self.pos.to_dict()

        height = self.height

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        orientation_vector: dict[str, Any] | Unset = UNSET
        if not isinstance(self.orientation_vector, Unset):
            orientation_vector = self.orientation_vector.to_dict()

        conversion_matrix: list[float] | Unset = UNSET
        if not isinstance(self.conversion_matrix, Unset):
            conversion_matrix = self.conversion_matrix

        coverage_radius = self.coverage_radius

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deviceId": device_id,
                "greenhouseId": greenhouse_id,
                "deviceType": device_type,
                "pos": pos,
                "height": height,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if orientation_vector is not UNSET:
            field_dict["orientationVector"] = orientation_vector
        if conversion_matrix is not UNSET:
            field_dict["conversionMatrix"] = conversion_matrix
        if coverage_radius is not UNSET:
            field_dict["coverageRadius"] = coverage_radius

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
        from ..models.common_types_orientation_vector import CommonTypesOrientationVector

        d = dict(src_dict)
        device_id = UUID(d.pop("deviceId"))

        greenhouse_id = UUID(d.pop("greenhouseId"))

        device_type = DevicesModelsDeviceType(d.pop("deviceType"))

        pos = CommonTypesFlatGridPos.from_dict(d.pop("pos"))

        height = d.pop("height")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        _orientation_vector = d.pop("orientationVector", UNSET)
        orientation_vector: CommonTypesOrientationVector | Unset
        if isinstance(_orientation_vector, Unset):
            orientation_vector = UNSET
        else:
            orientation_vector = CommonTypesOrientationVector.from_dict(_orientation_vector)

        conversion_matrix = cast(list[float], d.pop("conversionMatrix", UNSET))

        coverage_radius = d.pop("coverageRadius", UNSET)

        models_device_in_greenhouse = cls(
            device_id=device_id,
            greenhouse_id=greenhouse_id,
            device_type=device_type,
            pos=pos,
            height=height,
            created_at=created_at,
            updated_at=updated_at,
            orientation_vector=orientation_vector,
            conversion_matrix=conversion_matrix,
            coverage_radius=coverage_radius,
        )

        models_device_in_greenhouse.additional_properties = d
        return models_device_in_greenhouse

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
