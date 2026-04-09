from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.models_report import ModelsReport


T = TypeVar("T", bound="ListReportsResponse200")


@_attrs_define
class ListReportsResponse200:
    """Generic paginated response model with cursor-based pagination

    Attributes:
        items (list[ModelsReport]): Items for the current page
        next_token (str | Unset): Token to retrieve the next page of items, if any
    """

    items: list[ModelsReport]
    next_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        next_token = self.next_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )
        if next_token is not UNSET:
            field_dict["next_token"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_report import ModelsReport

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ModelsReport.from_dict(items_item_data)

            items.append(items_item)

        next_token = d.pop("next_token", UNSET)

        list_reports_response_200 = cls(
            items=items,
            next_token=next_token,
        )

        list_reports_response_200.additional_properties = d
        return list_reports_response_200

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
