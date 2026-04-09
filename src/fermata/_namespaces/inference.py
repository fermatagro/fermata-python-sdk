from __future__ import annotations

from fermata._generated.aivision.models.models_inference_response import ModelsInferenceResponse
from fermata._generated.aivision.models.models_task import ModelsTask
from fermata._transport import Transport


class AsyncInference:
    def __init__(self, transport: Transport) -> None:
        self._t = transport

    async def submit(self, photo_id: str, model_name: str) -> str:
        resp = await self._t.request(
            "POST",
            "/api/v1/inference",
            json={"photoId": photo_id, "modelName": model_name},
        )
        result = ModelsInferenceResponse.from_dict(resp.json())
        return str(result.task_id)

    async def get(self, task_id: str) -> ModelsTask:
        resp = await self._t.request("GET", f"/api/v1/inference/task/{task_id}")
        return ModelsTask.from_dict(resp.json())
