from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ModelsInferenceRequest")


@_attrs_define
class ModelsInferenceRequest:
    """Request to submit an inference task

    Attributes:
        photo_id (UUID): UUID identifier
        model_name (str): ML model name to use for inference
    """

    photo_id: UUID
    model_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        photo_id = str(self.photo_id)

        model_name = self.model_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "photoId": photo_id,
                "modelName": model_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        photo_id = UUID(d.pop("photoId"))

        model_name = d.pop("modelName")

        models_inference_request = cls(
            photo_id=photo_id,
            model_name=model_name,
        )

        models_inference_request.additional_properties = d
        return models_inference_request

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
