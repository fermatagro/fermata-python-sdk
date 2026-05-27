"""Traceback filtering for uncaught FermataError exceptions.

Installed at import time. Chains to the previous ``sys.excepthook``. When an
uncaught ``FermataError`` reaches the top level, drops frames inside the SDK
(``fermata/``) and httpx/httpcore transport layers from the printed traceback,
leaving only user code + asyncio frames + the error message.

Caught exceptions are untouched — ``exc.__traceback__`` always contains the
full chain for introspection.

Disabled by setting ``FERMATA_DEBUG=1`` (full chain shown).
"""

from __future__ import annotations

import os
import sys
from types import FrameType, TracebackType

import httpcore
import httpx

from fermata.exceptions import FermataError

_FERMATA_DIR = os.path.dirname(os.path.abspath(__file__))
_HTTPX_DIR = os.path.dirname(os.path.abspath(httpx.__file__))
_HTTPCORE_DIR = os.path.dirname(os.path.abspath(httpcore.__file__))
_INTERNAL_DIRS = (_FERMATA_DIR, _HTTPX_DIR, _HTTPCORE_DIR)


def _is_internal(filename: str) -> bool:
    try:
        abs_path = os.path.abspath(filename)
    except (OSError, ValueError):
        return False
    return any(abs_path.startswith(d + os.sep) for d in _INTERNAL_DIRS)


def _filter_traceback(tb: TracebackType | None) -> TracebackType | None:
    """Build a new traceback chain that omits SDK + transport internal frames."""
    if tb is None:
        return None

    keep: list[tuple[FrameType, int, int]] = []
    cur: TracebackType | None = tb
    while cur is not None:
        if not _is_internal(cur.tb_frame.f_code.co_filename):
            keep.append((cur.tb_frame, cur.tb_lasti, cur.tb_lineno))
        cur = cur.tb_next

    new_tb: TracebackType | None = None
    for frame, lasti, lineno in reversed(keep):
        new_tb = TracebackType(new_tb, frame, lasti, lineno)
    return new_tb


def _debug_enabled() -> bool:
    return os.environ.get("FERMATA_DEBUG", "").lower() in ("1", "true", "yes")


def install() -> None:
    """Install the chained excepthook. Safe to call multiple times — no-op if already installed."""
    if getattr(sys.excepthook, "_fermata_installed", False):
        return

    previous = sys.excepthook

    def fermata_excepthook(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: TracebackType | None,
    ) -> None:
        if isinstance(exc_value, FermataError) and not _debug_enabled():
            exc_tb = _filter_traceback(exc_tb)
            # Modern Python's default printer reads exc_value.__traceback__, ignoring exc_tb.
            exc_value.__traceback__ = exc_tb
        previous(exc_type, exc_value, exc_tb)

    fermata_excepthook._fermata_installed = True  # type: ignore[attr-defined]
    sys.excepthook = fermata_excepthook
