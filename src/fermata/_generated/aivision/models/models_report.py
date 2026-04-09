from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.models_report_kind import ModelsReportKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelsReport")


@_attrs_define
class ModelsReport:
    """
    Attributes:
        id (UUID): UUID identifier
        greenhouse_id (UUID): UUID identifier
        kind (ModelsReportKind): Type of AI vision report
        title (str):
        from_ (datetime.datetime):
        to (datetime.datetime):
        created_at (datetime.datetime):
        cycle_id (UUID | Unset): UUID identifier
        ready_at (datetime.datetime | Unset):
        download_url (str | Unset): Presigned URL to download the report PDF (available when report is ready)
    """

    id: UUID
    greenhouse_id: UUID
    kind: ModelsReportKind
    title: str
    from_: datetime.datetime
    to: datetime.datetime
    created_at: datetime.datetime
    cycle_id: UUID | Unset = UNSET
    ready_at: datetime.datetime | Unset = UNSET
    download_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        greenhouse_id = str(self.greenhouse_id)

        kind = self.kind.value

        title = self.title

        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        created_at = self.created_at.isoformat()

        cycle_id: str | Unset = UNSET
        if not isinstance(self.cycle_id, Unset):
            cycle_id = str(self.cycle_id)

        ready_at: str | Unset = UNSET
        if not isinstance(self.ready_at, Unset):
            ready_at = self.ready_at.isoformat()

        download_url = self.download_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "greenhouseId": greenhouse_id,
                "kind": kind,
                "title": title,
                "from": from_,
                "to": to,
                "createdAt": created_at,
            }
        )
        if cycle_id is not UNSET:
            field_dict["cycleId"] = cycle_id
        if ready_at is not UNSET:
            field_dict["readyAt"] = ready_at
        if download_url is not UNSET:
            field_dict["downloadUrl"] = download_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        greenhouse_id = UUID(d.pop("greenhouseId"))

        kind = ModelsReportKind(d.pop("kind"))

        title = d.pop("title")

        from_ = isoparse(d.pop("from"))

        to = isoparse(d.pop("to"))

        created_at = isoparse(d.pop("createdAt"))

        _cycle_id = d.pop("cycleId", UNSET)
        cycle_id: UUID | Unset
        if isinstance(_cycle_id, Unset):
            cycle_id = UNSET
        else:
            cycle_id = UUID(_cycle_id)

        _ready_at = d.pop("readyAt", UNSET)
        ready_at: datetime.datetime | Unset
        if isinstance(_ready_at, Unset):
            ready_at = UNSET
        else:
            ready_at = isoparse(_ready_at)

        download_url = d.pop("downloadUrl", UNSET)

        models_report = cls(
            id=id,
            greenhouse_id=greenhouse_id,
            kind=kind,
            title=title,
            from_=from_,
            to=to,
            created_at=created_at,
            cycle_id=cycle_id,
            ready_at=ready_at,
            download_url=download_url,
        )

        models_report.additional_properties = d
        return models_report

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
