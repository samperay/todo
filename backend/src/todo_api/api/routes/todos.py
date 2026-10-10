from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from todo_api.api.deps import get_current_user_id, get_todo_service
from todo_api.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from todo_api.services.todo_service import TodoService

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


@router.post("", status_code=201)
async def create_todo(
    body: TodoCreate,
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> TodoResponse:
    todo = await service.create(owner_id, body.title, body.description, body.priority)
    return TodoResponse.model_validate(todo)


@router.get("")
async def list_todos(
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> list[TodoResponse]:
    todos = await service.list_todos(owner_id)
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.get("/{todo_id}")
async def get_todo(
    todo_id: UUID,
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> TodoResponse:
    todo = await service.get(owner_id, todo_id)
    return TodoResponse.model_validate(todo)


@router.patch("/{todo_id}")
async def update_todo(
    todo_id: UUID,
    body: TodoUpdate,
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> TodoResponse:
    fields = body.model_dump(exclude_unset=True)
    todo = await service.update(
        owner_id,
        todo_id,
        title=fields.get("title"),
        description=fields.get("description"),
        priority=fields.get("priority"),
        set_title="title" in fields,
        set_description="description" in fields,
        set_priority="priority" in fields,
    )
    return TodoResponse.model_validate(todo)


@router.post("/{todo_id}/complete")
async def complete_todo(
    todo_id: UUID,
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> TodoResponse:
    todo = await service.mark_completed(owner_id, todo_id)
    return TodoResponse.model_validate(todo)


@router.post("/{todo_id}/incomplete")
async def incomplete_todo(
    todo_id: UUID,
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> TodoResponse:
    todo = await service.mark_incomplete(owner_id, todo_id)
    return TodoResponse.model_validate(todo)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: UUID,
    owner_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[TodoService, Depends(get_todo_service)],
) -> Response:
    await service.delete(owner_id, todo_id)
    return Response(status_code=204)
