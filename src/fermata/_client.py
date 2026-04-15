from __future__ import annotations

import datetime
import uuid
from pathlib import Path
from typing import Any, Self

import httpx
from uuid_utils import uuid7

from fermata._auth import TokenManager
from fermata._http import ApiClient, FermataAuth
from fermata._namespaces.catalog import AsyncModels
from fermata._namespaces.cultivation import AsyncCultivation
from fermata._namespaces.greenhouses import AsyncGreenhouses
from fermata._namespaces.inference import AsyncInference
from fermata._namespaces.photos import AsyncPhotos
from fermata._namespaces.pipelines import AsyncPipelines
from fermata.exceptions import ConflictError
from fermata.types import PipelineRun

# Fixed namespace for deterministic photo ID generation (UUIDv5).
_PHOTO_NS = uuid.UUID("a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d")


def _deterministic_photo_id(
    sync_id: str,
    captured_at: str,
    position: dict[str, float] | None,
) -> str:
    """Generate a deterministic photo ID from scan context."""
    parts = [sync_id, captured_at]
    if position:
        parts.extend(
            [str(position.get("x", 0)), str(position.get("y", 0)), str(position.get("h", 0))]
        )
    return str(uuid.uuid5(_PHOTO_NS, ":".join(parts)))


class Fermata:
    """Async Fermata SDK client.

    Usage:
        async with Fermata(url="http://localhost:3000", username="...", password="...") as f:
            task_id = await f.infer(image="photo.jpg", captured_at="...")

    Pipeline mode:
        async with Fermata(url=..., username=..., password=...,
                           pipeline_id="schedule-uuid", sync_id="run-001") as f:
            task_id = await f.infer(image="photo.jpg", captured_at="...")
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
        if pipeline_id and not sync_id:
            raise ValueError("sync_id is required when pipeline_id is set")

        self._url = url
        self._timeout = timeout
        self._tm = TokenManager(url, username, password)
        self._auth = FermataAuth(self._tm, max_retries=max_retries)
        self._pipeline_id = pipeline_id
        self._sync_id = sync_id
        self._scan_id = str(uuid7())
        self._run: PipelineRun | None = None

        # Namespaces initialized in __aenter__ after clients are ready
        self.photos: AsyncPhotos
        self.inference: AsyncInference
        self.models: AsyncModels
        self.greenhouses: AsyncGreenhouses
        self.pipelines: AsyncPipelines
        self.cultivation: AsyncCultivation

    @property
    def scan_id(self) -> str:
        return self._scan_id

    @property
    def run(self) -> PipelineRun | None:
        return self._run

    async def _init_pipeline(self) -> None:
        assert self._pipeline_id is not None
        assert self._sync_id is not None

        # 1. Resolve schedule (scope=growing_cycle, scope_id=cycle_id)
        schedule = await self.pipelines.get_schedule(self._pipeline_id)
        cycle_id = str(schedule.scope_id)
        template_id = str(schedule.template_id)
        model_name: str | None = schedule.arguments.additional_properties.get("model_name")
        org_id = schedule.organization_id

        # 2. Get greenhouse + culture from growing cycle
        cycle = await self.cultivation.get_cycle(cycle_id)
        greenhouse_id = str(cycle.greenhouse_id)
        culture_id = cycle.culture_id if hasattr(cycle, "culture_id") and cycle.culture_id else ""

        # 3. Auto-select model if not in schedule arguments
        if not model_name:
            models_list = await self.models.list()
            if not models_list:
                raise RuntimeError("No models available on Hera and none configured in schedule")
            model_name = models_list[0].model_name

        # 4. Create fire (run instance)
        fire_id = str(uuid7())
        await self.pipelines.create_fire(
            fire_id,
            template_id=template_id,
            scope="growing_cycle",
            scope_id=cycle_id,
            trigger_id=self._pipeline_id,
            arguments={"sync_id": self._sync_id},
        )

        # 5. Store context
        self._run = PipelineRun(
            run_id=fire_id,
            greenhouse_id=greenhouse_id,
            growing_cycle_id=cycle_id,
            culture_id=culture_id,
            model_name=model_name,
            organization_id=org_id,
        )
        self._scan_id = fire_id

        # 6. Mark fire as running
        await self.pipelines.start_fire(fire_id)

    async def __aenter__(self) -> Self:
        await self._tm.open()
        api = ApiClient(self._url, self._auth, timeout=self._timeout)
        self._api = api
        self._raw = httpx.AsyncClient()
        self.photos = AsyncPhotos(api, self._raw)
        self.inference = AsyncInference(api)
        self.models = AsyncModels(api)
        self.greenhouses = AsyncGreenhouses(api)
        self.pipelines = AsyncPipelines(api)
        self.cultivation = AsyncCultivation(api)
        if self._pipeline_id:
            await self._init_pipeline()
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._run:
            error = str(exc[1]) if exc[1] else None
            await self.pipelines.complete_fire(self._run.run_id, error_message=error)
        await self._raw.aclose()
        await self._api.aclose()
        await self._tm.close()

    async def infer(
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
        """Upload photo + submit inference. Returns task_id."""
        # Fill from run context
        culture_id = ""
        growing_cycle_id = ""
        if self._run:
            greenhouse_id = greenhouse_id or self._run.greenhouse_id
            model_name = model_name or self._run.model_name
            culture_id = self._run.culture_id
            growing_cycle_id = self._run.growing_cycle_id

        if not greenhouse_id:
            raise ValueError("greenhouse_id is required when not using pipeline mode")

        ts = captured_at if isinstance(captured_at, str) else captured_at.isoformat()

        # Deterministic photo_id in pipeline mode
        if photo_id is None:
            if self._sync_id:
                photo_id = _deterministic_photo_id(self._sync_id, ts, position)
            else:
                photo_id = str(uuid7())

        link = await self.photos.upload_link(photo_id, captured_at)
        await self.photos.upload(link.upload_url, image)

        try:
            await self.photos.create(
                photo_id,
                greenhouse_id=greenhouse_id,
                captured_at=captured_at,
                culture_id=culture_id,
                growing_cycle_id=growing_cycle_id,
                position=position,
                ptz=ptz,
                scan_id=self._scan_id,
            )
        except ConflictError:
            pass  # already exists (retry idempotency)

        if model_name is None:
            models = await self.models.list()
            if not models:
                raise RuntimeError("No models available on Hera")
            model_name = models[0].model_name

        return await self.inference.submit(photo_id, model_name)
