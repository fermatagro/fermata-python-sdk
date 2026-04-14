""" Contains all the data models used in inputs/outputs """

from .common_errors_api_error import CommonErrorsApiError
from .common_types_grid_pos import CommonTypesGridPos
from .common_types_grid_rect import CommonTypesGridRect
from .common_types_ptz import CommonTypesPTZ
from .common_types_time_range import CommonTypesTimeRange
from .create_or_update_report import CreateOrUpdateReport
from .create_or_update_threshold_preset import CreateOrUpdateThresholdPreset
from .create_or_update_threshold_preset_values import CreateOrUpdateThresholdPresetValues
from .list_predictions_for_gallery_response_200 import ListPredictionsForGalleryResponse200
from .list_predictions_response_200 import ListPredictionsResponse200
from .list_presets_response_200 import ListPresetsResponse200
from .list_reports_response_200 import ListReportsResponse200
from .models_affected_area import ModelsAffectedArea
from .models_affecting_class import ModelsAffectingClass
from .models_covered_area import ModelsCoveredArea
from .models_hide_predictions_request import ModelsHidePredictionsRequest
from .models_inference_request import ModelsInferenceRequest
from .models_inference_response import ModelsInferenceResponse
from .models_inference_task_payload import ModelsInferenceTaskPayload
from .models_precomputed_prediction import ModelsPrecomputedPrediction
from .models_prediction import ModelsPrediction
from .models_prediction_count import ModelsPredictionCount
from .models_prediction_heatmap import ModelsPredictionHeatmap
from .models_prediction_heatmap_class import ModelsPredictionHeatmapClass
from .models_prediction_heatmap_rect import ModelsPredictionHeatmapRect
from .models_prediction_query import ModelsPredictionQuery
from .models_preset_level import ModelsPresetLevel
from .models_preset_type import ModelsPresetType
from .models_report import ModelsReport
from .models_report_kind import ModelsReportKind
from .models_set_preset_name_request import ModelsSetPresetNameRequest
from .models_task import ModelsTask
from .models_task_status import ModelsTaskStatus
from .models_threshold_preset import ModelsThresholdPreset
from .models_threshold_preset_values import ModelsThresholdPresetValues
from .models_time_bucket import ModelsTimeBucket
from .models_unhide_predictions_request import ModelsUnhidePredictionsRequest
from .models_update_preset_values_request import ModelsUpdatePresetValuesRequest
from .models_update_preset_values_request_values import ModelsUpdatePresetValuesRequestValues
from .models_upload_predictions_request import ModelsUploadPredictionsRequest
from .models_upload_predictions_response import ModelsUploadPredictionsResponse
from .models_vertex import ModelsVertex

__all__ = (
    "CommonErrorsApiError",
    "CommonTypesGridPos",
    "CommonTypesGridRect",
    "CommonTypesPTZ",
    "CommonTypesTimeRange",
    "CreateOrUpdateReport",
    "CreateOrUpdateThresholdPreset",
    "CreateOrUpdateThresholdPresetValues",
    "ListPredictionsForGalleryResponse200",
    "ListPredictionsResponse200",
    "ListPresetsResponse200",
    "ListReportsResponse200",
    "ModelsAffectedArea",
    "ModelsAffectingClass",
    "ModelsCoveredArea",
    "ModelsHidePredictionsRequest",
    "ModelsInferenceRequest",
    "ModelsInferenceResponse",
    "ModelsInferenceTaskPayload",
    "ModelsPrecomputedPrediction",
    "ModelsPrediction",
    "ModelsPredictionCount",
    "ModelsPredictionHeatmap",
    "ModelsPredictionHeatmapClass",
    "ModelsPredictionHeatmapRect",
    "ModelsPredictionQuery",
    "ModelsPresetLevel",
    "ModelsPresetType",
    "ModelsReport",
    "ModelsReportKind",
    "ModelsSetPresetNameRequest",
    "ModelsTask",
    "ModelsTaskStatus",
    "ModelsThresholdPreset",
    "ModelsThresholdPresetValues",
    "ModelsTimeBucket",
    "ModelsUnhidePredictionsRequest",
    "ModelsUpdatePresetValuesRequest",
    "ModelsUpdatePresetValuesRequestValues",
    "ModelsUploadPredictionsRequest",
    "ModelsUploadPredictionsResponse",
    "ModelsVertex",
)
