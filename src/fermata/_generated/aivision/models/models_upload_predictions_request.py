from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.models_precomputed_prediction import ModelsPrecomputedPrediction





T = TypeVar("T", bound="ModelsUploadPredictionsRequest")



@_attrs_define
class ModelsUploadPredictionsRequest:
    """ Request to upload pre-computed predictions for a photo

        Attributes:
            photo_id (UUID): UUID identifier
            model_name (str): ML model name that produced the predictions
            organization_name (str | Unset): Organization display name (for inference logs)
            greenhouse_id (UUID | Unset): UUID identifier
            culture_id (str | Unset): Culture being grown
            growing_cycle_id (UUID | Unset): UUID identifier
            planting_date (datetime.datetime | Unset): Planting date for the growing cycle
            device_id (UUID | Unset): UUID identifier
            device_type (str | Unset): Device type (e.g. 'camera', 'router')
            predictions (list[ModelsPrecomputedPrediction] | Unset): Pre-computed predictions to store
            predicted_at (datetime.datetime | Unset): Timestamp when predictions were generated. Defaults to current time if
                omitted.
     """

    photo_id: UUID
    model_name: str
    organization_name: str | Unset = UNSET
    greenhouse_id: UUID | Unset = UNSET
    culture_id: str | Unset = UNSET
    growing_cycle_id: UUID | Unset = UNSET
    planting_date: datetime.datetime | Unset = UNSET
    device_id: UUID | Unset = UNSET
    device_type: str | Unset = UNSET
    predictions: list[ModelsPrecomputedPrediction] | Unset = UNSET
    predicted_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.models_precomputed_prediction import ModelsPrecomputedPrediction
        photo_id = str(self.photo_id)

        model_name = self.model_name

        organization_name = self.organization_name

        greenhouse_id: str | Unset = UNSET
        if not isinstance(self.greenhouse_id, Unset):
            greenhouse_id = str(self.greenhouse_id)

        culture_id = self.culture_id

        growing_cycle_id: str | Unset = UNSET
        if not isinstance(self.growing_cycle_id, Unset):
            growing_cycle_id = str(self.growing_cycle_id)

        planting_date: str | Unset = UNSET
        if not isinstance(self.planting_date, Unset):
            planting_date = self.planting_date.isoformat()

        device_id: str | Unset = UNSET
        if not isinstance(self.device_id, Unset):
            device_id = str(self.device_id)

        device_type = self.device_type

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
        field_dict.update({
            "photoId": photo_id,
            "modelName": model_name,
        })
        if organization_name is not UNSET:
            field_dict["organizationName"] = organization_name
        if greenhouse_id is not UNSET:
            field_dict["greenhouseId"] = greenhouse_id
        if culture_id is not UNSET:
            field_dict["cultureId"] = culture_id
        if growing_cycle_id is not UNSET:
            field_dict["growingCycleId"] = growing_cycle_id
        if planting_date is not UNSET:
            field_dict["plantingDate"] = planting_date
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if device_type is not UNSET:
            field_dict["deviceType"] = device_type
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

        organization_name = d.pop("organizationName", UNSET)

        _greenhouse_id = d.pop("greenhouseId", UNSET)
        greenhouse_id: UUID | Unset
        if isinstance(_greenhouse_id,  Unset):
            greenhouse_id = UNSET
        else:
            greenhouse_id = UUID(_greenhouse_id)




        culture_id = d.pop("cultureId", UNSET)

        _growing_cycle_id = d.pop("growingCycleId", UNSET)
        growing_cycle_id: UUID | Unset
        if isinstance(_growing_cycle_id,  Unset):
            growing_cycle_id = UNSET
        else:
            growing_cycle_id = UUID(_growing_cycle_id)




        _planting_date = d.pop("plantingDate", UNSET)
        planting_date: datetime.datetime | Unset
        if isinstance(_planting_date,  Unset):
            planting_date = UNSET
        else:
            planting_date = isoparse(_planting_date)




        _device_id = d.pop("deviceId", UNSET)
        device_id: UUID | Unset
        if isinstance(_device_id,  Unset):
            device_id = UNSET
        else:
            device_id = UUID(_device_id)




        device_type = d.pop("deviceType", UNSET)

        _predictions = d.pop("predictions", UNSET)
        predictions: list[ModelsPrecomputedPrediction] | Unset = UNSET
        if _predictions is not UNSET:
            predictions = []
            for predictions_item_data in _predictions:
                predictions_item = ModelsPrecomputedPrediction.from_dict(predictions_item_data)



                predictions.append(predictions_item)


        _predicted_at = d.pop("predictedAt", UNSET)
        predicted_at: datetime.datetime | Unset
        if isinstance(_predicted_at,  Unset):
            predicted_at = UNSET
        else:
            predicted_at = isoparse(_predicted_at)




        models_upload_predictions_request = cls(
            photo_id=photo_id,
            model_name=model_name,
            organization_name=organization_name,
            greenhouse_id=greenhouse_id,
            culture_id=culture_id,
            growing_cycle_id=growing_cycle_id,
            planting_date=planting_date,
            device_id=device_id,
            device_type=device_type,
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
