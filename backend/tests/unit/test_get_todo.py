from uuid import uuid4

import pytest

from tests.fakes import MemoryTodoRepository
from todo_api.services.errors import TodoNotFound
from todo_api.services.todo_service import TodoService


async def test_get_returns_owned_todo() -> None:
    service = TodoService(MemoryTodoRepository())
    owner = uuid4()
    created = await service.create(owner, "Buy milk", "1 liter")

    fetched = await service.get(owner, created.id)

    assert fetched == created


async def test_get_hides_other_owners() -> None:
    service = TodoService(MemoryTodoRepository())
    owner = uuid4()
    created = await service.create(owner, "Buy milk", None)

    with pytest.raises(TodoNotFound):
        await service.get(uuid4(), created.id)
    with pytest.raises(TodoNotFound):
        await service.get(owner, uuid4())
