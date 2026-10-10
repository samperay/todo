from typing import Annotated

from fastapi import APIRouter, Depends

from todo_api.api.deps import get_user_repository
from todo_api.core.tokens import generate_token, hash_token
from todo_api.repositories.protocols import UserRepository
from todo_api.schemas.user import UserCreated

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", status_code=201)
async def create_user(
    users: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserCreated:
    token = generate_token()
    person_id = await users.create(hash_token(token))
    return UserCreated(id=person_id, token=token)
