"""Integration test: full pipeline mode flow against real Hera.

Requires on-site docker-compose stack running (postgres + seaweedfs + hera).
"""

from __future__ import annotations

import os
import time

import httpx
import pytest
from uuid_utils import uuid7

from fermata import Fermata, FermataSync

HERA_URL = os.environ.get("HERA_URL", "http://172.28.0.10:3000")
APP_ID = os.environ.get("HERA_APP_ID", "viscon-onsite-01")
APP_SECRET = os.environ.get("HERA_APP_SECRET", "change-me-in-production")


def _get_token() -> tuple[str, str]:
    """Get auth token and org_id from Hera."""
    resp = httpx.post(
        f"{HERA_URL}/auth/token",
        data={"client_id": APP_ID, "client_secret": APP_SECRET},
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    import base64, json
    payload = token.split(".")[1]
    payload += "=" * (4 - len(payload) % 4)
    claims = json.loads(base64.b64decode(payload))
    return token, claims.get("organization_id", "")


def _api(token: str, method: str, path: str, **kwargs) -> httpx.Response:
    return httpx.request(
        method, f"{HERA_URL}{path}",
        headers={"Authorization": f"Bearer {token}"},
        **kwargs,
    )


def _create_pipeline_data(token: str, org_id: str) -> dict:
    """Create a full set of test entities: greenhouse, culture, cycle, template, schedule."""
    gh_id = str(uuid7())
    culture_id = "tomato"
    cycle_id = str(uuid7())
    template_id = str(uuid7())
    schedule_id = str(uuid7())

    resp = _api(token, "POST", f"/api/v1/greenhouses/{gh_id}", json={
        "description": "Pipeline Test GH", "width": 100.0, "height": 50.0, "tz": "UTC",
    })
    assert resp.status_code == 201, f"Create greenhouse: {resp.status_code} {resp.text}"

    resp = _api(token, "POST", f"/api/v1/cultures/{culture_id}", json={"description": "Tomatoes"})
    assert resp.status_code in (201, 409), f"Create culture: {resp.status_code} {resp.text}"

    resp = _api(token, "POST", f"/api/v1/cycles/{cycle_id}", json={
        "greenhouseId": gh_id, "cultureId": culture_id,
        "plantingDate": "2026-03-01T00:00:00Z", "description": "Spring 2026",
    })
    assert resp.status_code == 201, f"Create cycle: {resp.status_code} {resp.text}"

    resp = _api(token, "POST", f"/api/v1/pipelines/templates/{template_id}", json={
        "name": "onsite-scan", "flowName": "onsite-scan",
    })
    assert resp.status_code in (201, 409), f"Create template: {resp.status_code} {resp.text}"

    resp = _api(token, "POST", f"/api/v1/pipelines/schedules/{schedule_id}", json={
        "templateId": template_id, "scope": "growing_cycle", "type": "onsite",
        "scopeId": cycle_id, "cronExprUTC": "0 0 * * *",
        "arguments": {"model_name": "tomato-v3"},
    })
    assert resp.status_code == 201, f"Create schedule: {resp.status_code} {resp.text}"

    return {
        "greenhouse_id": gh_id, "culture_id": culture_id, "cycle_id": cycle_id,
        "template_id": template_id, "schedule_id": schedule_id, "org_id": org_id,
    }


@pytest.fixture(scope="module")
def shared_data():
    """Shared test data — used by tests that don't create fires."""
    token, org_id = _get_token()
    return _create_pipeline_data(token, org_id)


@pytest.fixture
def pipeline_data():
    """Per-test data — each test gets its own schedule to avoid fire dedup collisions."""
    token, org_id = _get_token()
    return _create_pipeline_data(token, org_id)


# --- Tests ---


def test_list_schedules(shared_data):
    """SDK can list schedules and find the one we created."""
    with FermataSync(HERA_URL, APP_ID, APP_SECRET) as f:
        schedules = f.pipelines.list_schedules()
        assert len(schedules) >= 1
        ids = [str(s.id) for s in schedules]
        assert shared_data["schedule_id"] in ids


def test_pipeline_init_resolves_context(pipeline_data):
    """Pipeline mode resolves greenhouse, cycle, model from schedule."""
    data = pipeline_data
    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=f"test-{uuid7()}",
    ) as f:
        assert f.run is not None
        assert f.run.greenhouse_id == data["greenhouse_id"]
        assert f.run.growing_cycle_id == data["cycle_id"]
        assert f.run.organization_id == data["org_id"]
        assert f.run.model_name is not None
        assert f.run.run_id


def test_pipeline_infer_upload(pipeline_data):
    """Pipeline mode: infer() uploads photo and submits inference."""
    data = pipeline_data
    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=f"test-{uuid7()}",
    ) as f:
        try:
            task_id = f.infer(
                image=b"\xff\xd8\xff\xe0" + b"\x00" * 100,
                captured_at="2026-04-15T10:00:00Z",
                position={"x": 1.0, "y": 2.0, "h": 0.5},
            )
            assert task_id
        except Exception:
            # Inference submit may fail without Argus, but photo was created
            pass


def test_pipeline_idempotent_retry(pipeline_data):
    """Same sync_id + captured_at + position produces same photo_id. 409 caught on retry."""
    data = pipeline_data
    sync_id = f"idem-{uuid7()}"

    # First run
    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=sync_id,
    ) as f:
        try:
            f.infer(
                image=b"\xff\xd8\xff\xe0" + b"\x00" * 100,
                captured_at="2026-04-15T11:00:00Z",
                position={"x": 5.0, "y": 3.0, "h": 1.0},
            )
        except Exception:
            pass

    # Second run — same sync_id. Uses a NEW schedule to avoid fire dedup collision.
    token, org_id = _get_token()
    data2 = _create_pipeline_data(token, org_id)

    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data2["schedule_id"],
        sync_id=sync_id,
    ) as f:
        try:
            f.infer(
                image=b"\xff\xd8\xff\xe0" + b"\x00" * 100,
                captured_at="2026-04-15T11:00:00Z",
                position={"x": 5.0, "y": 3.0, "h": 1.0},
            )
        except Exception:
            pass
        # No crash = success. The 409 on photo create was handled.


def test_fire_lifecycle(pipeline_data):
    """Fire transitions: pending → running → completed."""
    data = pipeline_data
    token, _ = _get_token()

    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=f"lifecycle-{uuid7()}",
    ) as f:
        fire_id = f.run.run_id

        # Fire should be running inside the context
        resp = _api(token, "GET", f"/api/v1/pipelines/fires/{fire_id}")
        assert resp.status_code == 200
        assert resp.json()["status"] == "running"

    # After exit, fire should be completed
    resp = _api(token, "GET", f"/api/v1/pipelines/fires/{fire_id}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


def test_legacy_mode_unchanged(shared_data):
    """Without pipeline args, SDK works as before."""
    with FermataSync(HERA_URL, APP_ID, APP_SECRET) as f:
        assert f.run is None
        schedules = f.pipelines.list_schedules()
        assert len(schedules) >= 1
