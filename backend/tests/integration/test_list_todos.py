from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from todo_api.core.tokens import hash_token
from todo_api.repositories.protocols import TodoView
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository


async def test_list_orders_newest_first_and_excludes_other_owners(session_factory) -> None:
    older = datetime(2026, 1, 1, tzinfo=UTC)
    newer = older + timedelta(days=1)
    low_id = UUID(int=1)
    high_id = UUID(int=2)

    async with session_factory() as session:
        users = SqlAlchemyUserRepository(session)
        owner = await users.create(hash_token("owner"))
        other = await users.create(hash_token("other"))
        repository = SqlAlchemyTodoRepository(session)
        await repository.add(owner, _todo(low_id, "Low", newer))
        await repository.add(owner, _todo(high_id, "High", newer))
        await repository.add(owner, _todo(uuid4(), "Older", older))
        await repository.add(other, _todo(uuid4(), "Hidden", newer))
        await session.commit()

    async with session_factory() as session:
        listed = await SqlAlchemyTodoRepository(session).list_for_owner(owner)

    assert [todo.title for todo in listed] == ["High", "Low", "Older"]


def _todo(todo_id: UUID, title: str, moment: datetime) -> TodoView:
    return TodoView(
        id=todo_id,
        title=title,
        description=None,
        completed=False,
        priority="medium",
        created_at=moment,
        updated_at=moment,
    )
