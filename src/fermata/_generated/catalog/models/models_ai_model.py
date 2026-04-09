from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.models_ai_model_type import ModelsAIModelType

T = TypeVar("T", bound="ModelsAIModel")


@_attrs_define
class ModelsAIModel:
    """AI Model from ML API

    Attributes:
        model_name (str): Model name (unique identifier)
        model_type (ModelsAIModelType): Type of AI model
        is_active (bool): Whether the model is active
    """

    model_name: str
    model_type: ModelsAIModelType
    is_active: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_name = self.model_name

        model_type = self.model_type.value

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "modelName": model_name,
                "modelType": model_type,
                "isActive": is_active,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_name = d.pop("modelName")

        model_type = ModelsAIModelType(d.pop("modelType"))

        is_active = d.pop("isActive")

        models_ai_model = cls(
            model_name=model_name,
            model_type=model_type,
            is_active=is_active,
        )

        models_ai_model.additional_properties = d
        return models_ai_model

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
