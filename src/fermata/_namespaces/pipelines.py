from __future__ import annotations

from uuid import UUID

from fermata._generated.pipelines.models.models_schedule import ModelsSchedule
from fermata._generated.pipelines.models.models_template import ModelsTemplate
from fermata._transport import Transport


class AsyncPipelines:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    async def list(self) -> list[ModelsTemplate]:
        resp = await self._t.request("GET", "/api/v1/pipelines/templates")
        return [ModelsTemplate.from_dict(item) for item in resp.json()["items"]]

    async def list_schedules(self, template_id: UUID | str | None = None) -> list[ModelsSchedule]:
        params = {"templateId": str(template_id)} if template_id is not None else None
        resp = await self._t.request("GET", "/api/v1/pipelines/schedules", params=params)
        return [ModelsSchedule.from_dict(item) for item in resp.json()["items"]]
