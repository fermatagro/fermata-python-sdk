from enum import Enum


class ModelsTaskStatus(str, Enum):
    CANCELED = "canceled"
    DONE = "done"
    FAILED = "failed"
    PENDING = "pending"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)
