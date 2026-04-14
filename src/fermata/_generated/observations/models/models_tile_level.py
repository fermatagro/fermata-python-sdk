from enum import Enum

class ModelsTileLevel(str, Enum):
    L0 = "l0"
    L1 = "l1"
    L2 = "l2"

    def __str__(self) -> str:
        return str(self.value)
