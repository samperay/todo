from uuid import UUID

from pydantic import BaseModel


class UserCreated(BaseModel):
    id: UUID
    token: str
