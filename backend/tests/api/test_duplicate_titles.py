from tests.api_helpers import auth, create_person


async def test_duplicate_titles_are_allowed_and_identity_is_the_id(client) -> None:
    _, first_token = await create_person(client)
    _, second_token = await create_person(client)

    one = await client.post(
        "/api/v1/todos", headers=auth(first_token), json={"title": "Buy milk"}
    )
    two = await client.post(
        "/api/v1/todos", headers=auth(first_token), json={"title": "Buy milk"}
    )
    other = await client.post(
        "/api/v1/todos", headers=auth(second_token), json={"title": "Buy milk"}
    )
    assert one.status_code == two.status_code == other.status_code == 201
    ids = {one.json()["id"], two.json()["id"], other.json()["id"]}
    assert len(ids) == 3

    listed = await client.get("/api/v1/todos", headers=auth(first_token))
    assert len(listed.json()) == 2
    assert {item["title"] for item in listed.json()} == {"Buy milk"}
