from enum import Enum


class ModelsControlPointType(str, Enum):
    CONTROL = "control"
    REFERENCE = "reference"

    def __str__(self) -> str:
        return str(self.value)
