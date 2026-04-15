from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.models_task_status import ModelsTaskStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.models_inference_task_payload import ModelsInferenceTaskPayload


T = TypeVar("T", bound="ModelsTask")


@_attrs_define
class ModelsTask:
    """A task in the processing queue

    Attributes:
        id (UUID): UUID identifier
        status (ModelsTaskStatus): Status of a task in the processing queue
        type_ (str): Type of the task (e.g., 'aivision:inference')
        attempts (int): Number of processing attempts
        run_at (datetime.datetime): Scheduled run time
        created_at (datetime.datetime): Task creation time
        modified_at (datetime.datetime | Unset): Last modification time
        error_reason (str | Unset): Error reason if task failed
        payload (ModelsInferenceTaskPayload | Unset): Payload information for inference tasks
    """

    id: UUID
    status: ModelsTaskStatus
    type_: str
    attempts: int
    run_at: datetime.datetime
    created_at: datetime.datetime
    modified_at: datetime.datetime | Unset = UNSET
    error_reason: str | Unset = UNSET
    payload: ModelsInferenceTaskPayload | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        status = self.status.value

        type_ = self.type_

        attempts = self.attempts

        run_at = self.run_at.isoformat()

        created_at = self.created_at.isoformat()

        modified_at: str | Unset = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        error_reason = self.error_reason

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "type": type_,
                "attempts": attempts,
                "runAt": run_at,
                "createdAt": created_at,
            }
        )
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if error_reason is not UNSET:
            field_dict["errorReason"] = error_reason
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_inference_task_payload import ModelsInferenceTaskPayload

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        status = ModelsTaskStatus(d.pop("status"))

        type_ = d.pop("type")

        attempts = d.pop("attempts")

        run_at = isoparse(d.pop("runAt"))

        created_at = isoparse(d.pop("createdAt"))

        _modified_at = d.pop("modifiedAt", UNSET)
        modified_at: datetime.datetime | Unset
        if isinstance(_modified_at, Unset):
            modified_at = UNSET
        else:
            modified_at = isoparse(_modified_at)

        error_reason = d.pop("errorReason", UNSET)

        _payload = d.pop("payload", UNSET)
        payload: ModelsInferenceTaskPayload | Unset
        if isinstance(_payload, Unset):
            payload = UNSET
        else:
            payload = ModelsInferenceTaskPayload.from_dict(_payload)

        models_task = cls(
            id=id,
            status=status,
            type_=type_,
            attempts=attempts,
            run_at=run_at,
            created_at=created_at,
            modified_at=modified_at,
            error_reason=error_reason,
            payload=payload,
        )

        models_task.additional_properties = d
        return models_task

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
