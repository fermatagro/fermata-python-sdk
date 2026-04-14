from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.models_expected_argument import ModelsExpectedArgument


T = TypeVar("T", bound="UpdateTemplateExpectedArgumentsBody")


@_attrs_define
class UpdateTemplateExpectedArgumentsBody:
    """
    Attributes:
        expected_arguments (list[ModelsExpectedArgument]):
    """

    expected_arguments: list[ModelsExpectedArgument]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expected_arguments = []
        for expected_arguments_item_data in self.expected_arguments:
            expected_arguments_item = expected_arguments_item_data.to_dict()
            expected_arguments.append(expected_arguments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expectedArguments": expected_arguments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_expected_argument import ModelsExpectedArgument

        d = dict(src_dict)
        expected_arguments = []
        _expected_arguments = d.pop("expectedArguments")
        for expected_arguments_item_data in _expected_arguments:
            expected_arguments_item = ModelsExpectedArgument.from_dict(expected_arguments_item_data)

            expected_arguments.append(expected_arguments_item)

        update_template_expected_arguments_body = cls(
            expected_arguments=expected_arguments,
        )

        update_template_expected_arguments_body.additional_properties = d
        return update_template_expected_arguments_body

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
