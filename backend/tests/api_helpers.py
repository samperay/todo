from httpx import AsyncClient


async def create_person(client: AsyncClient) -> tuple[str, str]:
    response = await client.post("/api/v1/users")
    assert response.status_code == 201
    body = response.json()
    return body["id"], body["token"]


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
