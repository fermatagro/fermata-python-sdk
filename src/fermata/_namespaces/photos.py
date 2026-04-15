from __future__ import annotations

import datetime
from collections.abc import Callable
from pathlib import Path
from typing import Any
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from fermata._call import call_async
from fermata._generated.observations.api.photos import (
    create_photo as _create_photo,
)
from fermata._generated.observations.api.photos import (
    create_photo_upload_link as _upload_link,
)
from fermata._generated.observations.models.common_types_grid_pos import CommonTypesGridPos
from fermata._generated.observations.models.create_or_update_photo import CreateOrUpdatePhoto
from fermata._generated.observations.models.models_create_upload_link import ModelsCreateUploadLink
from fermata._generated.observations.models.models_photo_source import ModelsPhotoSource
from fermata._generated.observations.models.models_upload_link_response import ModelsUploadLinkResponse
from fermata._generated.observations.types import UNSET


def _parse_dt(value: str | datetime.datetime) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value
    return isoparse(value)


def _read_image(image: str | Path | bytes) -> bytes:
    if isinstance(image, (str, Path)):
        return Path(image).read_bytes()
    return image


class AsyncPhotos:
    def __init__(self, client: Any, raw_client: httpx.AsyncClient) -> None:
        self._c = client
        self._raw = raw_client

    async def upload_link(
        self, photo_id: str, captured_at: str | datetime.datetime
    ) -> ModelsUploadLinkResponse:
        body = ModelsCreateUploadLink(captured_at=_parse_dt(captured_at))
        return await call_async(_upload_link.asyncio_detailed(UUID(photo_id), body=body, client=self._c))

    async def upload(self, upload_url: str, image: str | Path | bytes) -> None:
        resp = await self._raw.put(upload_url, content=_read_image(image))
        resp.raise_for_status()

    async def create(
        self,
        photo_id: str,
        *,
        greenhouse_id: str,
        captured_at: str | datetime.datetime,
        culture_id: str = "",
        growing_cycle_id: str = "",
        source: str = "human",
        position: dict[str, float] | None = None,
        ptz: list[float] | None = None,
        device_id: str | None = None,
        scan_id: str | None = None,
    ) -> None:
        pos = CommonTypesGridPos(
            x=position.get("x", 0) if position else 0,
            y=position.get("y", 0) if position else 0,
            h=position.get("h", 0) if position else 0,
        )
        body = CreateOrUpdatePhoto(
            id=UUID(photo_id),
            greenhouse_id=UUID(greenhouse_id),
            culture_id=culture_id,
            growing_cycle_id=UUID(growing_cycle_id) if growing_cycle_id else UUID(int=0),
            captured_at=_parse_dt(captured_at),
            source=ModelsPhotoSource(source),
            pos=pos,
            ptz=ptz or [0.0, 0.0, 0.0],
            device_id=UUID(device_id) if device_id else UNSET,
            pipeline_id=UUID(scan_id) if scan_id else UNSET,
        )
        await call_async(_create_photo.asyncio_detailed(UUID(photo_id), body=body, client=self._c))


class SyncPhotos:
    def __init__(self, async_ns: AsyncPhotos, run: Callable[..., Any]) -> None:
        self._a = async_ns
        self._run = run

    def upload_link(self, photo_id: str, captured_at: str | datetime.datetime) -> ModelsUploadLinkResponse:
        return self._run(self._a.upload_link(photo_id, captured_at))

    def upload(self, upload_url: str, image: str | Path | bytes) -> None:
        self._run(self._a.upload(upload_url, image))

    def create(self, photo_id: str, **kw: Any) -> None:
        self._run(self._a.create(photo_id, **kw))
