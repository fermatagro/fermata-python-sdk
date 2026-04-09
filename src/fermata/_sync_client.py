from __future__ import annotations

import asyncio
import datetime
import threading
from pathlib import Path
from typing import Any, Self

from fermata._client import Fermata


class _SyncNamespace:
    """Base for sync namespace wrappers."""

    def __init__(self, async_ns: Any, run: Any) -> None:
        self._async = async_ns
        self._run = run


class SyncPhotos(_SyncNamespace):
    def upload_link(self, photo_id: str, captured_at: str | datetime.datetime) -> Any:
        return self._run(self._async.upload_link(photo_id, captured_at))

    def upload(self, upload_url: str, image: str | Path | bytes) -> None:
        self._run(self._async.upload(upload_url, image))

    def create(self, photo_id: str, **kwargs: Any) -> Any:
        return self._run(self._async.create(photo_id, **kwargs))


class SyncInference(_SyncNamespace):
    def submit(self, photo_id: str, model_name: str) -> str:
        return self._run(self._async.submit(photo_id, model_name))

    def get(self, task_id: str) -> Any:
        return self._run(self._async.get(task_id))


class FermataSync:
    """Sync Fermata SDK client.

    Each instance represents a single scan session. All photos submitted
    through the same instance are grouped under the same scan_id.

    Usage:
        with FermataSync(url="http://localhost:3000", username="...", password="...") as f:
            task_id = f.infer(image="photo.jpg", greenhouse_id="gh-01", captured_at="...")
    """

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        *,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()

        self._async = Fermata(url, username, password, timeout=timeout, max_retries=max_retries)

        self.photos = SyncPhotos(self._async.photos, self._run)
        self.inference = SyncInference(self._async.inference, self._run)

    @property
    def scan_id(self) -> str:
        """Unique ID for this scan session. Auto-generated on construction."""
        return self._async.scan_id

    def _run(self, coro: Any) -> Any:
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def __enter__(self) -> Self:
        self._run(self._async.__aenter__())
        return self

    def __exit__(self, *exc: Any) -> None:
        self._run(self._async.__aexit__(*exc))
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=5)

    def infer(
        self,
        image: str | Path | bytes,
        greenhouse_id: str,
        captured_at: str | datetime.datetime,
        *,
        position: dict[str, float] | None = None,
        model_name: str | None = None,
        photo_id: str | None = None,
    ) -> str:
        return self._run(
            self._async.infer(
                image,
                greenhouse_id,
                captured_at,
                position=position,
                model_name=model_name,
                photo_id=photo_id,
            )
        )
