from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.models_preset_level import ModelsPresetLevel
from ..models.models_preset_type import ModelsPresetType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.models_threshold_preset_values import ModelsThresholdPresetValues


T = TypeVar("T", bound="ModelsThresholdPreset")


@_attrs_define
class ModelsThresholdPreset:
    """A threshold preset with per-class confidence thresholds for a model

    Attributes:
        id (UUID): UUID identifier
        level (ModelsPresetLevel): Hierarchy level of a threshold preset
        external_id (str): Scoping key: model_name for model-level, org_id for organization, gc_id for gc
        model_name (str):
        preset_type (ModelsPresetType): Preset category
        selected (bool):
        name (str):
        values (ModelsThresholdPresetValues): Map of class name to confidence threshold (0..1)
        created_at (datetime.datetime):
        owner_organization_id (str | Unset): Owner organization ID. Null for model-level (system) presets.
        updated_at (datetime.datetime | Unset):
    """

    id: UUID
    level: ModelsPresetLevel
    external_id: str
    model_name: str
    preset_type: ModelsPresetType
    selected: bool
    name: str
    values: ModelsThresholdPresetValues
    created_at: datetime.datetime
    owner_organization_id: str | Unset = UNSET
    updated_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        level = self.level.value

        external_id = self.external_id

        model_name = self.model_name

        preset_type = self.preset_type.value

        selected = self.selected

        name = self.name

        values = self.values.to_dict()

        created_at = self.created_at.isoformat()

        owner_organization_id = self.owner_organization_id

        updated_at: str | Unset = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "level": level,
                "externalId": external_id,
                "modelName": model_name,
                "presetType": preset_type,
                "selected": selected,
                "name": name,
                "values": values,
                "createdAt": created_at,
            }
        )
        if owner_organization_id is not UNSET:
            field_dict["ownerOrganizationId"] = owner_organization_id
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_threshold_preset_values import ModelsThresholdPresetValues

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        level = ModelsPresetLevel(d.pop("level"))

        external_id = d.pop("externalId")

        model_name = d.pop("modelName")

        preset_type = ModelsPresetType(d.pop("presetType"))

        selected = d.pop("selected")

        name = d.pop("name")

        values = ModelsThresholdPresetValues.from_dict(d.pop("values"))

        created_at = isoparse(d.pop("createdAt"))

        owner_organization_id = d.pop("ownerOrganizationId", UNSET)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: datetime.datetime | Unset
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        models_threshold_preset = cls(
            id=id,
            level=level,
            external_id=external_id,
            model_name=model_name,
            preset_type=preset_type,
            selected=selected,
            name=name,
            values=values,
            created_at=created_at,
            owner_organization_id=owner_organization_id,
            updated_at=updated_at,
        )

        models_threshold_preset.additional_properties = d
        return models_threshold_preset

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
