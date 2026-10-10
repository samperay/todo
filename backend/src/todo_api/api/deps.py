from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.api.errors import Unauthenticated
from todo_api.core.tokens import hash_token
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository
from todo_api.services.todo_service import TodoService

_bearer = HTTPBearer(auto_error=False)


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory = request.app.state.session_factory
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)


async def get_todo_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TodoService:
    return TodoService(SqlAlchemyTodoRepository(session))


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    users: Annotated[SqlAlchemyUserRepository, Depends(get_user_repository)],
) -> UUID:
    if credentials is None or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise Unauthenticated()
    person_id = await users.get_id_by_token_hash(hash_token(credentials.credentials))
    if person_id is None:
        raise Unauthenticated()
    return person_id
