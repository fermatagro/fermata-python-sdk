from enum import Enum

class ModelsAIModelType(str, Enum):
    CLASSIFICATION = "classification"
    DETECTION = "detection"
    SEGMENTATION = "segmentation"

    def __str__(self) -> str:
        return str(self.value)
