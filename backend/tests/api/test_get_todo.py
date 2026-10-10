from uuid import uuid4

from tests.api_helpers import auth, create_person


async def test_get_owned_todo_and_hide_others(client) -> None:
    _, owner_token = await create_person(client)
    _, other_token = await create_person(client)
    created = await client.post(
        "/api/v1/todos",
        headers=auth(owner_token),
        json={"title": "Buy milk", "description": "1 liter"},
    )
    todo_id = created.json()["id"]

    fetched = await client.get(f"/api/v1/todos/{todo_id}", headers=auth(owner_token))
    hidden = await client.get(f"/api/v1/todos/{todo_id}", headers=auth(other_token))
    missing = await client.get(f"/api/v1/todos/{uuid4()}", headers=auth(owner_token))
    anonymous = await client.get(f"/api/v1/todos/{todo_id}")

    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Buy milk"
    assert fetched.json()["priority"] == "medium"
    assert hidden.status_code == 404
    assert hidden.json() == {"error": {"code": "not_found", "message": "Todo not found"}}
    assert missing.status_code == 404
    assert anonymous.status_code == 401
