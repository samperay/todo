from todo_api.core.tokens import hash_token
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository
from todo_api.services.todo_service import TodoService


async def test_updated_at_changes_only_when_completed_changes(session_factory) -> None:
    async with session_factory() as session:
        owner = await SqlAlchemyUserRepository(session).create(hash_token("owner"))
        service = TodoService(SqlAlchemyTodoRepository(session))
        created = await service.create(owner, "Buy milk", None)
        completed = await service.mark_completed(owner, created.id)
        again = await service.mark_completed(owner, created.id)
        await session.commit()

    assert completed.completed is True
    assert completed.updated_at > created.updated_at
    assert again.updated_at == completed.updated_at
    assert again.created_at == created.created_at
    assert completed.priority == created.priority
    assert again.priority == created.priority
