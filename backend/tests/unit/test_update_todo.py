from uuid import uuid4

import pytest

from tests.fakes import MemoryTodoRepository
from todo_api.services.errors import TodoNotFound
from todo_api.services.todo_service import TodoService


async def test_partial_update_and_clear_description() -> None:
    service = TodoService(MemoryTodoRepository())
    owner = uuid4()
    created = await service.create(owner, "Buy milk", "1 liter")

    renamed = await service.update(owner, created.id, title="Buy oat milk", set_title=True)
    cleared = await service.update(owner, created.id, description=None, set_description=True)

    assert renamed.description == "1 liter"
    assert renamed.completed is False
    assert renamed.created_at == created.created_at
    assert renamed.updated_at > created.updated_at
    assert cleared.title == "Buy oat milk"
    assert cleared.description is None


async def test_priority_only_update_leaves_other_fields() -> None:
    service = TodoService(MemoryTodoRepository())
    owner = uuid4()
    created = await service.create(owner, "Buy milk", "1 liter", priority="high")

    renamed = await service.update(owner, created.id, title="Buy oat milk", set_title=True)
    lowered = await service.update(owner, created.id, priority="low", set_priority=True)
    same = await service.update(owner, created.id, priority="low", set_priority=True)

    assert renamed.priority == "high"
    assert renamed.description == "1 liter"
    assert lowered.priority == "low"
    assert lowered.title == "Buy oat milk"
    assert lowered.description == "1 liter"
    assert lowered.updated_at > renamed.updated_at
    assert same.updated_at == lowered.updated_at
    for value in ("low", "medium", "high"):
        stored = await service.update(owner, created.id, priority=value, set_priority=True)
        assert stored.priority == value


async def test_update_missing_todo_is_not_found() -> None:
    service = TodoService(MemoryTodoRepository())
    with pytest.raises(TodoNotFound):
        await service.update(uuid4(), uuid4(), title="Nope", set_title=True)
