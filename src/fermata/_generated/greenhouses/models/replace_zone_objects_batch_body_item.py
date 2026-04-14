from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.models_zone_object_status import ModelsZoneObjectStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
    from ..models.common_types_ptz import CommonTypesPTZ


T = TypeVar("T", bound="ReplaceZoneObjectsBatchBodyItem")


@_attrs_define
class ReplaceZoneObjectsBatchBodyItem:
    """
    Attributes:
        id (UUID): UUID identifier
        organization_id (str): Organization identifier (opaque string)
        greenhouse_id (UUID): UUID identifier
        pos (CommonTypesFlatGridPos): Position on the flat greenhouse grid
        height (float): Height above the grid for this zone object
        ptz (CommonTypesPTZ): Pan-Tilt-Zoom camera position. Pan and tilt are in radians.
        device_id (UUID): UUID identifier
        status (ModelsZoneObjectStatus | Unset): Status of a zone object
    """

    id: UUID
    organization_id: str
    greenhouse_id: UUID
    pos: CommonTypesFlatGridPos
    height: float
    ptz: CommonTypesPTZ
    device_id: UUID
    status: ModelsZoneObjectStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = self.organization_id

        greenhouse_id = str(self.greenhouse_id)

        pos = self.pos.to_dict()

        height = self.height

        ptz = self.ptz.to_dict()

        device_id = str(self.device_id)

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organizationId": organization_id,
                "greenhouseId": greenhouse_id,
                "pos": pos,
                "height": height,
                "ptz": ptz,
                "deviceId": device_id,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_flat_grid_pos import CommonTypesFlatGridPos
        from ..models.common_types_ptz import CommonTypesPTZ

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        organization_id = d.pop("organizationId")

        greenhouse_id = UUID(d.pop("greenhouseId"))

        pos = CommonTypesFlatGridPos.from_dict(d.pop("pos"))

        height = d.pop("height")

        ptz = CommonTypesPTZ.from_dict(d.pop("ptz"))

        device_id = UUID(d.pop("deviceId"))

        _status = d.pop("status", UNSET)
        status: ModelsZoneObjectStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ModelsZoneObjectStatus(_status)

        replace_zone_objects_batch_body_item = cls(
            id=id,
            organization_id=organization_id,
            greenhouse_id=greenhouse_id,
            pos=pos,
            height=height,
            ptz=ptz,
            device_id=device_id,
            status=status,
        )

        replace_zone_objects_batch_body_item.additional_properties = d
        return replace_zone_objects_batch_body_item

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
