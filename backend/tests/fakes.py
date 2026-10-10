from uuid import UUID

from todo_api.repositories.protocols import TodoView


class MemoryTodoRepository:
    def __init__(self) -> None:
        self.rows: dict[tuple[UUID, UUID], TodoView] = {}

    async def add(self, owner_id: UUID, todo: TodoView) -> TodoView:
        self.rows[(owner_id, todo.id)] = todo
        return todo

    async def list_for_owner(self, owner_id: UUID) -> list[TodoView]:
        owned = [todo for (owner, _), todo in self.rows.items() if owner == owner_id]
        return sorted(owned, key=lambda todo: (todo.created_at, todo.id.int), reverse=True)

    async def get_for_owner(self, owner_id: UUID, todo_id: UUID) -> TodoView | None:
        return self.rows.get((owner_id, todo_id))

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
        current = self.rows.get((owner_id, todo_id))
        if current is None:
            return None
        new_title = title if set_title and title is not None else current.title
        new_description = description if set_description else current.description
        new_priority = (
            priority if set_priority and priority is not None else current.priority
        )
        changed = (
            new_title != current.title
            or new_description != current.description
            or new_priority != current.priority
        )
        updated = TodoView(
            id=current.id,
            title=new_title,
            description=new_description,
            completed=current.completed,
            priority=new_priority,
            created_at=current.created_at,
            updated_at=current.updated_at,
        )
        if changed:
            from datetime import datetime, timezone

            updated = TodoView(
                id=updated.id,
                title=updated.title,
                description=updated.description,
                completed=updated.completed,
                priority=updated.priority,
                created_at=updated.created_at,
                updated_at=datetime.now(timezone.utc),
            )
        self.rows[(owner_id, todo_id)] = updated
        return updated

    async def set_completed(
        self, owner_id: UUID, todo_id: UUID, completed: bool
    ) -> TodoView | None:
        current = self.rows.get((owner_id, todo_id))
        if current is None:
            return None
        if current.completed == completed:
            return current
        from datetime import datetime, timezone

        updated = TodoView(
            id=current.id,
            title=current.title,
            description=current.description,
            completed=completed,
            priority=current.priority,
            created_at=current.created_at,
            updated_at=datetime.now(timezone.utc),
        )
        self.rows[(owner_id, todo_id)] = updated
        return updated

    async def delete(self, owner_id: UUID, todo_id: UUID) -> bool:
        return self.rows.pop((owner_id, todo_id), None) is not None
