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

## CI

GitHub Actions runs [`.github/workflows/ci.yml`](.github/workflows/ci.yml) on pull requests to `main` and on pushes to `main`. The workflow uses Python 3.12 and four independent jobs. Each job checks out the repo, installs `backend` with the `dev` extra, and runs from `backend/`:

| Job | Command |
| --- | --- |
| Ruff Lint | `ruff check .` |
| Ruff Format | `ruff format --check .` |
| Mypy | `mypy src` |
| Pytest | `python -m pytest --cov=todo_api --cov-report=term-missing --cov-report=xml:coverage.xml --cov-fail-under=90` |

Pytest is the coverage gate. The job fails when total coverage of `todo_api` drops below 90%.

Run the same checks locally from `backend/` with the virtual environment active:

```bash
ruff check .
ruff format --check .
mypy src
python -m pytest \
  --cov=todo_api \
  --cov-report=term-missing \
  --cov-fail-under=90
```

## Branch protection

`main` is protected by a GitHub repository ruleset:

- Changes reach `main` through a pull request.
- The CI status checks above must pass before merge.
- The branch must be up to date before merge.
- History stays linear. Squash merge is the merge method.
- Force pushes and deletion of `main` are blocked.
- Signed commits are not required.
- The remote head branch is deleted after merge.

```text
Update main
    |
Create a short-lived branch
    |
Make changes and run the local checks
    |
Open a pull request
    |
Ruff Lint, Ruff Format, Mypy, and Pytest pass
    |
Squash merge into main
    |
Remote branch is deleted
```

After a squash merge, clean up the local branch:

```bash
git checkout main
git pull origin main
git fetch --prune
git branch -D <branch-name>
```

`-D` is required after a squash merge. Git records a new commit on `main`, so the original branch commits are not ancestors of `main`.
