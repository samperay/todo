from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.db.models import TodoModel
from todo_api.repositories.protocols import TodoView


class SqlAlchemyTodoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, owner_id: UUID, todo: TodoView) -> TodoView:
        row = TodoModel(
            id=todo.id,
            owner_id=owner_id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            priority=todo.priority,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )
        self._session.add(row)
        await self._session.flush()
        return _to_view(row)

    async def list_for_owner(self, owner_id: UUID) -> list[TodoView]:
        result = await self._session.execute(
            select(TodoModel)
            .where(TodoModel.owner_id == owner_id)
            .order_by(TodoModel.created_at.desc(), TodoModel.id.desc())
        )
        return [_to_view(row) for row in result.scalars().all()]

    async def get_for_owner(self, owner_id: UUID, todo_id: UUID) -> TodoView | None:
        row = await self._get_row(owner_id, todo_id)
        if row is None:
            return None
        return _to_view(row)

    async def update(
        self,
        owner_id: UUID,
        todo_id: UUID,
        *,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        set_title: bool = False,
        set_description: bool = False,
        set_priority: bool = False,
    ) -> TodoView | None:
        row = await self._get_row(owner_id, todo_id)
        if row is None:
            return None
        changed = False
        if set_title and title is not None and title != row.title:
            row.title = title
            changed = True
        if set_description and description != row.description:
            row.description = description
            changed = True
        if set_priority and priority is not None and priority != row.priority:
            row.priority = priority
            changed = True
        if changed:
            row.updated_at = datetime.now(timezone.utc)
        await self._session.flush()
        return _to_view(row)

    async def set_completed(
        self, owner_id: UUID, todo_id: UUID, completed: bool
    ) -> TodoView | None:
        row = await self._get_row(owner_id, todo_id)
        if row is None:
            return None
        if row.completed != completed:
            row.completed = completed
            row.updated_at = datetime.now(timezone.utc)
            await self._session.flush()
        return _to_view(row)

    async def delete(self, owner_id: UUID, todo_id: UUID) -> bool:
        row = await self._get_row(owner_id, todo_id)
        if row is None:
            return False
        await self._session.delete(row)
        await self._session.flush()
        return True

    async def _get_row(self, owner_id: UUID, todo_id: UUID) -> TodoModel | None:
        result = await self._session.execute(
            select(TodoModel).where(
                TodoModel.id == todo_id,
                TodoModel.owner_id == owner_id,
            )
        )
        return result.scalar_one_or_none()


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _to_view(row: TodoModel) -> TodoView:
    return TodoView(
        id=row.id,
        title=row.title,
        description=row.description,
        completed=row.completed,
        priority=row.priority,
        created_at=_as_utc(row.created_at),
        updated_at=_as_utc(row.updated_at),
    )
