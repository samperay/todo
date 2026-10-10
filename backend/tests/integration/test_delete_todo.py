from todo_api.core.tokens import hash_token
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository
from todo_api.services.todo_service import TodoService


async def test_delete_removes_only_the_owners_row(session_factory) -> None:
    async with session_factory() as session:
        users = SqlAlchemyUserRepository(session)
        owner = await users.create(hash_token("owner"))
        other = await users.create(hash_token("other"))
        service = TodoService(SqlAlchemyTodoRepository(session))
        mine = await service.create(owner, "Mine", None)
        theirs = await service.create(other, "Theirs", None)
        await service.delete(owner, mine.id)
        await session.commit()
        mine_id = mine.id
        theirs_id = theirs.id

    async with session_factory() as session:
        repository = SqlAlchemyTodoRepository(session)
        assert await repository.get_for_owner(owner, mine_id) is None
        assert await repository.get_for_owner(other, theirs_id) is not None
