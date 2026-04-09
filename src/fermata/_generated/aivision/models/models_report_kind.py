from enum import Enum


class ModelsReportKind(str, Enum):
    CUSTOM = "custom"
    DAILY = "daily"
    WEEKLY = "weekly"
    WRAPPED = "wrapped"

    def __str__(self) -> str:
        return str(self.value)
