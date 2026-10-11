from uuid import uuid4

from tests.fakes import MemoryTodoRepository
from todo_api.services.todo_service import TodoService


async def test_create_is_incomplete_and_owned() -> None:
    repository = MemoryTodoRepository()
    service = TodoService(repository)
    owner_id = uuid4()

    todo = await service.create(owner_id, "Buy milk", "1 liter")

    assert todo.completed is False
    assert todo.created_at == todo.updated_at
    assert todo.title == "Buy milk"
    assert todo.description == "1 liter"
    stored = await repository.get_for_owner(owner_id, todo.id)
    assert stored == todo
    assert await repository.get_for_owner(uuid4(), todo.id) is None


async def test_create_without_description() -> None:
    service = TodoService(MemoryTodoRepository())
    todo = await service.create(uuid4(), "Walk", None)
    assert todo.description is None
    assert todo.completed is False


async def test_omitted_priority_is_medium() -> None:
    service = TodoService(MemoryTodoRepository())
    todo = await service.create(uuid4(), "Walk", None)
    assert todo.priority == "medium"


async def test_create_stores_allowed_priority() -> None:
    service = TodoService(MemoryTodoRepository())
    for value in ("low", "medium", "high"):
        todo = await service.create(uuid4(), "Walk", None, priority=value)
        assert todo.priority == value
