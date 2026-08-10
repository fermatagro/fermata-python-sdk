from __future__ import annotations

import httpx
import pytest

from fermata import NotFoundError, ScanProgress

SCAN_ID = "01920000-0000-7000-8000-000000000001"
OTHER_SCAN_ID = "01920000-0000-7000-8000-000000000002"


def _status_url(scan_id: str) -> str:
    return f"/api/v1/inference/pipeline/{scan_id}/status"


async def test_scan_progress_maps_payload(client, mock_hera):
    """The endpoint payload becomes a ScanProgress."""
    mock_hera.get(_status_url(client.scan_id)).respond(
        200, json={"pipelineId": client.scan_id, "pending": 688}
    )

    progress = await client.scan_progress()

    assert progress == ScanProgress(scan_id=client.scan_id, pending=688)
    assert not progress.finished


async def test_scan_progress_finished_at_zero(client, mock_hera):
    """pending == 0 means every task reached a terminal state."""
    mock_hera.get(_status_url(client.scan_id)).respond(
        200, json={"pipelineId": client.scan_id, "pending": 0}
    )

    progress = await client.scan_progress()

    assert progress.pending == 0
    assert progress.finished


async def test_scan_progress_defaults_to_current_scan(client, mock_hera):
    """Called without an argument, the client polls its own scan."""
    route = mock_hera.get(_status_url(client.scan_id)).respond(
        200, json={"pipelineId": client.scan_id, "pending": 3}
    )

    await client.scan_progress()

    assert route.called
    assert client.scan_id in str(route.calls.last.request.url)


async def test_scan_progress_honors_explicit_scan_id(client, mock_hera):
    """An explicit scan id wins over the client's own."""
    mock_hera.get(_status_url(OTHER_SCAN_ID)).respond(
        200, json={"pipelineId": OTHER_SCAN_ID, "pending": 7}
    )

    progress = await client.scan_progress(OTHER_SCAN_ID)

    assert progress.scan_id == OTHER_SCAN_ID
    assert progress.pending == 7


async def test_scan_progress_polls_to_zero(client, mock_hera):
    """A caller-written poll loop sees pending decrease to zero."""
    mock_hera.get(_status_url(SCAN_ID)).mock(
        side_effect=[
            httpx.Response(200, json={"pipelineId": SCAN_ID, "pending": 5}),
            httpx.Response(200, json={"pipelineId": SCAN_ID, "pending": 2}),
            httpx.Response(200, json={"pipelineId": SCAN_ID, "pending": 0}),
        ]
    )

    seen = []
    while True:
        progress = await client.scan_progress(SCAN_ID)
        seen.append(progress.pending)
        if progress.finished:
            break

    assert seen == [5, 2, 0]


async def test_scan_progress_404_is_actionable(client, mock_hera):
    """404 names both causes: unknown scan, or a server without the endpoint."""
    mock_hera.get(_status_url(SCAN_ID)).respond(
        404, json={"message": "pipeline not found", "request_id": "req-42"}
    )

    with pytest.raises(NotFoundError) as excinfo:
        await client.scan_progress(SCAN_ID)

    message = str(excinfo.value)
    assert SCAN_ID in message
    assert "aivision 3.1.0" in message
    assert excinfo.value.status_code == 404
    assert excinfo.value.request_id == "req-42"


async def test_scan_progress_404_on_plaintext_body(client, mock_hera):
    """An old server answers with a plain-text router 404, not JSON."""
    mock_hera.get(_status_url(SCAN_ID)).respond(404, text="404 page not found")

    with pytest.raises(NotFoundError) as excinfo:
        await client.scan_progress(SCAN_ID)

    assert "aivision 3.1.0" in str(excinfo.value)


async def test_scan_progress_namespace_method(client, mock_hera):
    """The namespace method takes an explicit scan id."""
    mock_hera.get(_status_url(SCAN_ID)).respond(
        200, json={"pipelineId": SCAN_ID, "pending": 1}
    )

    progress = await client.inference.scan_progress(SCAN_ID)

    assert progress == ScanProgress(scan_id=SCAN_ID, pending=1)


def test_sync_scan_progress(sync_client, mock_hera):
    """The sync client delegates and returns the same type."""
    mock_hera.get(_status_url(sync_client.scan_id)).respond(
        200, json={"pipelineId": sync_client.scan_id, "pending": 4}
    )

    progress = sync_client.scan_progress()

    assert progress == ScanProgress(scan_id=sync_client.scan_id, pending=4)


def test_sync_scan_progress_namespace(sync_client, mock_hera):
    """The sync namespace delegate works too."""
    mock_hera.get(_status_url(SCAN_ID)).respond(
        200, json={"pipelineId": SCAN_ID, "pending": 0}
    )

    progress = sync_client.inference.scan_progress(SCAN_ID)

    assert progress.finished
