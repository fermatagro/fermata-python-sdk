"""Integration tests against real Hera in docker-compose.

Run with: .venv/bin/pytest tests/integration/ -v

Requires the on-site docker-compose stack to be running:
  docker compose -f fermata-onsite/deploy/docker-compose.yml up -d
"""
from __future__ import annotations

import os

from uuid_utils import uuid7

import pytest

from fermata import Fermata, FermataSync
from fermata.exceptions import NotFoundError

HERA_URL = os.environ.get("HERA_URL", "http://172.28.0.10:3000")
APP_ID = os.environ.get("HERA_APP_ID", "viscon-onsite-01")
APP_SECRET = os.environ.get("HERA_APP_SECRET", "change-me-in-production")


@pytest.fixture
async def client():
    async with Fermata(HERA_URL, APP_ID, APP_SECRET) as f:
        yield f


@pytest.fixture
def sync_client():
    with FermataSync(HERA_URL, APP_ID, APP_SECRET) as f:
        yield f


# --- Auth ---


async def test_auth_token_exchange(client):
    """Client should authenticate automatically on first request."""
    # Use greenhouses (not models) since models proxies to Argus which isn't running
    items = []
    async for gh in client.greenhouses.list():
        items.append(gh)
    assert isinstance(items, list)


# --- Greenhouses ---


async def test_greenhouse_crud(client):
    gh_id = str(uuid7())
    gh = await client.greenhouses.create(gh_id, name="SDK Test GH", width=100.0, height=50.0, timezone="UTC")
    assert gh.description == "SDK Test GH"

    fetched = await client.greenhouses.get(gh_id)
    assert fetched.description == "SDK Test GH"

    await client.greenhouses.rename(gh_id, "Renamed GH")
    fetched = await client.greenhouses.get(gh_id)
    assert fetched.description == "Renamed GH"

    await client.greenhouses.delete(gh_id)
    with pytest.raises(NotFoundError):
        await client.greenhouses.get(gh_id)


async def test_list_greenhouses(client):
    items = []
    async for gh in client.greenhouses.list():
        items.append(gh)
    assert isinstance(items, list)


# --- Cultivation ---


async def test_culture_crud(client):
    culture_id = f"sdk-test-{uuid7().hex[:8]}"
    culture = await client.cultures.create(culture_id, description="Test culture")
    assert culture.id == culture_id

    fetched = await client.cultures.get(culture_id)
    assert fetched.id == culture_id

    await client.cultures.delete(culture_id)


async def test_cycle_crud(client):
    gh_id = str(uuid7())
    await client.greenhouses.create(gh_id, name="Cycle Test GH", width=50.0, height=25.0)

    cycle_id = str(uuid7())
    cycle = await client.cycles.create(
        cycle_id,
        greenhouse_id=gh_id,
        planting_date="2026-03-01T00:00:00Z",
        description="Spring 2026",
    )
    assert str(cycle.greenhouse_id) == gh_id

    fetched = await client.cycles.get(cycle_id)
    assert fetched.description == "Spring 2026"

    await client.cycles.close(cycle_id, "2026-06-01T00:00:00Z")
    await client.cycles.delete(cycle_id)
    await client.greenhouses.delete(gh_id)


# --- Catalog ---


async def test_list_models(client):
    """Models endpoint proxies to Argus — may return 503 if Argus is not running."""
    try:
        models = await client.models.list()
        assert isinstance(models, list)
    except Exception:
        pytest.skip("Argus not running — models endpoint unavailable")


async def test_list_classes(client):
    """Classes endpoint proxies to Argus — may return 503 if Argus is not running."""
    try:
        classes = await client.classes.list()
        assert isinstance(classes, list)
    except Exception:
        pytest.skip("Argus not running — classes endpoint unavailable")


# --- Predictions ---


async def test_list_predictions(client):
    """Predictions require a cycle_id. Create a cycle first, then query."""
    gh_id = str(uuid7())
    cycle_id = str(uuid7())
    await client.greenhouses.create(gh_id, name="Pred Test GH", width=50.0, height=25.0)
    await client.cycles.create(cycle_id, greenhouse_id=gh_id, planting_date="2026-03-01T00:00:00Z", description="Test")

    items = []
    async for pred in client.predictions.list(cycle_id=cycle_id, from_="2026-01-01T00:00:00Z", to="2026-12-31T23:59:59Z"):
        items.append(pred)
        if len(items) >= 5:
            break
    assert isinstance(items, list)

    await client.cycles.delete(cycle_id)
    await client.greenhouses.delete(gh_id)


# --- Sync client ---


def test_sync_list_greenhouses(sync_client):
    items = list(sync_client.greenhouses.list())
    assert isinstance(items, list)


def test_sync_greenhouse_crud(sync_client):
    gh_id = str(uuid7())
    gh = sync_client.greenhouses.create(gh_id, name="Sync SDK Test", width=80.0, height=40.0)
    assert gh.description == "Sync SDK Test"

    sync_client.greenhouses.delete(gh_id)
    with pytest.raises(NotFoundError):
        sync_client.greenhouses.get(gh_id)
