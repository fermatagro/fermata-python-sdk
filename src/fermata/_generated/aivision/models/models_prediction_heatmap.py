from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.models_prediction_heatmap_rect import ModelsPredictionHeatmapRect





T = TypeVar("T", bound="ModelsPredictionHeatmap")



@_attrs_define
class ModelsPredictionHeatmap:
    """ 
        Attributes:
            time_range (datetime.datetime):
            boxes (list[ModelsPredictionHeatmapRect]):
     """

    time_range: datetime.datetime
    boxes: list[ModelsPredictionHeatmapRect]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.models_prediction_heatmap_rect import ModelsPredictionHeatmapRect
        time_range = self.time_range.isoformat()

        boxes = []
        for boxes_item_data in self.boxes:
            boxes_item = boxes_item_data.to_dict()
            boxes.append(boxes_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "timeRange": time_range,
            "boxes": boxes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.models_prediction_heatmap_rect import ModelsPredictionHeatmapRect
        d = dict(src_dict)
        time_range = isoparse(d.pop("timeRange"))




        boxes = []
        _boxes = d.pop("boxes")
        for boxes_item_data in (_boxes):
            boxes_item = ModelsPredictionHeatmapRect.from_dict(boxes_item_data)



            boxes.append(boxes_item)


        models_prediction_heatmap = cls(
            time_range=time_range,
            boxes=boxes,
        )


        models_prediction_heatmap.additional_properties = d
        return models_prediction_heatmap

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
