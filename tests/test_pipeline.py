from __future__ import annotations

import httpx
import pytest
import respx

from fermata import Fermata, FermataSync, PipelineRun
from fermata._client import _deterministic_photo_id

HERA_URL = "http://hera-test:3000"
USERNAME = "test-user"
PASSWORD = "test-password"
MINIO_URL_PATTERN = r"http://minio:9000/.*"

TOKEN_RESPONSE = {
    "access_token": "mock-jwt-token",
    "token_type": "Bearer",
    "expires_in": 3600,
}

SCHEDULE_ID = "00000000-0000-0000-0000-000000000100"
TEMPLATE_ID = "00000000-0000-0000-0000-000000000200"
GREENHOUSE_ID = "00000000-0000-0000-0000-000000000010"
CYCLE_ID = "00000000-0000-0000-0000-000000000020"
ORG_ID = "org_test"

SCHEDULE_RESPONSE = {
    "id": SCHEDULE_ID,
    "organizationId": ORG_ID,
    "templateId": TEMPLATE_ID,
    "scope": "growing_cycle",
    "scopeId": CYCLE_ID,
    "state": "enabled",
    "cronExprUTC": "0 0 * * *",
    "arguments": {"model_name": "tomato-v3"},
    "createdAt": "2026-04-01T00:00:00Z",
    "updatedAt": "2026-04-01T00:00:00Z",
}

CYCLE_RESPONSE = {
    "id": CYCLE_ID,
    "description": "Spring 2026",
    "organizationId": ORG_ID,
    "greenhouseId": GREENHOUSE_ID,
    "plantingDate": "2026-03-01T00:00:00Z",
}

PHOTO_JSON = {
    "id": "00000000-0000-0000-0000-000000000001",
    "userId": "test",
    "greenhouseId": GREENHOUSE_ID,
    "cultureId": "tomato",
    "growingCycleId": CYCLE_ID,
    "capturedAt": "2026-04-01T10:00:00Z",
    "source": "human",
    "pos": {"x": 0, "y": 0, "h": 0},
    "ptz": [0, 0, 0],
    "createdAt": "2026-04-01T10:00:00Z",
}


def _upload_link_handler(request: httpx.Request) -> httpx.Response:
    photo_id = str(request.url).split("/photos/")[1].split("/upload-link")[0]
    return httpx.Response(200, json={
        "photoId": photo_id,
        "uploadUrl": "http://minio:9000/bucket/photo?presigned=true",
        "downloadUrl": "http://minio:9000/bucket/photo?download=true",
        "deleteUrl": "http://minio:9000/bucket/photo?delete=true",
        "expiresAt": "2026-04-01T12:00:00Z",
    })


def _mock_pipeline_init(mock_hera: respx.Router) -> None:
    """Register mocks for the pipeline init sequence."""
    mock_hera.get(f"/api/v1/pipelines/schedules/{SCHEDULE_ID}").respond(200, json=SCHEDULE_RESPONSE)
    mock_hera.get(f"/api/v1/cycles/{CYCLE_ID}").respond(200, json=CYCLE_RESPONSE)
    mock_hera.post(url__regex=r"/api/v1/pipelines/fires/.+").respond(201)


# --- Pipeline init ---


async def test_pipeline_init_resolves_context(mock_hera: respx.Router) -> None:
    """Pipeline mode resolves greenhouse, cycle, model from schedule."""
    _mock_pipeline_init(mock_hera)

    async with Fermata(
        HERA_URL, USERNAME, PASSWORD,
        pipeline_id=SCHEDULE_ID, sync_id="run-001",
    ) as f:
        assert f.run is not None
        assert f.run.greenhouse_id == GREENHOUSE_ID
        assert f.run.growing_cycle_id == CYCLE_ID
        assert f.run.model_name == "tomato-v3"
        assert f.run.organization_id == ORG_ID
        assert f.run.run_id  # fire_id was generated
        assert f.scan_id == f.run.run_id  # scan_id set to fire_id


async def test_pipeline_init_sets_cycle_and_greenhouse(mock_hera: respx.Router) -> None:
    """Pipeline mode derives greenhouse_id from the growing cycle."""
    _mock_pipeline_init(mock_hera)

    async with Fermata(
        HERA_URL, USERNAME, PASSWORD,
        pipeline_id=SCHEDULE_ID, sync_id="run-001",
    ) as f:
        assert f.run is not None
        assert f.run.growing_cycle_id == CYCLE_ID
        assert f.run.greenhouse_id == GREENHOUSE_ID


async def test_pipeline_init_model_fallback(mock_hera: respx.Router) -> None:
    """If schedule has no model_name, fall back to models.list()."""
    schedule_no_model = {**SCHEDULE_RESPONSE, "arguments": {}}
    mock_hera.get(f"/api/v1/pipelines/schedules/{SCHEDULE_ID}").respond(200, json=schedule_no_model)
    mock_hera.get(f"/api/v1/cycles/{CYCLE_ID}").respond(200, json=CYCLE_RESPONSE)
    mock_hera.post(url__regex=r"/api/v1/pipelines/fires/.+").respond(201)
    mock_hera.get("/api/v1/models").respond(200, json=[
        {"modelName": "fallback-model", "modelType": "detection", "isActive": True}
    ])

    async with Fermata(
        HERA_URL, USERNAME, PASSWORD,
        pipeline_id=SCHEDULE_ID, sync_id="run-001",
    ) as f:
        assert f.run is not None
        assert f.run.model_name == "fallback-model"


# --- Validation ---


def test_pipeline_id_without_sync_id_raises() -> None:
    """pipeline_id without sync_id is a ValueError."""
    with pytest.raises(ValueError, match="sync_id is required"):
        Fermata(HERA_URL, USERNAME, PASSWORD, pipeline_id=SCHEDULE_ID)


async def test_no_pipeline_mode_by_default(mock_hera: respx.Router) -> None:
    """Without pipeline args, run is None."""
    async with Fermata(HERA_URL, USERNAME, PASSWORD) as f:
        assert f.run is None


# --- Infer with pipeline ---


async def test_infer_pipeline_auto_fills(mock_hera: respx.Router) -> None:
    """infer() uses greenhouse_id and model_name from run context."""
    _mock_pipeline_init(mock_hera)
    mock_hera.post(url__regex=r"/api/v1/photos/.+/upload-link").mock(side_effect=_upload_link_handler)
    mock_hera.post(url__regex=r"/api/v1/photos/[0-9a-f-]+$").respond(200, json=PHOTO_JSON)
    mock_hera.post("/api/v1/inference").respond(200, json={
        "taskId": "00000000-0000-0000-0000-000000000099",
    })

    with respx.mock() as minio_router:
        minio_router.put(url__regex=MINIO_URL_PATTERN).respond(200)

        async with Fermata(
            HERA_URL, USERNAME, PASSWORD,
            pipeline_id=SCHEDULE_ID, sync_id="run-001",
        ) as f:
            task_id = await f.infer(
                image=b"fake-jpeg-bytes",
                captured_at="2026-04-01T10:00:00Z",
            )

    assert task_id == "00000000-0000-0000-0000-000000000099"


async def test_infer_pipeline_explicit_override(mock_hera: respx.Router) -> None:
    """Explicit greenhouse_id and model_name override run context."""
    _mock_pipeline_init(mock_hera)
    mock_hera.post(url__regex=r"/api/v1/photos/.+/upload-link").mock(side_effect=_upload_link_handler)
    mock_hera.post(url__regex=r"/api/v1/photos/[0-9a-f-]+$").respond(200, json=PHOTO_JSON)
    mock_hera.post("/api/v1/inference").respond(200, json={
        "taskId": "00000000-0000-0000-0000-000000000099",
    })

    captured_inference: list[httpx.Request] = []
    original = mock_hera.routes[-1]  # the inference route

    with respx.mock() as minio_router:
        minio_router.put(url__regex=MINIO_URL_PATTERN).respond(200)

        async with Fermata(
            HERA_URL, USERNAME, PASSWORD,
            pipeline_id=SCHEDULE_ID, sync_id="run-001",
        ) as f:
            task_id = await f.infer(
                image=b"fake-jpeg-bytes",
                captured_at="2026-04-01T10:00:00Z",
                greenhouse_id="override-gh",
                model_name="override-model",
            )

    assert task_id == "00000000-0000-0000-0000-000000000099"


# --- Deterministic photo ID ---


def test_deterministic_photo_id_same_inputs() -> None:
    """Same inputs always produce the same photo_id."""
    id1 = _deterministic_photo_id("run-001", "2026-04-01T10:00:00Z", {"x": 1.0, "y": 2.0, "h": 0.5})
    id2 = _deterministic_photo_id("run-001", "2026-04-01T10:00:00Z", {"x": 1.0, "y": 2.0, "h": 0.5})
    assert id1 == id2


def test_deterministic_photo_id_different_inputs() -> None:
    """Different inputs produce different photo_ids."""
    id1 = _deterministic_photo_id("run-001", "2026-04-01T10:00:00Z", {"x": 1.0, "y": 2.0, "h": 0.5})
    id2 = _deterministic_photo_id("run-001", "2026-04-01T10:00:00Z", {"x": 1.0, "y": 3.0, "h": 0.5})
    assert id1 != id2


def test_deterministic_photo_id_no_position() -> None:
    """Without position, only sync_id and captured_at matter."""
    id1 = _deterministic_photo_id("run-001", "2026-04-01T10:00:00Z", None)
    id2 = _deterministic_photo_id("run-001", "2026-04-01T10:00:00Z", None)
    assert id1 == id2


def test_deterministic_photo_id_different_sync_id() -> None:
    """Different sync_id produces different photo_id."""
    id1 = _deterministic_photo_id("run-001", "2026-04-01T10:00:00Z", None)
    id2 = _deterministic_photo_id("run-002", "2026-04-01T10:00:00Z", None)
    assert id1 != id2


# --- Retry idempotency ---


async def test_infer_retry_handles_409(mock_hera: respx.Router) -> None:
    """On retry, 409 on photo create is caught and inference still proceeds."""
    _mock_pipeline_init(mock_hera)
    mock_hera.post(url__regex=r"/api/v1/photos/.+/upload-link").mock(side_effect=_upload_link_handler)
    mock_hera.post(url__regex=r"/api/v1/photos/[0-9a-f-]+$").respond(409, json={"message": "already exists"})
    mock_hera.post("/api/v1/inference").respond(200, json={
        "taskId": "00000000-0000-0000-0000-000000000099",
    })

    with respx.mock() as minio_router:
        minio_router.put(url__regex=MINIO_URL_PATTERN).respond(200)

        async with Fermata(
            HERA_URL, USERNAME, PASSWORD,
            pipeline_id=SCHEDULE_ID, sync_id="run-001",
        ) as f:
            task_id = await f.infer(
                image=b"fake-jpeg-bytes",
                captured_at="2026-04-01T10:00:00Z",
            )

    assert task_id == "00000000-0000-0000-0000-000000000099"


# --- Sync client pipeline ---


def test_sync_pipeline_init(mock_hera: respx.Router) -> None:
    """Sync client supports pipeline mode."""
    _mock_pipeline_init(mock_hera)

    with FermataSync(
        HERA_URL, USERNAME, PASSWORD,
        pipeline_id=SCHEDULE_ID, sync_id="run-001",
    ) as f:
        assert f.run is not None
        assert f.run.greenhouse_id == GREENHOUSE_ID
        assert f.run.model_name == "tomato-v3"


@pytest.fixture
def mock_hera():
    """respx mock router for Hera API."""
    with respx.mock(base_url=HERA_URL, assert_all_called=False) as router:
        router.post("/auth/token").respond(json=TOKEN_RESPONSE)
        yield router
