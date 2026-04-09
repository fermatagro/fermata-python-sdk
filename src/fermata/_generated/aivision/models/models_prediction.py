from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.common_types_grid_pos import CommonTypesGridPos
    from ..models.common_types_grid_rect import CommonTypesGridRect
    from ..models.common_types_ptz import CommonTypesPTZ
    from ..models.models_vertex import ModelsVertex


T = TypeVar("T", bound="ModelsPrediction")


@_attrs_define
class ModelsPrediction:
    """
    Attributes:
        id (UUID): UUID identifier
        greenhouse_id (UUID): UUID identifier
        photo_id (UUID): UUID identifier
        model_name (str):
        model_threshold (float | None):
        culture_id (str):
        captured_at (datetime.datetime):
        predicted_at (datetime.datetime):
        planting_date (datetime.datetime):
        pos (CommonTypesGridPos | Unset): Position in 3D grid space within the greenhouse
        ptz (CommonTypesPTZ | Unset): Pan-Tilt-Zoom camera position. Pan and tilt are in radians.
        class_id (str | Unset): Class identifier from ML API (class name)
        confidence (float | Unset):
        bbox (CommonTypesGridRect | Unset): Rectangular area on the greenhouse grid
        polygon (list[ModelsVertex] | Unset):
        hidden (bool | Unset): Whether the prediction is hidden from normal view
    """

    id: UUID
    greenhouse_id: UUID
    photo_id: UUID
    model_name: str
    model_threshold: float | None
    culture_id: str
    captured_at: datetime.datetime
    predicted_at: datetime.datetime
    planting_date: datetime.datetime
    pos: CommonTypesGridPos | Unset = UNSET
    ptz: CommonTypesPTZ | Unset = UNSET
    class_id: str | Unset = UNSET
    confidence: float | Unset = UNSET
    bbox: CommonTypesGridRect | Unset = UNSET
    polygon: list[ModelsVertex] | Unset = UNSET
    hidden: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        greenhouse_id = str(self.greenhouse_id)

        photo_id = str(self.photo_id)

        model_name = self.model_name

        model_threshold: float | None
        model_threshold = self.model_threshold

        culture_id = self.culture_id

        captured_at = self.captured_at.isoformat()

        predicted_at = self.predicted_at.isoformat()

        planting_date = self.planting_date.isoformat()

        pos: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pos, Unset):
            pos = self.pos.to_dict()

        ptz: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ptz, Unset):
            ptz = self.ptz.to_dict()

        class_id = self.class_id

        confidence = self.confidence

        bbox: dict[str, Any] | Unset = UNSET
        if not isinstance(self.bbox, Unset):
            bbox = self.bbox.to_dict()

        polygon: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.polygon, Unset):
            polygon = []
            for polygon_item_data in self.polygon:
                polygon_item = polygon_item_data.to_dict()
                polygon.append(polygon_item)

        hidden = self.hidden

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "greenhouseId": greenhouse_id,
                "photoId": photo_id,
                "modelName": model_name,
                "modelThreshold": model_threshold,
                "cultureId": culture_id,
                "capturedAt": captured_at,
                "predictedAt": predicted_at,
                "plantingDate": planting_date,
            }
        )
        if pos is not UNSET:
            field_dict["pos"] = pos
        if ptz is not UNSET:
            field_dict["ptz"] = ptz
        if class_id is not UNSET:
            field_dict["classId"] = class_id
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if bbox is not UNSET:
            field_dict["bbox"] = bbox
        if polygon is not UNSET:
            field_dict["polygon"] = polygon
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_pos import CommonTypesGridPos
        from ..models.common_types_grid_rect import CommonTypesGridRect
        from ..models.common_types_ptz import CommonTypesPTZ
        from ..models.models_vertex import ModelsVertex

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        greenhouse_id = UUID(d.pop("greenhouseId"))

        photo_id = UUID(d.pop("photoId"))

        model_name = d.pop("modelName")

        def _parse_model_threshold(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        model_threshold = _parse_model_threshold(d.pop("modelThreshold"))

        culture_id = d.pop("cultureId")

        captured_at = isoparse(d.pop("capturedAt"))

        predicted_at = isoparse(d.pop("predictedAt"))

        planting_date = isoparse(d.pop("plantingDate"))

        _pos = d.pop("pos", UNSET)
        pos: CommonTypesGridPos | Unset
        if isinstance(_pos, Unset):
            pos = UNSET
        else:
            pos = CommonTypesGridPos.from_dict(_pos)

        _ptz = d.pop("ptz", UNSET)
        ptz: CommonTypesPTZ | Unset
        if isinstance(_ptz, Unset):
            ptz = UNSET
        else:
            ptz = CommonTypesPTZ.from_dict(_ptz)

        class_id = d.pop("classId", UNSET)

        confidence = d.pop("confidence", UNSET)

        _bbox = d.pop("bbox", UNSET)
        bbox: CommonTypesGridRect | Unset
        if isinstance(_bbox, Unset):
            bbox = UNSET
        else:
            bbox = CommonTypesGridRect.from_dict(_bbox)

        _polygon = d.pop("polygon", UNSET)
        polygon: list[ModelsVertex] | Unset = UNSET
        if _polygon is not UNSET:
            polygon = []
            for polygon_item_data in _polygon:
                polygon_item = ModelsVertex.from_dict(polygon_item_data)

                polygon.append(polygon_item)

        hidden = d.pop("hidden", UNSET)

        models_prediction = cls(
            id=id,
            greenhouse_id=greenhouse_id,
            photo_id=photo_id,
            model_name=model_name,
            model_threshold=model_threshold,
            culture_id=culture_id,
            captured_at=captured_at,
            predicted_at=predicted_at,
            planting_date=planting_date,
            pos=pos,
            ptz=ptz,
            class_id=class_id,
            confidence=confidence,
            bbox=bbox,
            polygon=polygon,
            hidden=hidden,
        )

        models_prediction.additional_properties = d
        return models_prediction

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
