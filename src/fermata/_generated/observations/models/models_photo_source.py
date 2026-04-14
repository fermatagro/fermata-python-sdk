from enum import Enum

class ModelsPhotoSource(str, Enum):
    HUMAN = "human"
    PIPELINE = "pipeline"

    def __str__(self) -> str:
        return str(self.value)
