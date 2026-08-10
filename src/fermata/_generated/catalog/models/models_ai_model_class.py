from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelsAIModelClass")


@_attrs_define
class ModelsAIModelClass:
    """Class supported by an AI model

    Attributes:
        class_name (str): Class name (e.g. 'whitefly_aphid')
        legacy_num_id (str | Unset): Legacy numeric ID
    """

    class_name: str
    legacy_num_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        class_name = self.class_name

        legacy_num_id = self.legacy_num_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "className": class_name,
            }
        )
        if legacy_num_id is not UNSET:
            field_dict["legacyNumId"] = legacy_num_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        class_name = d.pop("className")

        legacy_num_id = d.pop("legacyNumId", UNSET)

        models_ai_model_class = cls(
            class_name=class_name,
            legacy_num_id=legacy_num_id,
        )

        models_ai_model_class.additional_properties = d
        return models_ai_model_class

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
