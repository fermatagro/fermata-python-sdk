from enum import Enum


class ModelsScheduleScope(str, Enum):
    GREENHOUSE = "greenhouse"
    GROWING_CYCLE = "growing_cycle"

    def __str__(self) -> str:
        return str(self.value)
