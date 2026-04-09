from enum import Enum


class ModelsTileFace(str, Enum):
    B = "b"
    D = "d"
    F = "f"
    L = "l"
    R = "r"
    U = "u"

    def __str__(self) -> str:
        return str(self.value)
