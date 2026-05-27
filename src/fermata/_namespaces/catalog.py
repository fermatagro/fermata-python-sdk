from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fermata._call import call_async
from fermata._generated.catalog.api.ai_models_api import (
    get_ai_model_by_name as _get_model,
)
from fermata._generated.catalog.api.ai_models_api import (
    list_ai_models as _list_models,
)
from fermata._generated.catalog.models.models_ai_model import ModelsAIModel


class AsyncModels:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def list(self) -> list[ModelsAIModel]:
        return await call_async(_list_models.asyncio_detailed(client=self._c))

    async def get(self, name: str) -> ModelsAIModel:
        return await call_async(_get_model.asyncio_detailed(name, client=self._c))


class SyncModels:
    def __init__(self, async_ns: AsyncModels, run: Callable[..., Any]) -> None:
        self._a = async_ns
        self._run = run

    def list(self) -> list[ModelsAIModel]:
        return self._run(self._a.list())

    def get(self, name: str) -> ModelsAIModel:
        return self._run(self._a.get(name))
