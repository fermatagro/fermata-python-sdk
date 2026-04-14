from __future__ import annotations

from typing import Any

from fermata._transport import Transport


class AsyncPipelines:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    async def get_schedule(self, schedule_id: str) -> dict[str, Any]:
        """Fetch a pipeline schedule by ID.

        GET /api/v1/pipelines/schedules/{scheduleId}
        """
        resp = await self._t.request("GET", f"/api/v1/pipelines/schedules/{schedule_id}")
        return resp.json()

    async def create_fire(
        self,
        fire_id: str,
        *,
        template_id: str,
        scope: str,
        scope_id: str,
        trigger_id: str,
        arguments: dict[str, Any] | None = None,
    ) -> None:
        """Create a pipeline fire (run instance).

        POST /api/v1/pipelines/fires/{fireId}
        """
        body: dict[str, Any] = {
            "pipelineTemplateId": template_id,
            "scope": scope,
            "scopeId": scope_id,
            "triggerId": trigger_id,
        }
        if arguments:
            body["arguments"] = arguments
        await self._t.request("POST", f"/api/v1/pipelines/fires/{fire_id}", json=body)
