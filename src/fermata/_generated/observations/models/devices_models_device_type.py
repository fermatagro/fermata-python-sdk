from enum import Enum


class DevicesModelsDeviceType(str, Enum):
    CAMERA = "camera"
    ROUTER = "router"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
