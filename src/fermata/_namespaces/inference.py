from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any
from uuid import UUID

from fermata._call import call_async
from fermata._generated.aivision.api.inference_api import (
    get_inference_pipeline_status as _get_pipeline_status,
)
from fermata._generated.aivision.api.inference_api import (
    get_inference_task as _get_task,
)
from fermata._generated.aivision.api.inference_api import (
    submit_inference as _submit,
)
from fermata._generated.aivision.models.models_inference_request import ModelsInferenceRequest
from fermata._generated.aivision.models.models_inference_response import ModelsInferenceResponse
from fermata._generated.aivision.models.models_pipeline_status import ModelsPipelineStatus
from fermata._generated.aivision.models.models_task import ModelsTask
from fermata.exceptions import NotFoundError
from fermata.types import ScanProgress

_SCAN_404 = (
    "No inference tasks found for scan {scan_id}. Either nothing was submitted under this "
    "scan id, or the server is older than aivision 3.1.0 and does not serve "
    "GET /api/v1/inference/pipeline/{{pipelineId}}/status."
)


class AsyncInference:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def submit(self, photo_id: str, model_name: str) -> str:
        body = ModelsInferenceRequest(photo_id=UUID(photo_id), model_name=model_name)
        result: ModelsInferenceResponse = await call_async(_submit.asyncio_detailed(body=body, client=self._c))
        return str(result.task_id)

    async def get(self, task_id: str) -> ModelsTask:
        return await call_async(_get_task.asyncio_detailed(UUID(task_id), client=self._c))

    async def scan_progress(self, scan_id: str) -> ScanProgress:
        """Count the inference tasks of a scan that are still pending.

        The scan id travels to the server as the photos' ``pipeline_id``.
        """
        try:
            status: ModelsPipelineStatus = await call_async(
                _get_pipeline_status.asyncio_detailed(UUID(scan_id), client=self._c)
            )
        except NotFoundError as exc:
            raise NotFoundError(
                _SCAN_404.format(scan_id=scan_id),
                status_code=exc.status_code,
                request_id=exc.request_id,
            ) from exc
        except json.JSONDecodeError as exc:
            # Servers without this route answer it with a plain-text router 404,
            # which the generated parser cannot decode into the error model.
            raise NotFoundError(_SCAN_404.format(scan_id=scan_id), status_code=404) from exc
        return ScanProgress(scan_id=str(status.pipeline_id), pending=status.pending)


class SyncInference:
    def __init__(self, async_ns: AsyncInference, run: Callable[..., Any]) -> None:
        self._a = async_ns
        self._run = run

    def submit(self, photo_id: str, model_name: str) -> str:
        return self._run(self._a.submit(photo_id, model_name))

    def get(self, task_id: str) -> ModelsTask:
        return self._run(self._a.get(task_id))

    def scan_progress(self, scan_id: str) -> ScanProgress:
        return self._run(self._a.scan_progress(scan_id))
