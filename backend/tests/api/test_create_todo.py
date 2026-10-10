from tests.api_helpers import auth, create_person


async def test_create_todo_with_description(client) -> None:
    _, token = await create_person(client)
    response = await client.post(
        "/api/v1/todos",
        headers=auth(token),
        json={"title": "Buy milk", "description": "1 liter"},
    )
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {
        "id",
        "title",
        "description",
        "completed",
        "priority",
        "created_at",
        "updated_at",
    }
    assert body["priority"] == "medium"
    assert "owner_id" not in body
    assert body["title"] == "Buy milk"
    assert body["description"] == "1 liter"
    assert body["completed"] is False
    assert body["created_at"] == body["updated_at"]


async def test_create_todo_without_description(client) -> None:
    _, token = await create_person(client)
    response = await client.post(
        "/api/v1/todos",
        headers=auth(token),
        json={"title": "Walk"},
    )
    assert response.status_code == 201
    assert response.json()["description"] is None


async def test_invalid_title_or_description_is_rejected(client) -> None:
    _, token = await create_person(client)
    headers = auth(token)
    rejected = [
        {},
        {"title": "   "},
        {"title": "a" * 201},
        {"title": "Ok", "description": "d" * 2001},
    ]
    for payload in rejected:
        response = await client.post("/api/v1/todos", headers=headers, json=payload)
        assert response.status_code == 422, payload

    listed = await client.get("/api/v1/todos", headers=headers)
    assert listed.json() == []


async def test_priority_can_be_set_and_invalid_values_are_rejected(client) -> None:
    _, token = await create_person(client)
    headers = auth(token)
    created = await client.post(
        "/api/v1/todos",
        headers=headers,
        json={"title": "Walk", "priority": "high"},
    )
    assert created.status_code == 201
    assert created.json()["priority"] == "high"

    rejected = await client.post(
        "/api/v1/todos",
        headers=headers,
        json={"title": "Walk", "priority": "urgent"},
    )
    assert rejected.status_code == 422
    listed = await client.get("/api/v1/todos", headers=headers)
    assert [item["title"] for item in listed.json()] == ["Walk"]


async def test_create_without_token_stores_nothing(client) -> None:
    response = await client.post("/api/v1/todos", json={"title": "Buy milk"})
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "You must be identified."
