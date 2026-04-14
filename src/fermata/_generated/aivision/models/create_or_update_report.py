from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.models_report_kind import ModelsReportKind
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="CreateOrUpdateReport")



@_attrs_define
class CreateOrUpdateReport:
    """ 
        Attributes:
            greenhouse_id (UUID): UUID identifier
            kind (ModelsReportKind): Type of AI vision report
            title (str):
            from_ (datetime.datetime):
            to (datetime.datetime):
            print_url (str): Full URL for Gotenberg to render the PDF (e.g., https://admin.example.com/reports/{id}/pdf)
            cycle_id (UUID | Unset): UUID identifier
     """

    greenhouse_id: UUID
    kind: ModelsReportKind
    title: str
    from_: datetime.datetime
    to: datetime.datetime
    print_url: str
    cycle_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        greenhouse_id = str(self.greenhouse_id)

        kind = self.kind.value

        title = self.title

        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        print_url = self.print_url

        cycle_id: str | Unset = UNSET
        if not isinstance(self.cycle_id, Unset):
            cycle_id = str(self.cycle_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "greenhouseId": greenhouse_id,
            "kind": kind,
            "title": title,
            "from": from_,
            "to": to,
            "printUrl": print_url,
        })
        if cycle_id is not UNSET:
            field_dict["cycleId"] = cycle_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        greenhouse_id = UUID(d.pop("greenhouseId"))




        kind = ModelsReportKind(d.pop("kind"))




        title = d.pop("title")

        from_ = isoparse(d.pop("from"))




        to = isoparse(d.pop("to"))




        print_url = d.pop("printUrl")

        _cycle_id = d.pop("cycleId", UNSET)
        cycle_id: UUID | Unset
        if isinstance(_cycle_id,  Unset):
            cycle_id = UNSET
        else:
            cycle_id = UUID(_cycle_id)




        create_or_update_report = cls(
            greenhouse_id=greenhouse_id,
            kind=kind,
            title=title,
            from_=from_,
            to=to,
            print_url=print_url,
            cycle_id=cycle_id,
        )


        create_or_update_report.additional_properties = d
        return create_or_update_report

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
