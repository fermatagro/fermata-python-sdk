from __future__ import annotations

import datetime
from collections.abc import Callable
from typing import Any
from uuid import UUID

from fermata._call import call_async
from fermata._generated.cultivation.api.cycles_api import (
    get_cycle as _get_cycle,
)
from fermata._generated.cultivation.api.cycles_api import (
    list_active_cycles_at_time as _list_active,
)
from fermata._generated.cultivation.models.models_growing_cycle import ModelsGrowingCycle


class AsyncCultivation:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def get_cycle(self, cycle_id: str) -> ModelsGrowingCycle:
        return await call_async(_get_cycle.asyncio_detailed(UUID(cycle_id), client=self._c))

    async def list_active_cycles(
        self, greenhouse_id: str, at_time: datetime.datetime
    ) -> list[ModelsGrowingCycle]:
        page = await call_async(
            _list_active.asyncio_detailed(client=self._c, greenhouse_id=UUID(greenhouse_id), at_time=at_time)
        )
        return page.items


class SyncCultivation:
    def __init__(self, async_ns: AsyncCultivation, run: Callable[..., Any]) -> None:
        self._a = async_ns
        self._run = run

    def get_cycle(self, cycle_id: str) -> ModelsGrowingCycle:
        return self._run(self._a.get_cycle(cycle_id))

    def list_active_cycles(self, greenhouse_id: str, at_time: datetime.datetime) -> list[ModelsGrowingCycle]:
        return self._run(self._a.list_active_cycles(greenhouse_id, at_time))
