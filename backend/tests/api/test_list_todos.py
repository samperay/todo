from tests.api_helpers import auth, create_person


async def test_list_returns_only_the_callers_todos(client) -> None:
    _, owner_token = await create_person(client)
    _, other_token = await create_person(client)
    created = await client.post(
        "/api/v1/todos", headers=auth(owner_token), json={"title": "Mine"}
    )
    await client.post(
        "/api/v1/todos", headers=auth(other_token), json={"title": "Theirs"}
    )

    listed = await client.get("/api/v1/todos", headers=auth(owner_token))
    empty = await client.get("/api/v1/todos", headers=auth(await _fresh_token(client)))

    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [created.json()["id"]]
    assert listed.json()[0]["priority"] == "medium"
    assert empty.status_code == 200
    assert empty.json() == []


async def test_list_requires_a_token(client) -> None:
    response = await client.get("/api/v1/todos")
    assert response.status_code == 401


async def _fresh_token(client) -> str:
    _, token = await create_person(client)
    return token
