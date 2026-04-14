from __future__ import annotations

from typing import Any

from fermata._call import call_async, call_sync
from fermata._generated.catalog.api.ai_models import (
    get_ai_model_by_name as _get_model,
)
from fermata._generated.catalog.api.ai_models import (
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
    def __init__(self, client: Any) -> None:
        self._c = client

    def list(self) -> list[ModelsAIModel]:
        return call_sync(_list_models.sync_detailed(client=self._c))

    def get(self, name: str) -> ModelsAIModel:
        return call_sync(_get_model.sync_detailed(name, client=self._c))
