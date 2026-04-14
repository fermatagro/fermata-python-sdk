"""Stable re-exports of generated model types.

Import from here instead of `fermata._generated.*` — these names are the public API.
"""

from dataclasses import dataclass

from fermata._generated.aivision.models.models_task import ModelsTask as InferenceTask
from fermata._generated.aivision.models.models_task_status import ModelsTaskStatus as TaskStatus
from fermata._generated.catalog.models.models_ai_model import ModelsAIModel as Model
from fermata._generated.observations.models.models_photo import ModelsPhoto as Photo
from fermata._generated.observations.models.models_upload_link_response import (
    ModelsUploadLinkResponse as UploadLink,
)


@dataclass(frozen=True)
class PipelineRun:
    """Resolved pipeline context for the current scan session."""

    run_id: str
    greenhouse_id: str
    growing_cycle_id: str | None
    model_name: str
    organization_id: str


__all__ = [
    "Photo",
    "UploadLink",
    "InferenceTask",
    "TaskStatus",
    "Model",
    "PipelineRun",
]
