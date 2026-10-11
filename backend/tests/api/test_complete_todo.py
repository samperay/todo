from uuid import uuid4

from tests.api_helpers import auth, create_person


async def test_complete_keeps_the_todo_and_second_call_is_a_noop(client) -> None:
    _, token = await create_person(client)
    created = await client.post(
        "/api/v1/todos",
        headers=auth(token),
        json={"title": "Buy milk", "priority": "high"},
    )
    todo_id = created.json()["id"]

    completed = await client.post(f"/api/v1/todos/{todo_id}/complete", headers=auth(token))
    again = await client.post(f"/api/v1/todos/{todo_id}/complete", headers=auth(token))
    listed = await client.get("/api/v1/todos", headers=auth(token))

    assert completed.status_code == 200
    assert completed.json()["completed"] is True
    assert completed.json()["priority"] == "high"
    assert completed.json()["created_at"] == created.json()["created_at"]
    assert again.json()["updated_at"] == completed.json()["updated_at"]
    assert listed.json()[0]["completed"] is True


async def test_complete_unknown_or_other_owner_is_not_found(client) -> None:
    _, owner_token = await create_person(client)
    _, other_token = await create_person(client)
    created = await client.post(
        "/api/v1/todos", headers=auth(owner_token), json={"title": "Buy milk"}
    )
    todo_id = created.json()["id"]

    other = await client.post(f"/api/v1/todos/{todo_id}/complete", headers=auth(other_token))
    missing = await client.post(f"/api/v1/todos/{uuid4()}/complete", headers=auth(owner_token))
    anonymous = await client.post(f"/api/v1/todos/{todo_id}/complete")

    assert other.status_code == 404
    assert other.json()["error"]["message"] == "Todo not found"
    assert missing.status_code == 404
    assert anonymous.status_code == 401
    stored = await client.get(f"/api/v1/todos/{todo_id}", headers=auth(owner_token))
    assert stored.json()["completed"] is False
