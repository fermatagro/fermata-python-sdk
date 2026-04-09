from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any

from fermata._generated.observations.models.models_photo import ModelsPhoto
from fermata._generated.observations.models.models_upload_link_response import ModelsUploadLinkResponse
from fermata._transport import Transport


class AsyncPhotos:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    async def upload_link(self, photo_id: str, captured_at: str | datetime.datetime) -> ModelsUploadLinkResponse:
        ts = captured_at if isinstance(captured_at, str) else captured_at.isoformat()
        resp = await self._t.request(
            "POST",
            f"/api/v1/photos/{photo_id}/upload-link",
            json={"capturedAt": ts},
        )
        return ModelsUploadLinkResponse.from_dict(resp.json())

    async def upload(self, upload_url: str, image: str | Path | bytes) -> None:
        if isinstance(image, (str, Path)):
            data = Path(image).read_bytes()
        else:
            data = image
        await self._t.request_raw("PUT", upload_url, content=data)

    async def create(
        self,
        photo_id: str,
        *,
        greenhouse_id: str,
        captured_at: str | datetime.datetime,
        source: str = "human",
        position: dict[str, float] | None = None,
        scan_id: str | None = None,
    ) -> ModelsPhoto:
        ts = captured_at if isinstance(captured_at, str) else captured_at.isoformat()
        body: dict[str, Any] = {
            "greenhouseId": greenhouse_id,
            "capturedAt": ts,
            "source": source,
        }
        if position:
            body["pos"] = {"x": position.get("x", 0), "y": position.get("y", 0), "h": position.get("h", 0)}
        if scan_id:
            body["pipelineId"] = scan_id
        resp = await self._t.request("POST", f"/api/v1/photos/{photo_id}", json=body)
        return ModelsPhoto.from_dict(resp.json())
