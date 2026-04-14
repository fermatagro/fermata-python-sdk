from enum import Enum


class ModelsTriggerType(str, Enum):
    REQUEST = "request"
    SCHEDULE = "schedule"

    def __str__(self) -> str:
        return str(self.value)
