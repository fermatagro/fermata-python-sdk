from enum import Enum

class ModelsScheduleType(str, Enum):
    CLOUD = "cloud"
    ONSITE = "onsite"

    def __str__(self) -> str:
        return str(self.value)
