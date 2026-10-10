from todo_api.core.tokens import hash_token
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository
from todo_api.services.todo_service import TodoService


async def test_incomplete_noop_does_not_move_updated_at(session_factory) -> None:
    async with session_factory() as session:
        owner = await SqlAlchemyUserRepository(session).create(hash_token("owner"))
        service = TodoService(SqlAlchemyTodoRepository(session))
        created = await service.create(owner, "Buy milk", None)
        first = await service.mark_incomplete(owner, created.id)
        second = await service.mark_incomplete(owner, created.id)
        await session.commit()

    assert first.updated_at == created.updated_at
    assert second.updated_at == first.updated_at
    assert second.completed is False
    assert first.priority == created.priority
    assert second.priority == created.priority
