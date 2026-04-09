from __future__ import annotations

import pytest
import respx

from fermata import Fermata, FermataSync

HERA_URL = "http://hera-test:3000"
USERNAME = "test-user"
PASSWORD = "test-password"

TOKEN_RESPONSE = {
    "access_token": "mock-jwt-token",
    "token_type": "Bearer",
    "expires_in": 3600,
}


@pytest.fixture
def mock_hera():
    """respx mock router for Hera API."""
    with respx.mock(base_url=HERA_URL, assert_all_called=False) as router:
        router.post("/auth/token").respond(json=TOKEN_RESPONSE)
        yield router


@pytest.fixture
async def client(mock_hera):
    """Async Fermata client with mocked Hera."""
    async with Fermata(HERA_URL, USERNAME, PASSWORD) as f:
        yield f


@pytest.fixture
def sync_client(mock_hera):
    """Sync Fermata client with mocked Hera."""
    with FermataSync(HERA_URL, USERNAME, PASSWORD) as f:
        yield f
