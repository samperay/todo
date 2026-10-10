from datetime import datetime
from typing import Protocol
from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True)
class TodoView:
    id: UUID
    title: str
    description: str | None
    completed: bool
    priority: str
    created_at: datetime
    updated_at: datetime


class TodoRepository(Protocol):
    async def add(self, owner_id: UUID, todo: TodoView) -> TodoView: ...

    async def list_for_owner(self, owner_id: UUID) -> list[TodoView]: ...

    async def get_for_owner(self, owner_id: UUID, todo_id: UUID) -> TodoView | None: ...

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
    ) -> TodoView | None: ...

    async def set_completed(
        self, owner_id: UUID, todo_id: UUID, completed: bool
    ) -> TodoView | None: ...

    async def delete(self, owner_id: UUID, todo_id: UUID) -> bool: ...


class UserRepository(Protocol):
    async def create(self, token_hash: str) -> UUID: ...

    async def get_id_by_token_hash(self, token_hash: str) -> UUID | None: ...
