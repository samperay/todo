from sqlalchemy.ext.asyncio import AsyncEngine

from todo_api.db.models import Base
from todo_api.db.models import PersonModel as PersonModel
from todo_api.db.models import TodoModel as TodoModel


async def init_schema(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
