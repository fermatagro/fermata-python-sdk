"""Integration tests for scan progress against real Hera in docker-compose.

Run with: .venv/bin/pytest tests/integration/test_scan_progress.py -v

Requires the on-site docker-compose stack to be running, with a Hera built from
demetra aivision >= 3.1.0 (older builds have no pipeline-status route):
  docker compose -f fermata-onsite/deploy/docker-compose.yml up -d
"""
from __future__ import annotations

import asyncio
import os

import pytest
from uuid_utils import uuid7

from fermata import Fermata
from fermata.exceptions import NotFoundError

HERA_URL = os.environ.get("HERA_URL", "http://172.28.0.10:3000")
APP_ID = os.environ.get("HERA_APP_ID", "viscon-onsite-01")
APP_SECRET = os.environ.get("HERA_APP_SECRET", "change-me-in-production")

GREENHOUSE_ID = os.environ.get("SDK_TEST_GREENHOUSE_ID")
MODEL_NAME = os.environ.get("SDK_TEST_MODEL_NAME")
DEVICE_ID = os.environ.get("SDK_TEST_DEVICE_ID")
BATCH = int(os.environ.get("SDK_TEST_SCAN_BATCH", "3"))
POLL_TIMEOUT = float(os.environ.get("SDK_TEST_SCAN_TIMEOUT", "120"))

# 1x1 JPEG, enough for the pipeline to accept an upload.
_PIXEL = bytes.fromhex(
    "ffd8ffe000104a46494600010100000100010000ffdb004300ff"
    "c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9c9"
)


@pytest.fixture
async def client():
    async with Fermata(HERA_URL, APP_ID, APP_SECRET) as f:
        yield f


async def test_unknown_scan_raises_not_found(client):
    """A scan nobody submitted to is indistinguishable from a foreign one: 404."""
    with pytest.raises(NotFoundError) as excinfo:
        await client.scan_progress(str(uuid7()))

    # Also the signal for a Hera older than aivision 3.1.0, which has no such route.
    assert "aivision 3.1.0" in str(excinfo.value)


@pytest.mark.skipif(
    not (GREENHOUSE_ID and MODEL_NAME and DEVICE_ID),
    reason=(
        "set SDK_TEST_GREENHOUSE_ID, SDK_TEST_MODEL_NAME and SDK_TEST_DEVICE_ID to run the "
        "bulk-send test; it also needs a reachable ML API, since submitInference validates "
        "the model and tasks only leave 'pending' once inference resolves"
    ),
)
async def test_scan_progress_drains_to_zero(client):
    """Bulk-send a batch, then poll the scan until nothing is pending."""
    for i in range(BATCH):
        await client.infer(
            image=_PIXEL,
            captured_at=f"2026-04-01T10:00:{i:02d}Z",
            greenhouse_id=GREENHOUSE_ID,
            model_name=MODEL_NAME,
            device_id=DEVICE_ID,
            position={"x": float(i), "y": 0.0, "h": 0.0},
        )

    progress = await client.scan_progress()
    assert progress.scan_id == client.scan_id
    assert progress.pending > 0

    deadline = asyncio.get_running_loop().time() + POLL_TIMEOUT
    while not progress.finished:
        assert asyncio.get_running_loop().time() < deadline, (
            f"scan {client.scan_id} still had {progress.pending} pending after {POLL_TIMEOUT}s"
        )
        await asyncio.sleep(2)
        progress = await client.scan_progress()

    assert progress.pending == 0
    assert progress.finished
