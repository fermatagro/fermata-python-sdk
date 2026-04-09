from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.models_preset_level import ModelsPresetLevel
from ..models.models_preset_type import ModelsPresetType

if TYPE_CHECKING:
    from ..models.create_or_update_threshold_preset_values import CreateOrUpdateThresholdPresetValues


T = TypeVar("T", bound="CreateOrUpdateThresholdPreset")


@_attrs_define
class CreateOrUpdateThresholdPreset:
    """
    Attributes:
        level (ModelsPresetLevel): Hierarchy level of a threshold preset
        external_id (str): Scoping key: model_name for model-level, org_id for organization, gc_id for gc
        model_name (str):
        preset_type (ModelsPresetType): Preset category
        name (str):
        values (CreateOrUpdateThresholdPresetValues): Map of class name to confidence threshold (0..1)
    """

    level: ModelsPresetLevel
    external_id: str
    model_name: str
    preset_type: ModelsPresetType
    name: str
    values: CreateOrUpdateThresholdPresetValues
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        external_id = self.external_id

        model_name = self.model_name

        preset_type = self.preset_type.value

        name = self.name

        values = self.values.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "level": level,
                "externalId": external_id,
                "modelName": model_name,
                "presetType": preset_type,
                "name": name,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_or_update_threshold_preset_values import CreateOrUpdateThresholdPresetValues

        d = dict(src_dict)
        level = ModelsPresetLevel(d.pop("level"))

        external_id = d.pop("externalId")

        model_name = d.pop("modelName")

        preset_type = ModelsPresetType(d.pop("presetType"))

        name = d.pop("name")

        values = CreateOrUpdateThresholdPresetValues.from_dict(d.pop("values"))

        create_or_update_threshold_preset = cls(
            level=level,
            external_id=external_id,
            model_name=model_name,
            preset_type=preset_type,
            name=name,
            values=values,
        )

        create_or_update_threshold_preset.additional_properties = d
        return create_or_update_threshold_preset

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
