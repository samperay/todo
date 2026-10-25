# Quickstart: React and TypeScript Todo Frontend

Validation guide for [plan.md](./plan.md). Client behavior is [contracts/http-client.md](./contracts/http-client.md) and [contracts/ui-behavior.md](./contracts/ui-behavior.md). Ports and proxy rules are [contracts/runtime.md](./contracts/runtime.md). Commands and jobs are [contracts/checks.md](./contracts/checks.md). Stored shapes are [data-model.md](./data-model.md).

This guide does not contain component source. It is the pass/fail check after implementation.

## Prerequisites

- Node.js 22 and npm
- Python 3.12 with the backend dev extra, for the API and pytest
- Docker Compose v2, for the container path
- Free host ports `127.0.0.1:5173`, `127.0.0.1:8000`, and, for Compose, `127.0.0.1:8080` and `127.0.0.1:9090`

## Backend checks

From `backend/`:

```bash
ruff check .
ruff format --check .
mypy src
python -m pytest --cov=todo_api --cov-report=term-missing --cov-fail-under=90
```

Expected: all four pass. The coverage floor is still 90. Existing user, todo, and metrics tests still pass.

## Frontend checks without a live API

From `frontend/`:

```bash
npm ci
npx tsc --noEmit
npx eslint .
npx vitest run
npm audit --audit-level=high
```

Expected:

- Typecheck and ESLint exit 0.
- Vitest exits 0 and covers rendering, client calls, interactions, a `401`, and HTTP errors.
- Separate Vitest cases show five different sentences for a 10-second client abort, HTTP 502, HTTP 504, another HTTP 5xx, and a browser network failure. None of those sentences contains a response body or a bearer token.
- A Vitest case completes account B's list while account A's list is still pending, then delivers A's list. The screen does not show A's todos. No test prints a bearer token.
- `npm audit --audit-level=high` exits 0 when no high or critical advisory applies. Moderate and low advisories may be printed and still exit 0.

## Playwright

From `frontend/`:

```bash
npx playwright test
```

Expected:

- The run starts a new API and a new Vite. It does not attach to a process that was already running.
- The new API listens on `127.0.0.1:8001` and Vite on `127.0.0.1:5174`. Neither `5173` nor `8000` is used.
- `DATABASE_URL` is an absolute path to a SQLite file created for this run. `backend/todo.db` and any other existing development database are not read or written.
- The scenario creates an account and runs create, edit, complete, reopen, delete, and filter.
- One step uses a bad token and sees the unidentified message with no previous todos left on screen.
- One step receives an HTTP error and sees a plain message. The token is not in that message.
- A title containing `<script>` is visible as text.
- When the command exits, including after a failed test, the temporary directory is gone and only the processes this run started have been stopped.

Playwright does not need Compose and does not add a backend error route.

To see the port guard, start a process that listens on `127.0.0.1:8001`, then run `npx playwright test` again. Expected: the command exits non-zero, the output names port `8001`, and the process that was already listening is still running. Stop that extra process yourself. Repeat the idea for `5174` if you want to see the Vite guard. Do not leave those listeners running.

## Local development path

Terminal A, from `backend/`:

```bash
uvicorn todo_api.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal B, from `frontend/`:

```bash
npm run dev
```

Expected:

- The page is `http://127.0.0.1:5173`.
- The browser's todo and account requests go to `http://127.0.0.1:5173/api/v1/...`.
- Vite forwards those to `http://127.0.0.1:8000`. The page origin is not `8000`.
- Create an account, copy the token from the one-time display, add a todo with only a title, and see it as incomplete with priority medium.
- Reload and the same list is there.
- Logout. The list is gone. Paste the same token. The list returns. The API has no revoke call in this path.
- Stop Uvicorn. The next action says the service could not be reached, and a list that was already showing stays visible. That sentence is the browser network failure, not the 10-second timeout sentence.
- Start Uvicorn again. A new list load works without restarting Vite.

A busy `5173` makes `npm run dev` exit with an error. It does not switch ports.

## Container path

From the repository root:

```bash
docker compose up -d --build
```

Expected:

- `http://127.0.0.1:8080` serves the page.
- `http://127.0.0.1:8000` still serves the API.
- `http://127.0.0.1:9090` still serves Prometheus.
- All three publishes are on `127.0.0.1` only.
- Account create and one todo succeed through `http://127.0.0.1:8080/api/v1/...`.
- Prometheus still scrapes `todo-api:8000` `/metrics`. The frontend is not a target.
- `docker compose ps` shows `frontend`, `todo-api`, and `prometheus` only.

Repeat the account-and-todo flow. It fits in 15 minutes when the images are already built. The first build may take longer. The spec's 15-minute check assumes prerequisites and images are ready.

Stopping or recreating `todo-api` can drop SQLite rows stored only in that container. That limitation is unchanged. Prometheus samples stay on `prometheus-data`.

To see the Compose port guard, start a process that listens on `127.0.0.1:8080`, then run `docker compose up -d --build` again. Expected: startup fails and the output shows that port `8080` is already in use. The process that was already listening is still running. Stop that extra process yourself. This check is manual. It is not a CI job, and the workflow must not bind port `8080` to prove it.

## Handbook

After the implementation exists, `tutorials/frontend-operations-handbook/` is present and uses the real files. Planning does not create it.

One exercise, chosen from that handbook, is run on the local machine. Expected: the write-up has symptoms, investigation, root cause, remediation, validation, and rollback, and the rollback returns the stack to the state from the start of the exercise. The exercise does not add an error route to FastAPI.

## Failures that mean the feature is not done

- The page calls `127.0.0.1:8000` directly from the browser.
- The API gained a CORS middleware or a new route.
- Logout calls a revoke endpoint.
- A second account's todos stay on screen after paste, create-account, logout, or `401`.
- Playwright uses `backend/todo.db`, attaches to an API it did not start, or stops a process it did not start.
- A late list for the previous account repaints that account's todos after the new account's list has loaded.
- A client timeout, HTTP 502, HTTP 504, another HTTP 5xx, and a network failure share one sentence, or any of those sentences includes a response body or a token.
- A backend CI job or the 90 percent coverage floor is removed.
