from uuid import uuid4

from tests.fakes import MemoryTodoRepository
from todo_api.services.todo_service import TodoService


async def test_list_returns_only_the_owners_todos() -> None:
    repository = MemoryTodoRepository()
    service = TodoService(repository)
    owner = uuid4()
    other = uuid4()
    mine = await service.create(owner, "Mine", None)
    await service.create(other, "Theirs", None)

    listed = await service.list_todos(owner)

    assert [todo.id for todo in listed] == [mine.id]


async def test_list_is_empty_when_the_owner_has_none() -> None:
    service = TodoService(MemoryTodoRepository())
    await service.create(uuid4(), "Theirs", None)
    assert await service.list_todos(uuid4()) == []
