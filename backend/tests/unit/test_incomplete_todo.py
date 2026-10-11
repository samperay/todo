from uuid import uuid4

from tests.fakes import MemoryTodoRepository
from todo_api.services.todo_service import TodoService


async def test_mark_incomplete_then_noop() -> None:
    service = TodoService(MemoryTodoRepository())
    owner = uuid4()
    created = await service.create(owner, "Buy milk", "1 liter")
    completed = await service.mark_completed(owner, created.id)

    opened = await service.mark_incomplete(owner, created.id)
    again = await service.mark_incomplete(owner, created.id)

    assert opened.completed is False
    assert opened.id == created.id
    assert opened.title == created.title
    assert opened.description == created.description
    assert opened.priority == created.priority
    assert opened.created_at == created.created_at
    assert opened.updated_at > completed.updated_at
    assert again == opened
