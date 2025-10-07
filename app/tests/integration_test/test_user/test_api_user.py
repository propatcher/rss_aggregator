import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "status_code",
    [
        (200),
    ],
)
async def test_add_and_get_link(auth_ac: AsyncClient,status_code):
    response = await auth_ac.post("/auth/me")

    assert response.status_code == status_code

 