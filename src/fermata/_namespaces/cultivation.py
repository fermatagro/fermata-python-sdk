from __future__ import annotations

from fermata._generated.cultivation.models.list_active_cycles_at_time_response_200 import (
    ListActiveCyclesAtTimeResponse200,
)
from fermata._generated.cultivation.models.models_growing_cycle import ModelsGrowingCycle
from fermata._transport import Transport


class AsyncCultivation:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    async def get_cycle(self, cycle_id: str) -> ModelsGrowingCycle:
        """Fetch a growing cycle by ID.

        GET /api/v1/cycles/{cycleId}
        """
        resp = await self._t.request("GET", f"/api/v1/cycles/{cycle_id}")
        return ModelsGrowingCycle.from_dict(resp.json())

    async def list_active_cycles(
        self, greenhouse_id: str, at_time: str
    ) -> list[ModelsGrowingCycle]:
        """List growing cycles active at a given time for a greenhouse.

        GET /api/v1/cycles/active?greenhouseId={id}&atTime={iso_timestamp}
        """
        resp = await self._t.request(
            "GET",
            "/api/v1/cycles/active",
            params={"greenhouseId": greenhouse_id, "atTime": at_time},
        )
        page = ListActiveCyclesAtTimeResponse200.from_dict(resp.json())
        return page.items
