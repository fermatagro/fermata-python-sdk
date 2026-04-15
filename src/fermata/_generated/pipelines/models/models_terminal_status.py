from enum import Enum


class ModelsTerminalStatus(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"
    SKIPPED = "skipped"

    def __str__(self) -> str:
        return str(self.value)
