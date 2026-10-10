from datetime import datetime, timezone
from uuid import UUID, uuid4

from todo_api.repositories.protocols import TodoRepository, TodoView
from todo_api.services.errors import TodoNotFound


class TodoService:
    def __init__(self, repository: TodoRepository) -> None:
        self._repository = repository

    async def create(
        self,
        owner_id: UUID,
        title: str,
        description: str | None,
        priority: str | None = None,
    ) -> TodoView:
        now = datetime.now(timezone.utc)
        todo = TodoView(
            id=uuid4(),
            title=title,
            description=description,
            completed=False,
            priority=priority if priority is not None else "medium",
            created_at=now,
            updated_at=now,
        )
        return await self._repository.add(owner_id, todo)

    async def list_todos(self, owner_id: UUID) -> list[TodoView]:
        return await self._repository.list_for_owner(owner_id)

    async def get(self, owner_id: UUID, todo_id: UUID) -> TodoView:
        todo = await self._repository.get_for_owner(owner_id, todo_id)
        if todo is None:
            raise TodoNotFound()
        return todo

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
    ) -> TodoView:
        todo = await self._repository.update(
            owner_id,
            todo_id,
            title=title,
            description=description,
            priority=priority,
            set_title=set_title,
            set_description=set_description,
            set_priority=set_priority,
        )
        if todo is None:
            raise TodoNotFound()
        return todo

    async def mark_completed(self, owner_id: UUID, todo_id: UUID) -> TodoView:
        return await self._set_completed(owner_id, todo_id, True)

    async def mark_incomplete(self, owner_id: UUID, todo_id: UUID) -> TodoView:
        return await self._set_completed(owner_id, todo_id, False)

    async def delete(self, owner_id: UUID, todo_id: UUID) -> None:
        deleted = await self._repository.delete(owner_id, todo_id)
        if not deleted:
            raise TodoNotFound()

    async def _set_completed(
        self, owner_id: UUID, todo_id: UUID, completed: bool
    ) -> TodoView:
        todo = await self._repository.set_completed(owner_id, todo_id, completed)
        if todo is None:
            raise TodoNotFound()
        return todo
