from uuid import uuid4

from todo_api.services.todo_service import TodoService
from tests.fakes import MemoryTodoRepository


async def test_later_request_wins_only_supplied_fields() -> None:
    service = TodoService(MemoryTodoRepository())
    owner = uuid4()
    created = await service.create(owner, "Buy milk", "1 liter")

    await service.update(owner, created.id, title="Buy oat milk", set_title=True)
    later = await service.update(
        owner,
        created.id,
        title="Buy milk",
        description="2 liters",
        set_title=True,
        set_description=True,
    )

    assert later.title == "Buy milk"
    assert later.description == "2 liters"

    title_only = await service.update(owner, created.id, title="Oats", set_title=True)
    description_only = await service.update(
        owner, created.id, description="2 liters", set_description=True
    )
    assert description_only.title == "Oats"
    assert description_only.description == "2 liters"
    assert title_only.id == created.id
