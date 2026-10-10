from uuid import uuid4

import pytest

from todo_api.services.errors import TodoNotFound
from todo_api.services.todo_service import TodoService
from tests.fakes import MemoryTodoRepository


async def test_delete_is_permanent_and_does_not_recreate() -> None:
    repository = MemoryTodoRepository()
    service = TodoService(repository)
    owner = uuid4()
    created = await service.create(owner, "Buy milk", None)
    other = await service.create(owner, "Keep", None)

    await service.delete(owner, created.id)

    with pytest.raises(TodoNotFound):
        await service.delete(owner, created.id)
    with pytest.raises(TodoNotFound):
        await service.update(owner, created.id, title="Back", set_title=True)
    assert await repository.get_for_owner(owner, created.id) is None
    assert (await service.get(owner, other.id)).title == "Keep"
