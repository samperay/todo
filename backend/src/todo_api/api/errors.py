from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from todo_api.services.errors import TodoNotFound


class Unauthenticated(Exception):
    """The caller did not present a known bearer token."""


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(TodoNotFound)
    async def todo_not_found(_request: Request, _exc: TodoNotFound) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"error": {"code": "not_found", "message": "Todo not found"}},
        )

    @app.exception_handler(Unauthenticated)
    async def unauthenticated(_request: Request, _exc: Unauthenticated) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={
                "error": {
                    "code": "unauthenticated",
                    "message": "You must be identified.",
                }
            },
        )
