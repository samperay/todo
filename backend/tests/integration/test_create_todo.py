from uuid import uuid4

from todo_api.core.tokens import hash_token
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository
from todo_api.services.todo_service import TodoService


async def test_todo_is_stored_for_the_creator_only(session_factory) -> None:
    async with session_factory() as session:
        users = SqlAlchemyUserRepository(session)
        owner = await users.create(hash_token("owner"))
        other = await users.create(hash_token("other"))
        service = TodoService(SqlAlchemyTodoRepository(session))
        todo = await service.create(owner, "Buy milk", "1 liter")
        await session.commit()
        todo_id = todo.id

    async with session_factory() as session:
        repository = SqlAlchemyTodoRepository(session)
        stored = await repository.get_for_owner(owner, todo_id)
        assert stored is not None
        assert stored.title == "Buy milk"
        assert await repository.get_for_owner(other, todo_id) is None
        assert await repository.get_for_owner(uuid4(), todo_id) is None


async def test_priority_is_stored(session_factory) -> None:
    async with session_factory() as session:
        owner = await SqlAlchemyUserRepository(session).create(hash_token("owner"))
        service = TodoService(SqlAlchemyTodoRepository(session))
        omitted = await service.create(owner, "Walk", None)
        high = await service.create(owner, "Run", None, priority="high")
        low = await service.create(owner, "Rest", None, priority="low")
        medium = await service.create(owner, "Read", None, priority="medium")
        await session.commit()

    assert omitted.priority == "medium"
    assert high.priority == "high"
    assert low.priority == "low"
    assert medium.priority == "medium"
