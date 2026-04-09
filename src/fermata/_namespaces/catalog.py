from __future__ import annotations

from fermata._generated.catalog.models.models_ai_model import ModelsAIModel
from fermata._transport import Transport


class AsyncModels:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    async def list(self) -> list[ModelsAIModel]:
        resp = await self._t.request("GET", "/api/v1/models")
        return [ModelsAIModel.from_dict(item) for item in resp.json()]

    async def get(self, name: str) -> ModelsAIModel:
        resp = await self._t.request("GET", f"/api/v1/models/by-name/{name}")
        return ModelsAIModel.from_dict(resp.json())
