from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.db.models import PersonModel


class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, token_hash: str) -> UUID:
        person = PersonModel(
            id=uuid4(),
            token_hash=token_hash,
            created_at=datetime.now(UTC),
        )
        self._session.add(person)
        await self._session.flush()
        return person.id

    async def get_id_by_token_hash(self, token_hash: str) -> UUID | None:
        result = await self._session.execute(
            select(PersonModel.id).where(PersonModel.token_hash == token_hash)
        )
        return result.scalar_one_or_none()
