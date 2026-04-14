from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.models_threshold_preset import ModelsThresholdPreset





T = TypeVar("T", bound="ListPresetsResponse200")



@_attrs_define
class ListPresetsResponse200:
    """ Generic paginated response model with cursor-based pagination

        Attributes:
            items (list[ModelsThresholdPreset]): Items for the current page
            next_token (str | Unset): Token to retrieve the next page of items, if any
     """

    items: list[ModelsThresholdPreset]
    next_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.models_threshold_preset import ModelsThresholdPreset
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        next_token = self.next_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "items": items,
        })
        if next_token is not UNSET:
            field_dict["next_token"] = next_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_threshold_preset import ModelsThresholdPreset
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ModelsThresholdPreset.from_dict(items_item_data)



            items.append(items_item)


        next_token = d.pop("next_token", UNSET)

        list_presets_response_200 = cls(
            items=items,
            next_token=next_token,
        )


        list_presets_response_200.additional_properties = d
        return list_presets_response_200

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
