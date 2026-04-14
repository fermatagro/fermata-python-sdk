from __future__ import annotations

from typing import Any

from fermata._transport import Transport


class AsyncCultivation:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    async def list_active_cycles(
        self, greenhouse_id: str, at_time: str
    ) -> list[dict[str, Any]]:
        """List growing cycles active at a given time for a greenhouse.

        GET /api/v1/cycles/active?greenhouseId={id}&atTime={iso_timestamp}
        """
        resp = await self._t.request(
            "GET",
            "/api/v1/cycles/active",
            params={"greenhouseId": greenhouse_id, "atTime": at_time},
        )
        data = resp.json()
        return data.get("items", [])
