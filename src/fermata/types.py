"""Stable re-exports of generated model types.

Import from here instead of `fermata._generated.*` — these names are the public API.
"""

from fermata._generated.observations.models.models_photo import ModelsPhoto as Photo
from fermata._generated.observations.models.models_upload_link_response import (
    ModelsUploadLinkResponse as UploadLink,
)
from fermata._generated.aivision.models.models_task import ModelsTask as InferenceTask
from fermata._generated.aivision.models.models_task_status import ModelsTaskStatus as TaskStatus
from fermata._generated.catalog.models.models_ai_model import ModelsAIModel as Model

__all__ = [
    "Photo",
    "UploadLink",
    "InferenceTask",
    "TaskStatus",
    "Model",
]
