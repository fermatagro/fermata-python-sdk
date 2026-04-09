from enum import Enum


class ModelsPresetLevel(str, Enum):
    GC = "gc"
    MODEL = "model"
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
