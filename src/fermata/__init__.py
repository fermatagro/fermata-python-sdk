"""Fermata Python SDK for Hera API."""

from fermata._client import Fermata
from fermata._excepthook import install as _install_excepthook
from fermata._sync_client import FermataSync
from fermata.exceptions import (
    AuthError,
    ConflictError,
    ConnectionError,
    FermataError,
    NotFoundError,
    ServerError,
    ValidationError,
)
from fermata.types import PipelineRun

_install_excepthook()

__all__ = [
    "Fermata",
    "FermataSync",
    "PipelineRun",
    "FermataError",
    "AuthError",
    "NotFoundError",
    "ConflictError",
    "ValidationError",
    "ServerError",
    "ConnectionError",
]
