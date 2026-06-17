from __future__ import annotations

import json

import httpx
import respx

MINIO_URL_PATTERN = r"http://minio:9000/.*"


def _upload_link_handler(request):
    photo_id = str(request.url).split("/photos/")[1].split("/upload-link")[0]
    return httpx.Response(200, json={
        "photoId": photo_id,
        "uploadUrl": "http://minio:9000/bucket/photo?presigned=true",
        "downloadUrl": "http://minio:9000/bucket/photo?download=true",
        "deleteUrl": "http://minio:9000/bucket/photo?delete=true",
        "expiresAt": "2026-04-01T12:00:00Z",
    })


async def test_infer_full_flow(client, mock_hera):
    """Test the full infer() convenience method."""
    mock_hera.post(url__regex=r"/api/v1/photos/.+/upload-link").mock(side_effect=_upload_link_handler)
    mock_hera.post(url__regex=r"/api/v1/photos/[0-9a-f-]+$").respond(201)
    mock_hera.get("/api/v1/models").respond(200, json=[
        {"modelName": "tomato-v3", "modelType": "detection", "isActive": True}
    ])
    mock_hera.post("/api/v1/inference").respond(202, json={
        "taskId": "00000000-0000-0000-0000-000000000099",
    })

    with respx.mock() as minio_router:
        minio_router.put(url__regex=MINIO_URL_PATTERN).respond(200)

        task_id = await client.infer(
            image=b"fake-jpeg-bytes",
            greenhouse_id="00000000-0000-0000-0000-000000000010",
            captured_at="2026-04-01T10:00:00Z",
            position={"x": 1.0, "y": 2.0, "h": 0.5},
        )

    assert task_id == "00000000-0000-0000-0000-000000000099"


async def test_infer_with_explicit_model(client, mock_hera):
    """When model_name is provided, skip the models list call."""
    mock_hera.post(url__regex=r"/api/v1/photos/.+/upload-link").mock(side_effect=_upload_link_handler)
    mock_hera.post(url__regex=r"/api/v1/photos/[0-9a-f-]+$").respond(201)
    mock_hera.post("/api/v1/inference").respond(202, json={
        "taskId": "00000000-0000-0000-0000-000000000099",
    })

    with respx.mock() as minio_router:
        minio_router.put(url__regex=MINIO_URL_PATTERN).respond(200)

        task_id = await client.infer(
            image=b"fake-jpeg-bytes",
            greenhouse_id="00000000-0000-0000-0000-000000000010",
            captured_at="2026-04-01T10:00:00Z",
            model_name="tomato-v3",
        )

    assert task_id == "00000000-0000-0000-0000-000000000099"


async def test_infer_persists_metadata(client, mock_hera):
    """metadata passed to infer() is serialized into the create-photo body."""
    mock_hera.post(url__regex=r"/api/v1/photos/.+/upload-link").mock(side_effect=_upload_link_handler)
    create_route = mock_hera.post(url__regex=r"/api/v1/photos/[0-9a-f-]+$").respond(201)
    mock_hera.post("/api/v1/inference").respond(202, json={
        "taskId": "00000000-0000-0000-0000-000000000099",
    })

    with respx.mock() as minio_router:
        minio_router.put(url__regex=MINIO_URL_PATTERN).respond(200)

        await client.infer(
            image=b"fake-jpeg-bytes",
            greenhouse_id="00000000-0000-0000-0000-000000000010",
            captured_at="2026-04-01T10:00:00Z",
            model_name="tomato-v3",
            metadata={"resolution": "4000x3000", "format": "jpeg", "exposure_ms": 12.5},
        )

    body = json.loads(create_route.calls.last.request.content)
    assert body["metadata"] == {"resolution": "4000x3000", "format": "jpeg", "exposure_ms": 12.5}


async def test_infer_omits_metadata_when_absent(client, mock_hera):
    """No metadata field is sent when none is provided."""
    mock_hera.post(url__regex=r"/api/v1/photos/.+/upload-link").mock(side_effect=_upload_link_handler)
    create_route = mock_hera.post(url__regex=r"/api/v1/photos/[0-9a-f-]+$").respond(201)
    mock_hera.post("/api/v1/inference").respond(202, json={
        "taskId": "00000000-0000-0000-0000-000000000099",
    })

    with respx.mock() as minio_router:
        minio_router.put(url__regex=MINIO_URL_PATTERN).respond(200)

        await client.infer(
            image=b"fake-jpeg-bytes",
            greenhouse_id="00000000-0000-0000-0000-000000000010",
            captured_at="2026-04-01T10:00:00Z",
            model_name="tomato-v3",
        )

    body = json.loads(create_route.calls.last.request.content)
    assert "metadata" not in body


async def test_scan_id_is_set(client):
    """Client should have a scan_id property."""
    assert client.scan_id
    assert len(client.scan_id) == 36  # UUIDv7 string


def test_sync_scan_id(sync_client):
    """Sync client should expose scan_id."""
    assert sync_client.scan_id
    assert len(sync_client.scan_id) == 36
