from todo_api.core.tokens import hash_token
from todo_api.db.models import PersonModel
from todo_api.repositories.user_repository import SqlAlchemyUserRepository


async def test_token_is_stored_as_a_hash(session_factory) -> None:
    token = "plain-token"
    async with session_factory() as session:
        repository = SqlAlchemyUserRepository(session)
        person_id = await repository.create(hash_token(token))
        await session.commit()

    async with session_factory() as session:
        row = await session.get(PersonModel, person_id)
        assert row is not None
        assert row.token_hash != token
        assert row.token_hash == hash_token(token)
        found = await SqlAlchemyUserRepository(session).get_id_by_token_hash(row.token_hash)
        assert found == person_id
