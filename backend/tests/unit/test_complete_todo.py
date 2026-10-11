from uuid import uuid4

import pytest

from tests.fakes import MemoryTodoRepository
from todo_api.services.errors import TodoNotFound
from todo_api.services.todo_service import TodoService


async def test_mark_completed_then_noop() -> None:
    service = TodoService(MemoryTodoRepository())
    owner = uuid4()
    created = await service.create(owner, "Buy milk", None)

    completed = await service.mark_completed(owner, created.id)
    again = await service.mark_completed(owner, created.id)

    assert completed.completed is True
    assert completed.id == created.id
    assert completed.title == created.title
    assert completed.priority == created.priority
    assert completed.created_at == created.created_at
    assert completed.updated_at > created.updated_at
    assert again == completed


async def test_complete_unknown_or_other_owner_is_not_found() -> None:
    service = TodoService(MemoryTodoRepository())
    owner = uuid4()
    created = await service.create(owner, "Buy milk", None)

    with pytest.raises(TodoNotFound):
        await service.mark_completed(owner, uuid4())
    with pytest.raises(TodoNotFound):
        await service.mark_completed(uuid4(), created.id)
    assert (await service.get(owner, created.id)).completed is False
