from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.models_precomputed_prediction import ModelsPrecomputedPrediction


T = TypeVar("T", bound="ModelsUploadPredictionsRequest")


@_attrs_define
class ModelsUploadPredictionsRequest:
    """Request to upload pre-computed predictions for a photo

    Attributes:
        photo_id (UUID): UUID identifier
        model_name (str): ML model name that produced the predictions
        predictions (list[ModelsPrecomputedPrediction] | Unset): Pre-computed predictions to store
        predicted_at (datetime.datetime | Unset): Timestamp when predictions were generated. Defaults to current time if
            omitted.
    """

    photo_id: UUID
    model_name: str
    predictions: list[ModelsPrecomputedPrediction] | Unset = UNSET
    predicted_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        photo_id = str(self.photo_id)

        model_name = self.model_name

        predictions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.predictions, Unset):
            predictions = []
            for predictions_item_data in self.predictions:
                predictions_item = predictions_item_data.to_dict()
                predictions.append(predictions_item)

        predicted_at: str | Unset = UNSET
        if not isinstance(self.predicted_at, Unset):
            predicted_at = self.predicted_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "photoId": photo_id,
                "modelName": model_name,
            }
        )
        if predictions is not UNSET:
            field_dict["predictions"] = predictions
        if predicted_at is not UNSET:
            field_dict["predictedAt"] = predicted_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_precomputed_prediction import ModelsPrecomputedPrediction

        d = dict(src_dict)
        photo_id = UUID(d.pop("photoId"))

        model_name = d.pop("modelName")

        _predictions = d.pop("predictions", UNSET)
        predictions: list[ModelsPrecomputedPrediction] | Unset = UNSET
        if _predictions is not UNSET:
            predictions = []
            for predictions_item_data in _predictions:
                predictions_item = ModelsPrecomputedPrediction.from_dict(predictions_item_data)

                predictions.append(predictions_item)

        _predicted_at = d.pop("predictedAt", UNSET)
        predicted_at: datetime.datetime | Unset
        if isinstance(_predicted_at, Unset):
            predicted_at = UNSET
        else:
            predicted_at = isoparse(_predicted_at)

        models_upload_predictions_request = cls(
            photo_id=photo_id,
            model_name=model_name,
            predictions=predictions,
            predicted_at=predicted_at,
        )

        models_upload_predictions_request.additional_properties = d
        return models_upload_predictions_request

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
