from tests.api_helpers import auth, create_person
from todo_api.core.tokens import hash_token
from todo_api.db.models import PersonModel


async def test_create_user_returns_token_once_and_stores_a_hash(client) -> None:
    response = await client.post("/api/v1/users")
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"id", "token"}

    session_factory = client.app_under_test.state.session_factory
    from uuid import UUID

    async with session_factory() as session:
        row = await session.get(PersonModel, UUID(body["id"]))
        assert row is not None
        assert row.token_hash != body["token"]
        assert row.token_hash == hash_token(body["token"])


async def test_same_token_identifies_the_same_person(client) -> None:
    _, token = await create_person(client)
    first = await client.get("/api/v1/todos", headers=auth(token))
    second = await client.get("/api/v1/todos", headers=auth(token))
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == []
    assert second.json() == []


async def test_missing_or_unknown_token_is_rejected(client) -> None:
    missing = await client.get("/api/v1/todos")
    unknown = await client.get("/api/v1/todos", headers=auth("not-a-real-token"))
    assert missing.status_code == 401
    assert unknown.status_code == 401
    assert missing.json() == {
        "error": {"code": "unauthenticated", "message": "You must be identified."}
    }
