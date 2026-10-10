# todo

Personal todo API. Each person gets a bearer token and can create, list, update, complete, and delete their own todos.

## Prerequisites

- Python 3.12 or newer

Local development uses SQLite. There is no separate database server and no migration command. Starting the app creates the tables.

## Setup

From `backend/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

The default database is `sqlite+aiosqlite:///./todo.db`, created in the directory you start the app from. Override it only when you want a different file:

```bash
export DATABASE_URL="sqlite+aiosqlite:///./todo.db"
```

Do not commit a URL that contains a password. Deleting the SQLite file and starting again recreates an empty schema.

## Run

From `backend/`, with the virtual environment active:

```bash
uvicorn todo_api.main:app --reload
```

The API listens on `http://127.0.0.1:8000`. Interactive docs are at `http://127.0.0.1:8000/docs`.

Create a person and save the token. It is shown only once:

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/users
```

Use that token on todo requests:

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/todos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","description":"1 liter"}'
```

## Tests

From `backend/`, with the virtual environment active:

```bash
pytest
```

Tests use a temporary SQLite file. They do not need `DATABASE_URL`.
# Branch protection test
