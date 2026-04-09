from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_grid_pos import CommonTypesGridPos
    from ..models.common_types_time_range import CommonTypesTimeRange


T = TypeVar("T", bound="ModelsPredictionQuery")


@_attrs_define
class ModelsPredictionQuery:
    """Query parameters for filtering predictions

    Attributes:
        range_ (CommonTypesTimeRange): Time range with start and end timestamps
        greenhouse_id (UUID | Unset): UUID identifier
        pos (CommonTypesGridPos | Unset): Position in 3D grid space within the greenhouse
        class_id (str | Unset): Class identifier from ML API (class name)
    """

    range_: CommonTypesTimeRange
    greenhouse_id: UUID | Unset = UNSET
    pos: CommonTypesGridPos | Unset = UNSET
    class_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        range_ = self.range_.to_dict()

        greenhouse_id: str | Unset = UNSET
        if not isinstance(self.greenhouse_id, Unset):
            greenhouse_id = str(self.greenhouse_id)

        pos: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pos, Unset):
            pos = self.pos.to_dict()

        class_id = self.class_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "range": range_,
            }
        )
        if greenhouse_id is not UNSET:
            field_dict["greenhouseId"] = greenhouse_id
        if pos is not UNSET:
            field_dict["pos"] = pos
        if class_id is not UNSET:
            field_dict["classId"] = class_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_pos import CommonTypesGridPos
        from ..models.common_types_time_range import CommonTypesTimeRange

        d = dict(src_dict)
        range_ = CommonTypesTimeRange.from_dict(d.pop("range"))

        _greenhouse_id = d.pop("greenhouseId", UNSET)
        greenhouse_id: UUID | Unset
        if isinstance(_greenhouse_id, Unset):
            greenhouse_id = UNSET
        else:
            greenhouse_id = UUID(_greenhouse_id)

        _pos = d.pop("pos", UNSET)
        pos: CommonTypesGridPos | Unset
        if isinstance(_pos, Unset):
            pos = UNSET
        else:
            pos = CommonTypesGridPos.from_dict(_pos)

        class_id = d.pop("classId", UNSET)

        models_prediction_query = cls(
            range_=range_,
            greenhouse_id=greenhouse_id,
            pos=pos,
            class_id=class_id,
        )

        models_prediction_query.additional_properties = d
        return models_prediction_query

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
