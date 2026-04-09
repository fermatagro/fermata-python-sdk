from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.models_update_preset_values_request_values import ModelsUpdatePresetValuesRequestValues


T = TypeVar("T", bound="ModelsUpdatePresetValuesRequest")


@_attrs_define
class ModelsUpdatePresetValuesRequest:
    """Request to replace all threshold values

    Attributes:
        values (ModelsUpdatePresetValuesRequestValues): Map of class name to confidence threshold (0..1)
    """

    values: ModelsUpdatePresetValuesRequestValues
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values = self.values.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_update_preset_values_request_values import ModelsUpdatePresetValuesRequestValues

        d = dict(src_dict)
        values = ModelsUpdatePresetValuesRequestValues.from_dict(d.pop("values"))

        models_update_preset_values_request = cls(
            values=values,
        )

        models_update_preset_values_request.additional_properties = d
        return models_update_preset_values_request

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
