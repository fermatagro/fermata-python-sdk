from __future__ import annotations

import asyncio
import datetime
from pathlib import Path
from typing import Any, Self

from fermata._client import Fermata
from fermata._namespaces.catalog import SyncModels
from fermata._namespaces.cultivation import SyncCultivation
from fermata._namespaces.greenhouses import SyncGreenhouses
from fermata._namespaces.inference import SyncInference
from fermata._namespaces.photos import SyncPhotos
from fermata._namespaces.pipelines import SyncPipelines
from fermata.types import PipelineRun


class FermataSync:
    """Sync Fermata SDK client.

    Wraps the async ``Fermata`` client with ``loop.run_until_complete()``.
    All logic lives in the async client — this is a thin sync adapter.

    Usage:
        with FermataSync(url="http://localhost:3000", username="...", password="...") as f:
            task_id = f.infer(image="photo.jpg", captured_at="...")

    Pipeline mode:
        with FermataSync(url=..., username=..., password=...,
                         pipeline_id="schedule-uuid", sync_id="run-001") as f:
            task_id = f.infer(image="photo.jpg", captured_at="...")
    """

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        *,
        pipeline_id: str | None = None,
        sync_id: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._loop = asyncio.new_event_loop()
        self._async = Fermata(
            url, username, password,
            pipeline_id=pipeline_id,
            sync_id=sync_id,
            timeout=timeout,
            max_retries=max_retries,
        )

    def _run(self, coro: Any) -> Any:
        return self._loop.run_until_complete(coro)

    @property
    def scan_id(self) -> str:
        return self._async.scan_id

    @property
    def run(self) -> PipelineRun | None:
        return self._async.run

    def __enter__(self) -> Self:
        self._run(self._async.__aenter__())
        self.photos = SyncPhotos(self._async.photos, self._run)
        self.inference = SyncInference(self._async.inference, self._run)
        self.models = SyncModels(self._async.models, self._run)
        self.greenhouses = SyncGreenhouses(self._async.greenhouses, self._run)
        self.pipelines = SyncPipelines(self._async.pipelines, self._run)
        self.cultivation = SyncCultivation(self._async.cultivation, self._run)
        return self

    def __exit__(self, *exc: Any) -> None:
        self._run(self._async.__aexit__(*exc))
        self._loop.close()

    def infer(
        self,
        image: str | Path | bytes,
        captured_at: str | datetime.datetime,
        *,
        greenhouse_id: str | None = None,
        position: dict[str, float] | None = None,
        ptz: list[float] | None = None,
        model_name: str | None = None,
        photo_id: str | None = None,
    ) -> str:
        return self._run(
            self._async.infer(
                image, captured_at,
                greenhouse_id=greenhouse_id,
                position=position,
                ptz=ptz,
                model_name=model_name,
                photo_id=photo_id,
            )
        )
