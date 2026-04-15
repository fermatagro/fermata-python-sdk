from __future__ import annotations

from typing import Any

from fermata._call import call_async, call_sync
from fermata._generated.greenhouses.api.greenhouses import list_greenhouses as _list_greenhouses
from fermata._generated.greenhouses.models.models_greenhouse import ModelsGreenhouse


class AsyncGreenhouses:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def list(self) -> list[ModelsGreenhouse]:
        page = await call_async(_list_greenhouses.asyncio_detailed(client=self._c))
        return page.items


class SyncGreenhouses:
    def __init__(self, client: Any) -> None:
        self._c = client

    def list(self) -> list[ModelsGreenhouse]:
        page = call_sync(_list_greenhouses.sync_detailed(client=self._c))
        return page.items
