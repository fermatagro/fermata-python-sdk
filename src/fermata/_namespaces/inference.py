from __future__ import annotations

from collections.abc import Callable
from typing import Any
from uuid import UUID

from fermata._call import call_async
from fermata._generated.aivision.api.inference_api import (
    get_inference_task as _get_task,
)
from fermata._generated.aivision.api.inference_api import (
    submit_inference as _submit,
)
from fermata._generated.aivision.models.models_inference_request import ModelsInferenceRequest
from fermata._generated.aivision.models.models_inference_response import ModelsInferenceResponse
from fermata._generated.aivision.models.models_task import ModelsTask


class AsyncInference:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def submit(self, photo_id: str, model_name: str) -> str:
        body = ModelsInferenceRequest(photo_id=UUID(photo_id), model_name=model_name)
        result: ModelsInferenceResponse = await call_async(_submit.asyncio_detailed(body=body, client=self._c))
        return str(result.task_id)

    async def get(self, task_id: str) -> ModelsTask:
        return await call_async(_get_task.asyncio_detailed(UUID(task_id), client=self._c))


class SyncInference:
    def __init__(self, async_ns: AsyncInference, run: Callable[..., Any]) -> None:
        self._a = async_ns
        self._run = run

    def submit(self, photo_id: str, model_name: str) -> str:
        return self._run(self._a.submit(photo_id, model_name))

    def get(self, task_id: str) -> ModelsTask:
        return self._run(self._a.get(task_id))
