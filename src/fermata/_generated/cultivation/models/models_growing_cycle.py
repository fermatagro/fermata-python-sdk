from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelsGrowingCycle")


@_attrs_define
class ModelsGrowingCycle:
    """A growing cycle (planting to harvest) in a greenhouse

    Attributes:
        id (UUID): UUID identifier
        description (str):
        organization_id (str): Organization identifier (opaque string)
        greenhouse_id (UUID): UUID identifier
        planting_date (datetime.datetime):
        currency (str | Unset): Currency code (ISO 4217)
        culture_id (str | Unset):
        harvest_date (datetime.datetime | Unset):
    """

    id: UUID
    description: str
    organization_id: str
    greenhouse_id: UUID
    planting_date: datetime.datetime
    currency: str | Unset = UNSET
    culture_id: str | Unset = UNSET
    harvest_date: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        description = self.description

        organization_id = self.organization_id

        greenhouse_id = str(self.greenhouse_id)

        planting_date = self.planting_date.isoformat()

        currency = self.currency

        culture_id = self.culture_id

        harvest_date: str | Unset = UNSET
        if not isinstance(self.harvest_date, Unset):
            harvest_date = self.harvest_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "description": description,
                "organizationId": organization_id,
                "greenhouseId": greenhouse_id,
                "plantingDate": planting_date,
            }
        )
        if currency is not UNSET:
            field_dict["currency"] = currency
        if culture_id is not UNSET:
            field_dict["cultureId"] = culture_id
        if harvest_date is not UNSET:
            field_dict["harvestDate"] = harvest_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        description = d.pop("description")

        organization_id = d.pop("organizationId")

        greenhouse_id = UUID(d.pop("greenhouseId"))

        planting_date = isoparse(d.pop("plantingDate"))

        currency = d.pop("currency", UNSET)

        culture_id = d.pop("cultureId", UNSET)

        _harvest_date = d.pop("harvestDate", UNSET)
        harvest_date: datetime.datetime | Unset
        if isinstance(_harvest_date, Unset):
            harvest_date = UNSET
        else:
            harvest_date = isoparse(_harvest_date)

        models_growing_cycle = cls(
            id=id,
            description=description,
            organization_id=organization_id,
            greenhouse_id=greenhouse_id,
            planting_date=planting_date,
            currency=currency,
            culture_id=culture_id,
            harvest_date=harvest_date,
        )

        models_growing_cycle.additional_properties = d
        return models_growing_cycle

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
