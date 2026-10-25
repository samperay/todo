# Contract: Checks and CI

Backend jobs stay. Frontend jobs are added beside them. Triggers stay `pull_request` and `push` to `main`.

## Backend jobs, unchanged

File: `.github/workflows/ci.yml`. Working directory `backend/`.

| Job | Command | Gate |
|-----|---------|------|
| Ruff Lint | `ruff check .` | Existing |
| Ruff Format | `ruff format --check .` | Existing |
| Pytest | `python -m pytest --cov=todo_api --cov-report=term-missing --cov-report=xml:coverage.xml --cov-fail-under=90` | Coverage floor stays 90 |
| Mypy | `mypy src` | Existing |

A new pytest module may read `compose.yaml` and `deploy/prometheus/prometheus.yml` and assert the frontend publish, the unchanged API and Prometheus publishes, and the unchanged scrape target. It must not start Docker and must not lower coverage of `todo_api`.

## Frontend jobs, new

Working directory `frontend/`. Node.js 22. `npm ci` from `package-lock.json`.

| Job | Command | Live API |
|-----|---------|----------|
| `frontend-static` | `npx tsc --noEmit` and ESLint | No |
| `frontend-unit` | Vitest once, not watch mode | No. Communication tests use a substitute for Fetch. |
| `frontend-e2e` | Playwright Chromium | Yes. A new temp SQLite file and a new API on `127.0.0.1:8001`. Python 3.12 installs the existing backend. `reuseExistingServer` is false. See [runtime.md](./runtime.md). |
| `frontend-audit` | `npm audit --audit-level=high` | No |

`frontend-e2e` installs Chromium only. It deletes the temp database at the end. It does not set `DATABASE_URL` to `backend/todo.db`.

Vitest and React Testing Library cover rendering, the client, user interactions, authentication failure, and HTTP errors. They also cover five transport results with a Fetch substitute: the 10-second client abort, HTTP 502, HTTP 504, another HTTP 5xx, and a browser network failure. Each test asserts a different fixed sentence and asserts that the response body and the bearer token are absent. One test starts a list for account A, switches to account B, completes B's list, then releases A's response. The screen still shows only B's todos.

Playwright covers create account, create, edit, complete, reopen, delete, filter, one authentication failure, and one HTTP error. It does not reuse a running backend. If `8001` or `5174` is occupied, the command fails and names the port. After the run, the temporary database is gone and the contributor's processes are still running.

## Local commands

From `frontend/`:

```bash
npm ci
npx tsc --noEmit
npx eslint .
npx vitest run
npm audit --audit-level=high
npx playwright test
```

`npx playwright test` starts the disposable API and Vite itself. It does not need Compose.

From `backend/`, the existing pytest command still passes at the 90 percent floor.

## Not in these checks

- No new backend fault route.
- No change to the pytest coverage floor.
- No PostgreSQL, Redis, Kubernetes, or API gateway.
- The operations handbook is not a CI job. It is reviewed by following one exercise after implementation.
