from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from todo_api.api.errors import register_exception_handlers
from todo_api.api.routes.todos import router as todos_router
from todo_api.api.routes.users import router as users_router
from todo_api.core.config import Settings, get_settings
from todo_api.db.schema import init_schema
from todo_api.db.session import create_engine, create_session_factory


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings if settings is not None else get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(resolved.database_url)
        await init_schema(engine)
        app.state.session_factory = create_session_factory(engine)
        try:
            yield
        finally:
            await engine.dispose()

    app = FastAPI(title="Todo API", lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(users_router)
    app.include_router(todos_router)
    return app


app = create_app()
