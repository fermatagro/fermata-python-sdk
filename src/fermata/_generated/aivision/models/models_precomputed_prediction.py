from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_grid_rect import CommonTypesGridRect


T = TypeVar("T", bound="ModelsPrecomputedPrediction")


@_attrs_define
class ModelsPrecomputedPrediction:
    """A single pre-computed prediction from an external model

    Attributes:
        class_id (str | Unset): Detection class name from the external model
        confidence (float | Unset): Confidence score (0-1)
        bbox (CommonTypesGridRect | Unset): Rectangular area on the greenhouse grid
    """

    class_id: str | Unset = UNSET
    confidence: float | Unset = UNSET
    bbox: CommonTypesGridRect | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        class_id = self.class_id

        confidence = self.confidence

        bbox: dict[str, Any] | Unset = UNSET
        if not isinstance(self.bbox, Unset):
            bbox = self.bbox.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if class_id is not UNSET:
            field_dict["classId"] = class_id
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if bbox is not UNSET:
            field_dict["bbox"] = bbox

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_rect import CommonTypesGridRect

        d = dict(src_dict)
        class_id = d.pop("classId", UNSET)

        confidence = d.pop("confidence", UNSET)

        _bbox = d.pop("bbox", UNSET)
        bbox: CommonTypesGridRect | Unset
        if isinstance(_bbox, Unset):
            bbox = UNSET
        else:
            bbox = CommonTypesGridRect.from_dict(_bbox)

        models_precomputed_prediction = cls(
            class_id=class_id,
            confidence=confidence,
            bbox=bbox,
        )

        models_precomputed_prediction.additional_properties = d
        return models_precomputed_prediction

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
