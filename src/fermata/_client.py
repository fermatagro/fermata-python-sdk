from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Self
from uuid_utils import uuid7

from fermata._auth import TokenManager
from fermata._namespaces.catalog import AsyncModels
from fermata._namespaces.greenhouses import AsyncGreenhouses
from fermata._namespaces.inference import AsyncInference
from fermata._namespaces.photos import AsyncPhotos
from fermata._transport import Transport


class Fermata:
    """Async Fermata SDK client.

    Each instance represents a single scan session. All photos submitted
    through the same instance are grouped under the same scan_id.

    Usage:
        async with Fermata(url="http://localhost:3000", username="...", password="...") as f:
            task_id = await f.infer(image="photo.jpg", greenhouse_id="gh-01", captured_at="...")
    """

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        *,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._token_manager = TokenManager(url, username, password)
        self._transport = Transport(url, self._token_manager, timeout=timeout, max_retries=max_retries)
        self._scan_id = str(uuid7())

        self.photos = AsyncPhotos(self._transport)
        self.inference = AsyncInference(self._transport)
        self.models = AsyncModels(self._transport)
        self.greenhouses = AsyncGreenhouses(self._transport)

    @property
    def scan_id(self) -> str:
        """Unique ID for this scan session. Auto-generated on construction."""
        return self._scan_id

    async def __aenter__(self) -> Self:
        await self._transport.__aenter__()
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self._transport.__aexit__(*exc)

    async def infer(
        self,
        image: str | Path | bytes,
        greenhouse_id: str,
        captured_at: str | datetime.datetime,
        *,
        position: dict[str, float] | None = None,
        model_name: str | None = None,
        photo_id: str | None = None,
    ) -> str:
        """Upload photo + submit inference. Returns task_id.

        Steps:
        1. Generate photo_id (UUIDv7) if not provided
        2. Get presigned upload URL from Hera
        3. Upload image bytes to storage via presigned URL
        4. Create photo metadata in Hera
        5. Resolve model_name if not specified
        6. Submit inference task
        7. Return task_id
        """
        if photo_id is None:
            photo_id = str(uuid7())

        link = await self.photos.upload_link(photo_id, captured_at)
        await self.photos.upload(link.upload_url, image)
        await self.photos.create(
            photo_id,
            greenhouse_id=greenhouse_id,
            captured_at=captured_at,
            position=position,
            scan_id=self._scan_id,
        )

        if model_name is None:
            models = await self.models.list()
            if not models:
                raise RuntimeError("No models available on Hera")
            model_name = models[0].model_name

        task_id = await self.inference.submit(photo_id, model_name)
        return task_id
