from tests.api_helpers import auth, create_person


async def test_delete_is_permanent(client) -> None:
    _, owner_token = await create_person(client)
    _, other_token = await create_person(client)
    mine = await client.post("/api/v1/todos", headers=auth(owner_token), json={"title": "Mine"})
    theirs = await client.post("/api/v1/todos", headers=auth(other_token), json={"title": "Theirs"})
    todo_id = mine.json()["id"]

    deleted = await client.delete(f"/api/v1/todos/{todo_id}", headers=auth(owner_token))
    again = await client.delete(f"/api/v1/todos/{todo_id}", headers=auth(owner_token))
    fetched = await client.get(f"/api/v1/todos/{todo_id}", headers=auth(owner_token))
    listed = await client.get("/api/v1/todos", headers=auth(owner_token))
    other_listed = await client.get("/api/v1/todos", headers=auth(other_token))

    assert deleted.status_code == 204
    assert deleted.content == b""
    assert again.status_code == 404
    assert again.json()["error"]["message"] == "Todo not found"
    assert fetched.status_code == 404
    assert listed.json() == []
    assert [item["id"] for item in other_listed.json()] == [theirs.json()["id"]]


async def test_delete_other_owner_or_anonymous_changes_nothing(client) -> None:
    _, owner_token = await create_person(client)
    _, other_token = await create_person(client)
    created = await client.post("/api/v1/todos", headers=auth(owner_token), json={"title": "Mine"})
    todo_id = created.json()["id"]
    other = await client.delete(f"/api/v1/todos/{todo_id}", headers=auth(other_token))
    anonymous = await client.delete(f"/api/v1/todos/{todo_id}")
    stored = await client.get(f"/api/v1/todos/{todo_id}", headers=auth(owner_token))
    assert other.status_code == 404
    assert anonymous.status_code == 401
    assert stored.status_code == 200
