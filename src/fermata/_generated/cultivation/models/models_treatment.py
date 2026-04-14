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
    from ..models.common_types_grid_rect import CommonTypesGridRect


T = TypeVar("T", bound="ModelsTreatment")


@_attrs_define
class ModelsTreatment:
    """A crop treatment applied to a growing cycle

    Attributes:
        id (UUID): UUID identifier
        organization_id (str): Organization identifier (opaque string)
        growing_cycle_id (UUID): UUID identifier
        treatment_type_id (str):
        name (str):
        applied_at (datetime.datetime):
        rect (CommonTypesGridRect): Rectangular area on the greenhouse grid
        concentration (float | Unset): Concentration in g/l (grams per liter)
        applied_volume (float | Unset): Applied volume in liters
        cost (float | Unset): Cost of the treatment
        currency (str | Unset): Currency code (ISO 4217)
        note (str | Unset):
    """

    id: UUID
    organization_id: str
    growing_cycle_id: UUID
    treatment_type_id: str
    name: str
    applied_at: datetime.datetime
    rect: CommonTypesGridRect
    concentration: float | Unset = UNSET
    applied_volume: float | Unset = UNSET
    cost: float | Unset = UNSET
    currency: str | Unset = UNSET
    note: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        organization_id = self.organization_id

        growing_cycle_id = str(self.growing_cycle_id)

        treatment_type_id = self.treatment_type_id

        name = self.name

        applied_at = self.applied_at.isoformat()

        rect = self.rect.to_dict()

        concentration = self.concentration

        applied_volume = self.applied_volume

        cost = self.cost

        currency = self.currency

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organizationId": organization_id,
                "growingCycleId": growing_cycle_id,
                "treatmentTypeId": treatment_type_id,
                "name": name,
                "appliedAt": applied_at,
                "rect": rect,
            }
        )
        if concentration is not UNSET:
            field_dict["concentration"] = concentration
        if applied_volume is not UNSET:
            field_dict["appliedVolume"] = applied_volume
        if cost is not UNSET:
            field_dict["cost"] = cost
        if currency is not UNSET:
            field_dict["currency"] = currency
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_rect import CommonTypesGridRect

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        organization_id = d.pop("organizationId")

        growing_cycle_id = UUID(d.pop("growingCycleId"))

        treatment_type_id = d.pop("treatmentTypeId")

        name = d.pop("name")

        applied_at = isoparse(d.pop("appliedAt"))

        rect = CommonTypesGridRect.from_dict(d.pop("rect"))

        concentration = d.pop("concentration", UNSET)

        applied_volume = d.pop("appliedVolume", UNSET)

        cost = d.pop("cost", UNSET)

        currency = d.pop("currency", UNSET)

        note = d.pop("note", UNSET)

        models_treatment = cls(
            id=id,
            organization_id=organization_id,
            growing_cycle_id=growing_cycle_id,
            treatment_type_id=treatment_type_id,
            name=name,
            applied_at=applied_at,
            rect=rect,
            concentration=concentration,
            applied_volume=applied_volume,
            cost=cost,
            currency=currency,
            note=note,
        )

        models_treatment.additional_properties = d
        return models_treatment

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
