from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ModelsHidePredictionsRequest")



@_attrs_define
class ModelsHidePredictionsRequest:
    """ Request to hide predictions

        Attributes:
            prediction_ids (list[UUID]): List of prediction IDs to hide
     """

    prediction_ids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        prediction_ids = []
        for prediction_ids_item_data in self.prediction_ids:
            prediction_ids_item = str(prediction_ids_item_data)
            prediction_ids.append(prediction_ids_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "predictionIds": prediction_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        prediction_ids = []
        _prediction_ids = d.pop("predictionIds")
        for prediction_ids_item_data in (_prediction_ids):
            prediction_ids_item = UUID(prediction_ids_item_data)



            prediction_ids.append(prediction_ids_item)


        models_hide_predictions_request = cls(
            prediction_ids=prediction_ids,
        )


        models_hide_predictions_request.additional_properties = d
        return models_hide_predictions_request

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
