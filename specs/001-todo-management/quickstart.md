# Quickstart: Basic Todo Management

Validation guide for the backend described in [plan.md](./plan.md). Field rules are in [data-model.md](./data-model.md). Status codes and bodies are in [contracts/todos.openapi.yaml](./contracts/todos.openapi.yaml).

## Prerequisites

- Python 3.12 or newer
- No separate database server. Local development uses SQLite.

The default database URL is `sqlite+aiosqlite:///./todo.db`. Override it only when you want a different file:

```bash
export DATABASE_URL="sqlite+aiosqlite:///./todo.db"
```

Do not commit a URL that contains a password. The SQLite file default is not a secret.

## Setup

From `backend/` after the implementation exists:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Starting the app creates the person and todo tables with `Base.metadata.create_all()`. There is no migration command. Confirm those tables match [data-model.md](./data-model.md). Deleting the SQLite file and starting again recreates an empty schema.

## Automated checks

`pytest` uses a temporary SQLite file. It does not need PostgreSQL or an exported database URL.

```bash
pytest
```

Expected:

- Service unit tests pass without a live database. They cover create defaults, not-found for another owner's id, no-op complete and incomplete, and a later write that does not recreate a deleted id.
- Repository tests pass against SQLite. List order is newest `created_at` first, and a query for one owner returns none of another owner's rows.
- API tests pass against SQLite. They cover the status codes below.

## Manual API check

Start the app from `backend/` with the same `DATABASE_URL`:

```bash
uvicorn todo_api.main:app --reload
```

Create two people. Save each `token`. The token is not shown again.

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/users
curl -s -X POST http://127.0.0.1:8000/api/v1/users
```

Use person A's token as `TOKEN`.

1. **Create.** `POST /api/v1/todos` with `{"title":"Buy milk","description":"1 liter"}` and `Authorization: Bearer $TOKEN` returns 201. `completed` is false. `created_at` equals `updated_at`. The body has `id`, `title`, `description`, `completed`, `created_at`, and `updated_at`, and no owner field.
2. **Title only.** `POST /api/v1/todos` with `{"title":"Walk"}` returns 201 and `description` is null.
3. **Reject title.** Missing title, `"   "`, or a 201-character title returns 422. A following list does not include a new row.
4. **Reject description.** A description longer than 2,000 characters returns 422.
5. **List.** `GET /api/v1/todos` returns only A's todos, newest first.
6. **Retrieve.** `GET /api/v1/todos/{id}` returns that todo.
7. **Update.** `PATCH /api/v1/todos/{id}` with `{"title":"Buy oat milk"}` leaves `description` and `completed` unchanged and moves `updated_at`.
8. **Clear description.** `PATCH` with `{"description":null}` stores no description.
9. **Complete.** `POST /api/v1/todos/{id}/complete` sets `completed` to true. Calling it again returns 200 and does not change `updated_at`. The todo remains in the list.
10. **Incomplete.** `POST /api/v1/todos/{id}/incomplete` sets `completed` to false and keeps `id`, `title`, `description`, and `created_at`. Calling it again changes nothing.
11. **Other person.** Person B's token on A's id for retrieve, patch, complete, incomplete, and delete returns 404 `Todo not found`. A's list still contains the todo. B's list does not.
12. **Delete.** A's `DELETE /api/v1/todos/{id}` returns 204. A second delete, and a later get, return 404. The id is not issued again.
13. **No token.** Any todo call without `Authorization` returns 401 `You must be identified.` and does not change stored todos.
14. **Overlap.** Two patches that both send `title` and `description`, with the later one using title `Buy milk` and description `2 liters`, leave that later pair stored. The response is not a conflict error.

## Done when

- `pytest` is green on SQLite.
- The fourteen checks match the contract.
- Route modules contain no SQL and no ownership rules; those stay in the service and repository.
