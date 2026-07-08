from __future__ import annotations

import httpx
import pytest
import respx

from fermata.exceptions import NotFoundError
from fermata.types import GreenhouseObject, GreenhouseObjectType

GREENHOUSE_ID = "00000000-0000-0000-0000-000000000010"

ROW_OBJECT = {
    "id": 1,
    "greenhouseId": GREENHOUSE_ID,
    "kind": "row",
    "description": "Row 1",
    "pos": {"x": 1.0, "y": 2.0},
    "height": 3.5,
    "createdAt": "2026-04-01T00:00:00Z",
    "updatedAt": "2026-04-01T00:00:00Z",
}

BLOCK_OBJECT = {
    "id": 2,
    "greenhouseId": GREENHOUSE_ID,
    "kind": "block",
    "description": "Block A",
    "rect": {"x1": 0.0, "y1": 0.0, "x2": 10.0, "y2": 5.0},
    "createdAt": "2026-04-01T00:00:00Z",
    "updatedAt": "2026-04-01T00:00:00Z",
}

NOT_FOUND_JSON = {
    "code": "NotFound",
    "request_id": "req-1",
    "message": "greenhouse object not found",
}


# --- list ---


async def test_list_follows_cursor_pagination(client, mock_hera: respx.Router) -> None:
    """list() transparently follows next_token across pages."""

    def _pages(request: httpx.Request) -> httpx.Response:
        if request.url.params.get("cursor") == "page-2":
            return httpx.Response(200, json={"items": [BLOCK_OBJECT]})
        return httpx.Response(200, json={"items": [ROW_OBJECT], "next_token": "page-2"})

    route = mock_hera.get(f"/api/v1/greenhouses/{GREENHOUSE_ID}/objects").mock(side_effect=_pages)

    objects = await client.greenhouse_objects.list(GREENHOUSE_ID)

    assert route.call_count == 2
    assert route.calls[1].request.url.params["cursor"] == "page-2"
    assert [o.id for o in objects] == [1, 2]
    assert all(isinstance(o, GreenhouseObject) for o in objects)
    assert objects[0].kind is GreenhouseObjectType.ROW
    assert objects[1].kind is GreenhouseObjectType.BLOCK


async def test_list_single_page(client, mock_hera: respx.Router) -> None:
    """A response without next_token ends pagination after one call."""
    route = mock_hera.get(f"/api/v1/greenhouses/{GREENHOUSE_ID}/objects").respond(
        200, json={"items": [ROW_OBJECT]}
    )

    objects = await client.greenhouse_objects.list(GREENHOUSE_ID)

    assert route.call_count == 1
    assert len(objects) == 1
    assert objects[0].description == "Row 1"
    assert objects[0].pos.x == 1.0
    assert objects[0].height == 3.5


# --- get ---


async def test_get_returns_typed_model(client, mock_hera: respx.Router) -> None:
    mock_hera.get(f"/api/v1/greenhouses/{GREENHOUSE_ID}/objects/2").respond(
        200, json=BLOCK_OBJECT
    )

    obj = await client.greenhouse_objects.get(GREENHOUSE_ID, 2)

    assert isinstance(obj, GreenhouseObject)
    assert obj.id == 2
    assert obj.kind is GreenhouseObjectType.BLOCK
    assert obj.rect.x2 == 10.0


async def test_get_missing_raises_not_found(client, mock_hera: respx.Router) -> None:
    mock_hera.get(f"/api/v1/greenhouses/{GREENHOUSE_ID}/objects/999").respond(
        404, json=NOT_FOUND_JSON
    )

    with pytest.raises(NotFoundError):
        await client.greenhouse_objects.get(GREENHOUSE_ID, 999)


# --- sync client ---


def test_sync_list_and_get(sync_client, mock_hera: respx.Router) -> None:
    mock_hera.get(f"/api/v1/greenhouses/{GREENHOUSE_ID}/objects").respond(
        200, json={"items": [ROW_OBJECT]}
    )
    mock_hera.get(f"/api/v1/greenhouses/{GREENHOUSE_ID}/objects/1").respond(
        200, json=ROW_OBJECT
    )

    objects = sync_client.greenhouse_objects.list(GREENHOUSE_ID)
    obj = sync_client.greenhouse_objects.get(GREENHOUSE_ID, 1)

    assert [o.id for o in objects] == [1]
    assert obj.kind is GreenhouseObjectType.ROW
