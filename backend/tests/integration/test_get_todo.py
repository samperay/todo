from todo_api.core.tokens import hash_token
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository
from todo_api.services.todo_service import TodoService


async def test_owner_query_cannot_read_another_owners_row(session_factory) -> None:
    async with session_factory() as session:
        users = SqlAlchemyUserRepository(session)
        owner = await users.create(hash_token("owner"))
        other = await users.create(hash_token("other"))
        created = await TodoService(SqlAlchemyTodoRepository(session)).create(
            owner, "Buy milk", None
        )
        await session.commit()
        todo_id = created.id

    async with session_factory() as session:
        repository = SqlAlchemyTodoRepository(session)
        assert await repository.get_for_owner(owner, todo_id) is not None
        assert await repository.get_for_owner(other, todo_id) is None
