from uuid import uuid4

from tests.api_helpers import auth, create_person


async def test_patch_changes_only_supplied_fields(client) -> None:
    _, token = await create_person(client)
    created = await client.post(
        "/api/v1/todos",
        headers=auth(token),
        json={"title": "Buy milk", "description": "1 liter"},
    )
    todo_id = created.json()["id"]

    renamed = await client.patch(
        f"/api/v1/todos/{todo_id}",
        headers=auth(token),
        json={"title": "Buy oat milk"},
    )
    cleared = await client.patch(
        f"/api/v1/todos/{todo_id}",
        headers=auth(token),
        json={"description": None},
    )

    assert renamed.status_code == 200
    assert renamed.json()["description"] == "1 liter"
    assert renamed.json()["completed"] is False
    assert renamed.json()["created_at"] == created.json()["created_at"]
    assert cleared.json()["title"] == "Buy oat milk"
    assert cleared.json()["description"] is None


async def test_patch_priority_and_rejects_invalid_values(client) -> None:
    _, token = await create_person(client)
    created = await client.post(
        "/api/v1/todos",
        headers=auth(token),
        json={"title": "Buy milk", "description": "1 liter", "priority": "high"},
    )
    todo_id = created.json()["id"]
    lowered = await client.patch(
        f"/api/v1/todos/{todo_id}",
        headers=auth(token),
        json={"priority": "low"},
    )
    assert lowered.status_code == 200
    body = lowered.json()
    assert body["priority"] == "low"
    assert body["title"] == "Buy milk"
    assert body["description"] == "1 liter"

    for payload in ({"priority": "urgent"}, {"priority": None}):
        rejected = await client.patch(f"/api/v1/todos/{todo_id}", headers=auth(token), json=payload)
        assert rejected.status_code == 422, payload
    stored = await client.get(f"/api/v1/todos/{todo_id}", headers=auth(token))
    assert stored.json()["priority"] == "low"
    assert stored.json()["title"] == "Buy milk"


async def test_patch_rejects_invalid_text(client) -> None:
    _, token = await create_person(client)
    created = await client.post("/api/v1/todos", headers=auth(token), json={"title": "Buy milk"})
    todo_id = created.json()["id"]
    for payload in ({"title": "   "}, {"title": "a" * 201}, {"description": "d" * 2001}, {}):
        response = await client.patch(f"/api/v1/todos/{todo_id}", headers=auth(token), json=payload)
        assert response.status_code == 422, payload
    stored = await client.get(f"/api/v1/todos/{todo_id}", headers=auth(token))
    assert stored.json()["title"] == "Buy milk"


async def test_later_overlapping_patch_wins_supplied_fields(client) -> None:
    _, token = await create_person(client)
    created = await client.post(
        "/api/v1/todos",
        headers=auth(token),
        json={"title": "Buy milk", "description": "1 liter"},
    )
    todo_id = created.json()["id"]
    await client.patch(
        f"/api/v1/todos/{todo_id}",
        headers=auth(token),
        json={"title": "Buy oat milk"},
    )
    later = await client.patch(
        f"/api/v1/todos/{todo_id}",
        headers=auth(token),
        json={"title": "Buy milk", "description": "2 liters"},
    )
    assert later.status_code == 200
    assert later.json()["title"] == "Buy milk"
    assert later.json()["description"] == "2 liters"


async def test_patch_not_found_and_unauthenticated(client) -> None:
    _, owner_token = await create_person(client)
    _, other_token = await create_person(client)
    created = await client.post(
        "/api/v1/todos", headers=auth(owner_token), json={"title": "Buy milk"}
    )
    todo_id = created.json()["id"]
    other = await client.patch(
        f"/api/v1/todos/{todo_id}",
        headers=auth(other_token),
        json={"title": "Stolen"},
    )
    missing = await client.patch(
        f"/api/v1/todos/{uuid4()}",
        headers=auth(owner_token),
        json={"title": "Missing"},
    )
    anonymous = await client.patch(f"/api/v1/todos/{todo_id}", json={"title": "No"})
    assert other.status_code == 404
    assert missing.status_code == 404
    assert anonymous.status_code == 401
    stored = await client.get(f"/api/v1/todos/{todo_id}", headers=auth(owner_token))
    assert stored.json()["title"] == "Buy milk"
