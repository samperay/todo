from uuid import uuid4

from todo_api.core.tokens import hash_token
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository
from todo_api.services.todo_service import TodoService


async def test_later_fields_replace_earlier_ones_and_deleted_ids_stay_gone(
    session_factory,
) -> None:
    async with session_factory() as session:
        owner = await SqlAlchemyUserRepository(session).create(hash_token("owner"))
        repository = SqlAlchemyTodoRepository(session)
        service = TodoService(repository)
        created = await service.create(owner, "Buy milk", "1 liter")
        await service.update(owner, created.id, title="Buy oat milk", set_title=True)
        later = await service.update(
            owner,
            created.id,
            title="Buy milk",
            description="2 liters",
            set_title=True,
            set_description=True,
        )
        await service.delete(owner, created.id)
        missing = await repository.update(
            owner, created.id, title="Back", set_title=True
        )
        await session.commit()

    assert later.title == "Buy milk"
    assert later.description == "2 liters"
    assert missing is None
    assert created.id != uuid4()


async def test_priority_column_changes_only_when_supplied_and_different(
    session_factory,
) -> None:
    async with session_factory() as session:
        owner = await SqlAlchemyUserRepository(session).create(hash_token("owner"))
        service = TodoService(SqlAlchemyTodoRepository(session))
        created = await service.create(owner, "Buy milk", "1 liter", priority="high")
        renamed = await service.update(
            owner, created.id, title="Buy oat milk", set_title=True
        )
        lowered = await service.update(
            owner, created.id, priority="low", set_priority=True
        )
        same = await service.update(owner, created.id, priority="low", set_priority=True)
        await session.commit()

    assert renamed.priority == "high"
    assert lowered.priority == "low"
    assert lowered.title == "Buy oat milk"
    assert lowered.description == "1 liter"
    assert same.updated_at == lowered.updated_at
