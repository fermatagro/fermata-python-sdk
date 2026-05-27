from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fermata._call import call_async
from fermata._generated.greenhouses.api.greenhouse_api import list_greenhouses as _list_greenhouses
from fermata._generated.greenhouses.models.models_greenhouse import ModelsGreenhouse


class AsyncGreenhouses:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def list(self) -> list[ModelsGreenhouse]:
        page = await call_async(_list_greenhouses.asyncio_detailed(client=self._c))
        return page.items


class SyncGreenhouses:
    def __init__(self, async_ns: AsyncGreenhouses, run: Callable[..., Any]) -> None:
        self._a = async_ns
        self._run = run

    def list(self) -> list[ModelsGreenhouse]:
        return self._run(self._a.list())
