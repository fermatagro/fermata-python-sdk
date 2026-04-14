from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.models_expected_argument import ModelsExpectedArgument


T = TypeVar("T", bound="CreateOrUpdateTemplate")


@_attrs_define
class CreateOrUpdateTemplate:
    """
    Attributes:
        name (str): Human-readable name for the pipeline
        flow_name (str): Prefect flow identifier (immutable after creation)
        description (str | Unset): Description of what this pipeline does
        expected_arguments (list[ModelsExpectedArgument] | Unset): Argument definitions describing what parameters this
            pipeline accepts
    """

    name: str
    flow_name: str
    description: str | Unset = UNSET
    expected_arguments: list[ModelsExpectedArgument] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        flow_name = self.flow_name

        description = self.description

        expected_arguments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.expected_arguments, Unset):
            expected_arguments = []
            for expected_arguments_item_data in self.expected_arguments:
                expected_arguments_item = expected_arguments_item_data.to_dict()
                expected_arguments.append(expected_arguments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "flowName": flow_name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if expected_arguments is not UNSET:
            field_dict["expectedArguments"] = expected_arguments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_expected_argument import ModelsExpectedArgument

        d = dict(src_dict)
        name = d.pop("name")

        flow_name = d.pop("flowName")

        description = d.pop("description", UNSET)

        _expected_arguments = d.pop("expectedArguments", UNSET)
        expected_arguments: list[ModelsExpectedArgument] | Unset = UNSET
        if _expected_arguments is not UNSET:
            expected_arguments = []
            for expected_arguments_item_data in _expected_arguments:
                expected_arguments_item = ModelsExpectedArgument.from_dict(expected_arguments_item_data)

                expected_arguments.append(expected_arguments_item)

        create_or_update_template = cls(
            name=name,
            flow_name=flow_name,
            description=description,
            expected_arguments=expected_arguments,
        )

        create_or_update_template.additional_properties = d
        return create_or_update_template

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
