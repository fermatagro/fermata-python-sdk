from __future__ import annotations

from collections.abc import Callable
from typing import Any
from uuid import UUID

from fermata._call import call_async
from fermata._generated.greenhouses.api.greenhouse_objects_api import (
    get_greenhouse_object as _get_greenhouse_object,
)
from fermata._generated.greenhouses.api.greenhouse_objects_api import (
    list_greenhouse_objects as _list_greenhouse_objects,
)
from fermata._generated.greenhouses.models.models_greenhouse_object import ModelsGreenhouseObject
from fermata._generated.greenhouses.types import UNSET, Unset


class AsyncGreenhouseObjects:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def list(self, greenhouse_id: str) -> list[ModelsGreenhouseObject]:
        """List all physical objects (rows, blocks) of a greenhouse, following pagination."""
        items: list[ModelsGreenhouseObject] = []
        cursor: str | Unset = UNSET
        while True:
            page = await call_async(
                _list_greenhouse_objects.asyncio_detailed(
                    UUID(greenhouse_id), client=self._c, cursor=cursor
                )
            )
            items.extend(page.items)
            if isinstance(page.next_token, Unset) or not page.next_token:
                return items
            cursor = page.next_token

    async def get(self, greenhouse_id: str, object_id: int) -> ModelsGreenhouseObject:
        return await call_async(
            _get_greenhouse_object.asyncio_detailed(
                UUID(greenhouse_id), str(object_id), client=self._c
            )
        )


class SyncGreenhouseObjects:
    def __init__(self, async_ns: AsyncGreenhouseObjects, run: Callable[..., Any]) -> None:
        self._a = async_ns
        self._run = run

    def list(self, greenhouse_id: str) -> list[ModelsGreenhouseObject]:
        return self._run(self._a.list(greenhouse_id))

    def get(self, greenhouse_id: str, object_id: int) -> ModelsGreenhouseObject:
        return self._run(self._a.get(greenhouse_id, object_id))
