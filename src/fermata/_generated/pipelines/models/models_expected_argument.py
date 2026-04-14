from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.models_argument_type import ModelsArgumentType
from ..types import UNSET, Unset






T = TypeVar("T", bound="ModelsExpectedArgument")



@_attrs_define
class ModelsExpectedArgument:
    """ Metadata describing an expected argument for a pipeline template

        Attributes:
            name (str): Argument name (key used when passing arguments to the pipeline)
            type_ (ModelsArgumentType): Type of an expected argument value
            required (bool): Whether this argument must be provided
            default_value (str | Unset): Default value when argument is omitted (serialized as string)
            description (str | Unset): Human-readable description of the argument's purpose
     """

    name: str
    type_: ModelsArgumentType
    required: bool
    default_value: str | Unset = UNSET
    description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_.value

        required = self.required

        default_value = self.default_value

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "type": type_,
            "required": required,
        })
        if default_value is not UNSET:
            field_dict["defaultValue"] = default_value
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = ModelsArgumentType(d.pop("type"))




        required = d.pop("required")

        default_value = d.pop("defaultValue", UNSET)

        description = d.pop("description", UNSET)

        models_expected_argument = cls(
            name=name,
            type_=type_,
            required=required,
            default_value=default_value,
            description=description,
        )


        models_expected_argument.additional_properties = d
        return models_expected_argument

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
