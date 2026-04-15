from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Self

import httpx
from uuid_utils import uuid7

from fermata._auth import TokenManager

# Reuse from async client
from fermata._client import _PHOTO_NS, _deterministic_photo_id  # noqa: F401
from fermata._http import FermataAuth, SyncApiClient
from fermata._namespaces.catalog import SyncModels
from fermata._namespaces.cultivation import SyncCultivation
from fermata._namespaces.greenhouses import SyncGreenhouses
from fermata._namespaces.inference import SyncInference
from fermata._namespaces.photos import SyncPhotos
from fermata._namespaces.pipelines import SyncPipelines
from fermata.exceptions import ConflictError
from fermata.types import PipelineRun


class FermataSync:
    """Sync Fermata SDK client.

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

        self.photos: SyncPhotos
        self.inference: SyncInference
        self.models: SyncModels
        self.greenhouses: SyncGreenhouses
        self.pipelines: SyncPipelines
        self.cultivation: SyncCultivation

    @property
    def scan_id(self) -> str:
        return self._scan_id

    @property
    def run(self) -> PipelineRun | None:
        return self._run

    def _init_pipeline(self) -> None:
        assert self._pipeline_id is not None
        assert self._sync_id is not None

        schedule = self.pipelines.get_schedule(self._pipeline_id)
        cycle_id = str(schedule.scope_id)
        template_id = str(schedule.template_id)
        model_name: str | None = schedule.arguments.additional_properties.get("model_name")
        org_id = schedule.organization_id

        cycle = self.cultivation.get_cycle(cycle_id)
        greenhouse_id = str(cycle.greenhouse_id)
        culture_id = cycle.culture_id if hasattr(cycle, "culture_id") and cycle.culture_id else ""

        if not model_name:
            models_list = self.models.list()
            if not models_list:
                raise RuntimeError("No models available on Hera and none configured in schedule")
            model_name = models_list[0].model_name

        fire_id = str(uuid7())
        self.pipelines.create_fire(
            fire_id,
            template_id=template_id,
            scope="growing_cycle",
            scope_id=cycle_id,
            trigger_id=self._pipeline_id,
            arguments={"sync_id": self._sync_id},
        )

        self._run = PipelineRun(
            run_id=fire_id,
            greenhouse_id=greenhouse_id,
            growing_cycle_id=cycle_id,
            culture_id=culture_id,
            model_name=model_name,
            organization_id=org_id,
        )
        self._scan_id = fire_id

    def __enter__(self) -> Self:
        self._tm.open_sync()
        api = SyncApiClient(self._url, self._auth, timeout=self._timeout)
        self._api = api
        self._raw = httpx.Client()
        self.photos = SyncPhotos(api, self._raw)
        self.inference = SyncInference(api)
        self.models = SyncModels(api)
        self.greenhouses = SyncGreenhouses(api)
        self.pipelines = SyncPipelines(api)
        self.cultivation = SyncCultivation(api)
        if self._pipeline_id:
            self._init_pipeline()
        return self

    def __exit__(self, *exc: Any) -> None:
        self._raw.close()
        self._api.close()
        self._tm.close_sync()

    def infer(
        self,
        image: str | Path | bytes,
        captured_at: str | datetime.datetime,
        *,
        greenhouse_id: str | None = None,
        position: dict[str, float] | None = None,
        model_name: str | None = None,
        photo_id: str | None = None,
    ) -> str:
        """Upload photo + submit inference. Returns task_id."""
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

        if photo_id is None:
            if self._sync_id:
                photo_id = _deterministic_photo_id(self._sync_id, ts, position)
            else:
                photo_id = str(uuid7())

        link = self.photos.upload_link(photo_id, captured_at)
        self.photos.upload(link.upload_url, image)

        try:
            self.photos.create(
                photo_id,
                greenhouse_id=greenhouse_id,
                captured_at=captured_at,
                culture_id=culture_id,
                growing_cycle_id=growing_cycle_id,
                position=position,
                scan_id=self._scan_id,
            )
        except ConflictError:
            pass

        if model_name is None:
            models = self.models.list()
            if not models:
                raise RuntimeError("No models available on Hera")
            model_name = models[0].model_name

        return self.inference.submit(photo_id, model_name)
