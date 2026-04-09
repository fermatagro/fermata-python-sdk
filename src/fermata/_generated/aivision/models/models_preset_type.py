from enum import Enum


class ModelsPresetType(str, Enum):
    BALANCE = "balance"
    EXPERIMENTAL = "experimental"
    PRECISION = "precision"
    RECALL = "recall"

    def __str__(self) -> str:
        return str(self.value)
