from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ModelsUploadPredictionsResponse")



@_attrs_define
class ModelsUploadPredictionsResponse:
    """ Response from uploading pre-computed predictions

        Attributes:
            rejected_prediction_ids (list[UUID] | Unset): IDs of predictions that were rejected during validation (e.g.
                unknown class names)
     """

    rejected_prediction_ids: list[UUID] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        rejected_prediction_ids: list[str] | Unset = UNSET
        if not isinstance(self.rejected_prediction_ids, Unset):
            rejected_prediction_ids = []
            for rejected_prediction_ids_item_data in self.rejected_prediction_ids:
                rejected_prediction_ids_item = str(rejected_prediction_ids_item_data)
                rejected_prediction_ids.append(rejected_prediction_ids_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if rejected_prediction_ids is not UNSET:
            field_dict["rejectedPredictionIds"] = rejected_prediction_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _rejected_prediction_ids = d.pop("rejectedPredictionIds", UNSET)
        rejected_prediction_ids: list[UUID] | Unset = UNSET
        if _rejected_prediction_ids is not UNSET:
            rejected_prediction_ids = []
            for rejected_prediction_ids_item_data in _rejected_prediction_ids:
                rejected_prediction_ids_item = UUID(rejected_prediction_ids_item_data)



                rejected_prediction_ids.append(rejected_prediction_ids_item)


        models_upload_predictions_response = cls(
            rejected_prediction_ids=rejected_prediction_ids,
        )


        models_upload_predictions_response.additional_properties = d
        return models_upload_predictions_response

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
