from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.models_terminal_status import ModelsTerminalStatus
from ..types import UNSET, Unset






T = TypeVar("T", bound="ModelsCompleteFireRequest")



@_attrs_define
class ModelsCompleteFireRequest:
    """ Request to complete a fire with terminal status

        Attributes:
            status (ModelsTerminalStatus): Terminal status for completing a fire
            error_message (str | Unset): Error message (should be present when status=failed)
     """

    status: ModelsTerminalStatus
    error_message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        error_message = self.error_message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
        })
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ModelsTerminalStatus(d.pop("status"))




        error_message = d.pop("errorMessage", UNSET)

        models_complete_fire_request = cls(
            status=status,
            error_message=error_message,
        )


        models_complete_fire_request.additional_properties = d
        return models_complete_fire_request

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
