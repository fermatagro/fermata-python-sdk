from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.models_zone_object_batch_error_code import ModelsZoneObjectBatchErrorCode

if TYPE_CHECKING:
    from ..models.models_zone_object_batch_error_details_item import ModelsZoneObjectBatchErrorDetailsItem


T = TypeVar("T", bound="ModelsZoneObjectBatchError")


@_attrs_define
class ModelsZoneObjectBatchError:
    """
    Attributes:
        code (ModelsZoneObjectBatchErrorCode):
        details (list[ModelsZoneObjectBatchErrorDetailsItem]):
        request_id (str): Unique identifier for the request, useful for debugging
        message (str): Human-readable message describing the error
        index (int):
    """

    code: ModelsZoneObjectBatchErrorCode
    details: list[ModelsZoneObjectBatchErrorDetailsItem]
    request_id: str
    message: str
    index: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        details = []
        for details_item_data in self.details:
            details_item = details_item_data.to_dict()
            details.append(details_item)

        request_id = self.request_id

        message = self.message

        index = self.index

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "details": details,
                "request_id": request_id,
                "message": message,
                "index": index,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_zone_object_batch_error_details_item import ModelsZoneObjectBatchErrorDetailsItem

        d = dict(src_dict)
        code = ModelsZoneObjectBatchErrorCode(d.pop("code"))

        details = []
        _details = d.pop("details")
        for details_item_data in _details:
            details_item = ModelsZoneObjectBatchErrorDetailsItem.from_dict(details_item_data)

            details.append(details_item)

        request_id = d.pop("request_id")

        message = d.pop("message")

        index = d.pop("index")

        models_zone_object_batch_error = cls(
            code=code,
            details=details,
            request_id=request_id,
            message=message,
            index=index,
        )

        models_zone_object_batch_error.additional_properties = d
        return models_zone_object_batch_error

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
