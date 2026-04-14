from enum import Enum


class ModelsGreenhouseObjectType(str, Enum):
    BLOCK = "block"
    EXIT = "exit"
    ROW = "row"

    def __str__(self) -> str:
        return str(self.value)
