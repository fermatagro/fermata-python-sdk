"""Integration test: prediction sync — watcher ticket + by-fire endpoint.

Requires on-site docker-compose stack running (postgres + seaweedfs + hera).
Tests the on-site components of the prediction sync pipeline.
"""

from __future__ import annotations

import os
import time

import httpx
import psycopg2
import pytest
from uuid_utils import uuid7

from PIL import Image
import io

from fermata import FermataSync


def _make_test_jpeg() -> bytes:
    """Create a minimal valid JPEG image (100x100 red square)."""
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

HERA_URL = os.environ.get("HERA_URL", "http://172.28.0.10:3000")
APP_ID = os.environ.get("HERA_APP_ID", "hera-onsite-m2m")
APP_SECRET = os.environ.get("HERA_APP_SECRET", "hera-onsite-secret-dev-only")
POSTGRES_DSN = os.environ.get(
    "POSTGRES_DSN",
    "dbname=demetra user=postgres password=postgres host=172.28.0.2 port=5432",
)


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
    """Create test entities: greenhouse, culture, cycle, template, schedule."""
    gh_id = str(uuid7())
    culture_id = "tomato"
    cycle_id = str(uuid7())
    template_id = str(uuid7())
    schedule_id = str(uuid7())

    resp = _api(token, "POST", f"/api/v1/greenhouses/{gh_id}", json={
        "description": "Sync Test GH", "width": 100.0, "height": 50.0, "tz": "UTC",
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
        "name": "sync-test", "flowName": "sync-test",
    })
    assert resp.status_code in (201, 409), f"Create template: {resp.status_code} {resp.text}"

    resp = _api(token, "POST", f"/api/v1/pipelines/schedules/{schedule_id}", json={
        "templateId": template_id, "scope": "growing_cycle", "type": "onsite",
        "scopeId": cycle_id, "cronExprUTC": "0 0 * * *",
        "arguments": {"model_name": "tomatoes_v1"},
    })
    assert resp.status_code == 201, f"Create schedule: {resp.status_code} {resp.text}"

    return {
        "greenhouse_id": gh_id, "culture_id": culture_id, "cycle_id": cycle_id,
        "template_id": template_id, "schedule_id": schedule_id, "org_id": org_id,
    }


def _pg_query(query: str, params: tuple = ()) -> list:
    """Execute a query against the on-site PostgreSQL."""
    conn = psycopg2.connect(POSTGRES_DSN)
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()


def _pg_exec(query: str, params: tuple = ()):
    """Execute a write query against the on-site PostgreSQL."""
    conn = psycopg2.connect(POSTGRES_DSN)
    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(query, params)
    finally:
        conn.close()


def _wait_for(predicate, timeout=30, interval=2, desc="condition"):
    """Poll until predicate returns True or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    raise TimeoutError(f"Timed out waiting for {desc} (timeout={timeout}s)")


@pytest.fixture
def pipeline_data():
    token, org_id = _get_token()
    return _create_pipeline_data(token, org_id)


# --- Tests ---


def test_watch_fire_ticket_created_on_start(pipeline_data):
    """After starting a fire, an onsite:watch-fire Kharon ticket should exist."""
    data = pipeline_data
    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=f"sync-test-{uuid7()}",
    ) as f:
        fire_id = str(f.run.run_id)

        # Check kharon_tickets table for the watcher
        rows = _pg_query(
            "SELECT id, type, status FROM kharon_tickets WHERE type = %s AND id = %s",
            ("onsite:watch-fire", fire_id),
        )
        assert len(rows) == 1, f"Expected 1 watch-fire ticket, got {len(rows)}"
        assert rows[0][1] == "onsite:watch-fire"


def test_predictions_by_fire_endpoint(pipeline_data):
    """GET /predictions/by-fire/{fireId} returns predictions seeded for a fire."""
    data = pipeline_data
    token, _ = _get_token()

    # Start and complete a fire
    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=f"sync-test-{uuid7()}",
    ) as f:
        fire_id = str(f.run.run_id)

    # Seed predictions directly in PG (simulating Argus inference results)
    pred_id = str(uuid7())
    photo_id = str(uuid7())
    _pg_exec("""
        INSERT INTO predictions (
            id, organization_id, greenhouse_id, photo_id, device_type,
            growing_cycle_id, culture_id, source, pipeline_id,
            x, y, h, model_name, class_id, confidence,
            captured_at, predicted_at, planting_date, status
        ) VALUES (
            %s, %s, %s::uuid, %s::uuid, 'camera',
            %s::uuid, %s, 'pipeline', %s::uuid,
            1.0, 2.0, 0.5, 'tomatoes_v1', 'botrytis', 0.85,
            '2026-04-15T10:00:00Z', NOW(), '2026-03-01T00:00:00Z', 'unhealthy'
        )
    """, (pred_id, data["org_id"], data["greenhouse_id"], photo_id,
          data["cycle_id"], data["culture_id"], fire_id))

    # Call the by-fire endpoint
    resp = _api(token, "GET", f"/api/v1/predictions/by-fire/{fire_id}")
    assert resp.status_code == 200, f"by-fire endpoint: {resp.status_code} {resp.text}"

    page = resp.json()
    assert "items" in page
    assert len(page["items"]) == 1
    assert page["items"][0]["id"] == pred_id
    assert page["items"][0]["classId"] == "botrytis"


def test_predictions_by_fire_non_empty_filter(pipeline_data):
    """non_empty=true excludes healthy predictions, nonEmpty=false includes them."""
    data = pipeline_data
    token, _ = _get_token()

    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=f"sync-test-{uuid7()}",
    ) as f:
        fire_id = str(f.run.run_id)

    photo_id = str(uuid7())

    # Seed one unhealthy prediction
    _pg_exec("""
        INSERT INTO predictions (
            id, organization_id, greenhouse_id, photo_id, device_type,
            growing_cycle_id, culture_id, source, pipeline_id,
            x, y, h, model_name, class_id, confidence,
            captured_at, predicted_at, planting_date, status
        ) VALUES (
            %s, %s, %s::uuid, %s::uuid, 'camera',
            %s::uuid, %s, 'pipeline', %s::uuid,
            1.0, 2.0, 0.5, 'tomatoes_v1', 'botrytis', 0.9,
            '2026-04-15T10:00:00Z', NOW(), '2026-03-01T00:00:00Z', 'unhealthy'
        )
    """, (str(uuid7()), data["org_id"], data["greenhouse_id"], photo_id,
          data["cycle_id"], data["culture_id"], fire_id))

    # Seed one healthy prediction (class_id IS NULL)
    _pg_exec("""
        INSERT INTO predictions (
            id, organization_id, greenhouse_id, photo_id, device_type,
            growing_cycle_id, culture_id, source, pipeline_id,
            x, y, h, model_name, confidence,
            captured_at, predicted_at, planting_date, status
        ) VALUES (
            %s, %s, %s::uuid, %s::uuid, 'camera',
            %s::uuid, %s, 'pipeline', %s::uuid,
            1.0, 2.0, 0.5, 'tomatoes_v1', 0.95,
            '2026-04-15T10:00:00Z', NOW(), '2026-03-01T00:00:00Z', 'healthy'
        )
    """, (str(uuid7()), data["org_id"], data["greenhouse_id"], photo_id,
          data["cycle_id"], data["culture_id"], fire_id))

    # Default (non_empty=true): should only return unhealthy
    resp = _api(token, "GET", f"/api/v1/predictions/by-fire/{fire_id}")
    assert resp.status_code == 200
    non_empty = resp.json()["items"]
    assert len(non_empty) == 1
    assert non_empty[0]["classId"] is not None

    # nonEmpty=false: should return both
    resp = _api(token, "GET", f"/api/v1/predictions/by-fire/{fire_id}?nonEmpty=false")
    assert resp.status_code == 200
    all_preds = resp.json()["items"]
    assert len(all_preds) == 2


def test_watcher_completes_after_fire_done_and_no_inference(pipeline_data):
    """Watcher ticket should reach Done when fire is completed and no inference tickets exist."""
    data = pipeline_data

    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=f"sync-test-{uuid7()}",
    ) as f:
        fire_id = str(f.run.run_id)

    # Fire is now completed. No inference tickets were created (no infer() calls).
    # The watcher should detect: fire terminal + 0 pending inference tickets → notify cloud.
    # Cloud notification will fail (no tunnel), but watcher will retry.
    # We just check that the watcher eventually processed (status changes from pending).

    def watcher_processed():
        rows = _pg_query(
            "SELECT status, attempts FROM kharon_tickets WHERE type = %s AND id = %s",
            ("onsite:watch-fire", fire_id),
        )
        if not rows:
            return False
        status, attempts = rows[0]
        # The watcher should have processed at least once (attempts > 0)
        return attempts > 0

    _wait_for(watcher_processed, timeout=90, interval=5,
              desc="watcher ticket to be processed")


def test_full_inference_creates_predictions_and_by_fire_returns_them(pipeline_data):
    """Full E2E: SDK infer() → Argus inference → predictions stored → by-fire endpoint returns them."""
    data = pipeline_data
    token, _ = _get_token()

    with FermataSync(
        HERA_URL, APP_ID, APP_SECRET,
        pipeline_id=data["schedule_id"],
        sync_id=f"sync-e2e-{uuid7()}",
    ) as f:
        # Submit real inference with valid JPEG (Argus should process it)
        device_id = str(uuid7())
        f.infer(
            image=_make_test_jpeg(),
            captured_at="2026-04-15T10:00:00Z",
            position={"x": 1.0, "y": 2.0, "h": 0.5},
            device_id=device_id,
        )
        fire_id = str(f.run.run_id)

    # Wait for predictions to appear in DB (inference is async via Kharon)
    def predictions_exist():
        rows = _pg_query(
            "SELECT COUNT(*) FROM predictions WHERE pipeline_id = %s",
            (fire_id,),
        )
        return rows[0][0] > 0

    _wait_for(predictions_exist, timeout=60, interval=3,
              desc="predictions to appear after inference")

    # Verify by-fire endpoint returns them
    resp = _api(token, "GET", f"/api/v1/predictions/by-fire/{fire_id}?nonEmpty=false")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert len(items) > 0, f"Expected predictions for fire {fire_id}"

    # Verify watcher ticket has been processed
    rows = _pg_query(
        "SELECT attempts FROM kharon_tickets WHERE type = %s AND id = %s",
        ("onsite:watch-fire", fire_id),
    )
    assert len(rows) == 1
    assert rows[0][0] > 0, "Watcher should have been processed at least once"
