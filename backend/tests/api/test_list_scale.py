from uuid import UUID

from tests.api_helpers import auth, create_person


async def test_list_of_100_is_complete_and_newest_first(client) -> None:
    _, owner_token = await create_person(client)
    _, other_token = await create_person(client)
    await client.post("/api/v1/todos", headers=auth(other_token), json={"title": "Not mine"})
    for index in range(100):
        response = await client.post(
            "/api/v1/todos",
            headers=auth(owner_token),
            json={"title": f"Todo {index}"},
        )
        assert response.status_code == 201

    listed = await client.get("/api/v1/todos", headers=auth(owner_token))
    body = listed.json()
    assert listed.status_code == 200
    assert len(body) == 100
    assert len({item["id"] for item in body}) == 100
    assert all(item["title"] != "Not mine" for item in body)
    for earlier, later in zip(body, body[1:], strict=False):
        if earlier["created_at"] == later["created_at"]:
            assert UUID(earlier["id"]).int >= UUID(later["id"]).int
        else:
            assert earlier["created_at"] > later["created_at"]
