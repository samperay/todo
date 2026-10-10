from uuid import uuid4

from tests.api_helpers import auth, create_person


async def test_mark_incomplete_restores_an_open_todo(client) -> None:
    _, token = await create_person(client)
    created = await client.post(
        "/api/v1/todos",
        headers=auth(token),
        json={"title": "Buy milk", "description": "1 liter", "priority": "high"},
    )
    todo_id = created.json()["id"]
    await client.post(f"/api/v1/todos/{todo_id}/complete", headers=auth(token))

    opened = await client.post(f"/api/v1/todos/{todo_id}/incomplete", headers=auth(token))
    again = await client.post(f"/api/v1/todos/{todo_id}/incomplete", headers=auth(token))

    assert opened.status_code == 200
    assert opened.json()["completed"] is False
    assert opened.json()["title"] == "Buy milk"
    assert opened.json()["description"] == "1 liter"
    assert opened.json()["priority"] == "high"
    assert opened.json()["created_at"] == created.json()["created_at"]
    assert again.json()["updated_at"] == opened.json()["updated_at"]


async def test_incomplete_unknown_or_other_owner_is_not_found(client) -> None:
    _, owner_token = await create_person(client)
    _, other_token = await create_person(client)
    created = await client.post(
        "/api/v1/todos", headers=auth(owner_token), json={"title": "Buy milk"}
    )
    todo_id = created.json()["id"]
    other = await client.post(f"/api/v1/todos/{todo_id}/incomplete", headers=auth(other_token))
    missing = await client.post(f"/api/v1/todos/{uuid4()}/incomplete", headers=auth(owner_token))
    anonymous = await client.post(f"/api/v1/todos/{todo_id}/incomplete")
    assert other.status_code == 404
    assert missing.status_code == 404
    assert anonymous.status_code == 401
