from enum import Enum


class ModelsZoneObjectBatchErrorCode(str, Enum):
    VALIDATIONERROR = "ValidationError"

    def __str__(self) -> str:
        return str(self.value)
