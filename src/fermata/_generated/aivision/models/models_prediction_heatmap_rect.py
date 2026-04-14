from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.common_types_grid_rect import CommonTypesGridRect
  from ..models.common_types_ptz import CommonTypesPTZ
  from ..models.models_prediction_heatmap_class import ModelsPredictionHeatmapClass





T = TypeVar("T", bound="ModelsPredictionHeatmapRect")



@_attrs_define
class ModelsPredictionHeatmapRect:
    """ 
        Attributes:
            rect (CommonTypesGridRect): Rectangular area on the greenhouse grid
            predictions (list[ModelsPredictionHeatmapClass]):
            ptz (CommonTypesPTZ | Unset): Pan-Tilt-Zoom camera position. Pan and tilt are in radians.
     """

    rect: CommonTypesGridRect
    predictions: list[ModelsPredictionHeatmapClass]
    ptz: CommonTypesPTZ | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.common_types_grid_rect import CommonTypesGridRect
        from ..models.common_types_ptz import CommonTypesPTZ
        from ..models.models_prediction_heatmap_class import ModelsPredictionHeatmapClass
        rect = self.rect.to_dict()

        predictions = []
        for predictions_item_data in self.predictions:
            predictions_item = predictions_item_data.to_dict()
            predictions.append(predictions_item)



        ptz: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ptz, Unset):
            ptz = self.ptz.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "rect": rect,
            "predictions": predictions,
        })
        if ptz is not UNSET:
            field_dict["ptz"] = ptz

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.common_types_grid_rect import CommonTypesGridRect
        from ..models.common_types_ptz import CommonTypesPTZ
        from ..models.models_prediction_heatmap_class import ModelsPredictionHeatmapClass
        d = dict(src_dict)
        rect = CommonTypesGridRect.from_dict(d.pop("rect"))




        predictions = []
        _predictions = d.pop("predictions")
        for predictions_item_data in (_predictions):
            predictions_item = ModelsPredictionHeatmapClass.from_dict(predictions_item_data)



            predictions.append(predictions_item)


        _ptz = d.pop("ptz", UNSET)
        ptz: CommonTypesPTZ | Unset
        if isinstance(_ptz,  Unset):
            ptz = UNSET
        else:
            ptz = CommonTypesPTZ.from_dict(_ptz)




        models_prediction_heatmap_rect = cls(
            rect=rect,
            predictions=predictions,
            ptz=ptz,
        )


        models_prediction_heatmap_rect.additional_properties = d
        return models_prediction_heatmap_rect

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
