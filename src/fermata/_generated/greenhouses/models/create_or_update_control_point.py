from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.models_control_point_type import ModelsControlPointType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_grid_pos import CommonTypesGridPos
    from ..models.models_pan_tilt import ModelsPanTilt


T = TypeVar("T", bound="CreateOrUpdateControlPoint")


@_attrs_define
class CreateOrUpdateControlPoint:
    """
    Attributes:
        pos (CommonTypesGridPos): Position in 3D grid space within the greenhouse
        cam_pos (CommonTypesGridPos): Position in 3D grid space within the greenhouse
        pt (ModelsPanTilt): Pan-Tilt result from world coordinate transformation
        name (str | Unset): Human-readable label (e.g. 'Pillar 4', 'Palette R9')
        type_ (ModelsControlPointType | Unset): Type of control point
    """

    pos: CommonTypesGridPos
    cam_pos: CommonTypesGridPos
    pt: ModelsPanTilt
    name: str | Unset = UNSET
    type_: ModelsControlPointType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pos = self.pos.to_dict()

        cam_pos = self.cam_pos.to_dict()

        pt = self.pt.to_dict()

        name = self.name

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pos": pos,
                "camPos": cam_pos,
                "pt": pt,
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
        pos = CommonTypesGridPos.from_dict(d.pop("pos"))

        cam_pos = CommonTypesGridPos.from_dict(d.pop("camPos"))

        pt = ModelsPanTilt.from_dict(d.pop("pt"))

        name = d.pop("name", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: ModelsControlPointType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ModelsControlPointType(_type_)

        create_or_update_control_point = cls(
            pos=pos,
            cam_pos=cam_pos,
            pt=pt,
            name=name,
            type_=type_,
        )

        create_or_update_control_point.additional_properties = d
        return create_or_update_control_point

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
