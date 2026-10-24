# Implementation Plan: React and TypeScript Todo Frontend

**Branch**: `feature/frontend-react-typescript` | **Date**: 2026-10-22 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-react-todo-frontend/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Add an independent React and TypeScript page under `frontend/` for the existing Todo API. The person creates an account, keeps the one-time bearer token in `localStorage`, and creates, lists, edits, completes, reopens, deletes, and filters only that account's todos. The browser calls relative `/api/v1` paths. Vite or Nginx forwards them to the existing FastAPI process. The API, its bearer-token rules, its SQLite file, and Prometheus stay as they are.

The learning target is request path, failure modes, containers, and checks. The UI is one plain page. Decisions are in [research.md](./research.md).

## Technical Context

**Language/Version**: TypeScript on Node.js 22 for the frontend. The existing API stays Python 3.12+ (FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite). No backend language change.

**Primary Dependencies**: React, React DOM, Vite, the native Fetch API, Vitest, React Testing Library, Playwright (Chromium only), TypeScript, ESLint, Nginx. npm is the package manager. No Redux, Next.js, router, component library, or third-party HTTP client. No third-party scripts in the page.

**Storage**: Browser `localStorage` keys `todo.accountId` and `todo.token` only. Todos stay in the existing SQLite database through the existing repository. Playwright creates a new temp SQLite file for each run and does not attach to an existing API process. The API container still has no database volume. Prometheus still uses `prometheus-data`.

**Testing**: `tsc --noEmit`, ESLint, Vitest, React Testing Library, Playwright, and `npm audit --audit-level=high`. Vitest covers the five transport failures and the late response from a previous account. Existing backend Ruff, format, mypy, and pytest jobs stay, including `--cov-fail-under=90`. A compose pytest may read the committed YAML and must not start Docker.

**Target Platform**: A developer machine. Local page at `http://127.0.0.1:5173`. Container page at `http://127.0.0.1:8080`. API remains `http://127.0.0.1:8000`. Prometheus remains `http://127.0.0.1:9090`.

**Project Type**: Browser UI in front of the existing web service. One page. The frontend builds without the Python package.

**Performance Goals**: A person can create an account and see a title-only todo in under 2 minutes (SC-001). A contributor with prerequisites installed finishes the local flow and the container flow within 15 minutes each (SC-009). A list of 50 todos filters correctly (SC-004). Client requests abort at 10 seconds. That abort is reported separately from HTTP 502, HTTP 504, other HTTP 5xx, and a browser network failure.

**Constraints**: Do not add CORS, routes, fields, fault-injection endpoints, PostgreSQL, Redis, Kubernetes, an API gateway, or a new identity system. Do not log tokens or put them in URLs. Failure text does not include response bodies or tokens. Logout does not revoke the server credential. A response from an older account session is discarded, including when it arrives after the new session's request completes. One page allows one editor per todo id. Cross-client edits are outside the frontend guarantee. Published ports bind to `127.0.0.1`. Playwright fails if `8001` or `5174` is taken and does not kill a process it did not start. Persistent token storage is an accepted local-learning limitation, not production authentication.

**Scale/Scope**: One frontend service, the existing `todo-api` service, and the existing `prometheus` service. Seven existing HTTP operations. One screen. Four new CI jobs beside the four backend jobs.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution at `.specify/memory/constitution.md` (3.1.0) governs the backend. This feature does not amend it.

| Gate | Requirement | Pre-research | Post-design |
|------|-------------|--------------|-------------|
| I. Layered architecture | API, service, and repository stay separate. Handlers delegate. Database access stays in the repository. | Pass | Pass. No route, service, or repository edit. The page talks to the existing HTTP boundary. Frontend modules separate the page, the Fetch client, and token storage. |
| II. Typed contracts | Pydantic v2 for JSON bodies. Protocol-specific responses may use their external form. | Pass | Pass. No new JSON endpoint. The client copies the existing user and todo fields into TypeScript interfaces. `GET /metrics` stays Prometheus text. |
| III. Tested features | pytest for backend behavior. Default tests use SQLite. A feature is unfinished without tests. | Pass | Pass. Backend pytest and the 90 percent floor stay. Frontend behavior is covered by Vitest and Playwright, which the spec requires and which do not replace pytest. Playwright's API uses a temp SQLite URL, the same idea as `backend/tests/conftest.py`. |
| IV. RESTful HTTP boundary | Noun resources, matching methods, one error policy. | Pass | Pass. The client uses the existing paths, methods, `401`/`404` error object, and `422` validation body. It does not add a route. |
| V. Secure configuration | Environment-backed settings. No committed secrets. Local defaults are non-secrets. | Pass | Pass. `API_PROXY_TARGET` and `API_UPSTREAM` are non-secret URLs. They are not `VITE_` variables and are not baked into the browser bundle as a token. No credential is committed. The token-storage limitation is documented and is not a hardcoded secret. |
| VI. Portable persistence | SQLAlchemy only. SQLite for local and default tests. Engine details stay behind the repository. | Pass | Pass. No engine change and no API volume. Playwright sets `DATABASE_URL` to a temp SQLite file and deletes it. |
| Stack | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite, pytest. | Pass | Pass. React, Vite, Nginx, and Node are the frontend runtime the spec adds. They do not replace the backend stack. |
| Workflow | New backend behavior ships with pytest. Shared exception handlers stay the error policy. | Pass | Pass. No new domain error and no handler edit. |

No gate fails. Complexity tracking is empty.

## Project Structure

### Documentation (this feature)

```text
specs/004-react-todo-frontend/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
frontend/
├── README.md                 # local dev, build, test, Docker, token limitation
├── ARCHITECTURE.md           # module map and browser-to-SQLite path
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts            # 127.0.0.1:5173, strictPort, proxy /api
├── eslint.config.js
├── playwright.config.ts      # reuseExistingServer false; 5174; new API on 8001
├── Dockerfile                # node:22-alpine build, nginx:1.28-alpine runtime
├── nginx.conf.template       # static files + /api/v1/ proxy; API_UPSTREAM substituted at start
├── docker-entrypoint.sh      # require API_UPSTREAM, envsubst, nginx -t
├── scripts/
│   └── playwright-servers.sh # Python 3 starts and stops the disposable API and Vite
├── .dockerignore
├── src/
│   ├── main.tsx              # startup
│   ├── App.tsx               # page composition
│   ├── styles.css
│   ├── config.ts             # relative /api/v1 base path only
│   ├── api/
│   │   ├── types.ts          # existing response and request fields
│   │   ├── client.ts         # Fetch, timeout, status mapping
│   │   ├── users.ts
│   │   └── todos.ts
│   ├── auth/
│   │   └── tokenStore.ts     # localStorage, no logging
│   ├── session/
│   │   └── useTodoSession.ts # list, filter, editor lock, account switch
│   └── components/
│       ├── AccountPanel.tsx
│       ├── TodoForm.tsx
│       ├── TodoList.tsx
│       ├── TodoItem.tsx
│       ├── TodoEditor.tsx
│       ├── FilterBar.tsx
│       └── Notice.tsx
├── tests/                    # Vitest and Testing Library
└── e2e/                      # Playwright

compose.yaml                  # add frontend; leave todo-api and prometheus
.github/workflows/ci.yml      # four existing jobs plus four frontend jobs
backend/tests/compose/        # optional YAML assertions, no Docker
README.md                     # short pointer to frontend/README.md

tutorials/frontend-operations-handbook/   # AFTER implementation, not in this phase
```

Existing backend modules stay as they are. Entry point remains `backend/src/todo_api/main.py`. Auth remains `HTTPBearer` plus the token hash in `backend/src/todo_api/api/deps.py`. Settings remain `database_url` in `backend/src/todo_api/core/config.py`.

**Structure Decision**: The frontend is a separate tree so `npm` and the Python package do not share an install. Screen components do not call `fetch`. The session hook is the only place that clears todos when the credential changes. Contracts live in `frontend/src/api/types.ts` and match the existing Pydantic models. The handbook waits until those files exist, so its exercises can name real paths.

## Architecture decisions

| Topic | Choice | Trade-off |
|-------|--------|-----------|
| UI toolkit | React | Required. One page, so no router. |
| Types | TypeScript strict interfaces | Client and server can still drift. The contract test fixes the fields we send and read. |
| Build | Vite | Fast local reload. Not a second application server. |
| HTTP | Native Fetch, 10-second abort | No client library. Timeout, 502, 504, other 5xx, and network failure stay distinct and body-free. |
| Origin | Vite and Nginx reverse proxy | No CORS change. A wrong upstream is an operator fault, which is the point of the handbook. |
| Token | `localStorage` | Reload works. Any script on this origin can read the token. Not production-ready. Logout is local only. |
| Static host | Nginx | Matches the spec. Proxy path mistakes are a documented failure mode. |
| Deploy | Existing Compose file, new `frontend` service | One stack. API SQLite still dies with the API container. |
| Tests | Vitest without a live API; Playwright starts a new API on a new SQLite file | E2E does not reuse a running backend or `backend/todo.db`. A busy `8001` or `5174` fails the run. Cleanup signals only sessions this run created, on macOS and Linux. |

Detail and rejected options are in [research.md](./research.md).

## Request path

```text
Browser
  -> React component
  -> useTodoSession
  -> api/todos.ts or api/users.ts
  -> api/client.ts Fetch
  -> relative /api/v1
  -> Vite (dev) or Nginx (container)
  -> FastAPI route
  -> service
  -> repository
  -> SQLite
```

Account create stores `id` and `token`, increments the session generation, aborts the previous generation's requests, clears any previous rows, then lists. Todo calls send `Authorization: Bearer`. A response is applied only when its generation is still current, so a slow list from the previous account cannot repaint those rows after logout or after the new account's list has completed. `401` clears the list. A client timeout, HTTP 502, HTTP 504, any other HTTP 5xx, and a browser network failure each keep the current account's last successful list and show a different fixed sentence, with no response body and no token. Loading is shown for every in-flight action. The same action is not submitted twice. Filter is local.

## Documentation

Ship with the implementation:

- `frontend/README.md` — prerequisites, `127.0.0.1:5173`, proxy, build, test, Compose, token limitation, logout does not revoke.
- `frontend/ARCHITECTURE.md` — the path above and the module split.
- A short section in the root `README.md` that points at `frontend/README.md`.

After that code is in the tree, write `tutorials/frontend-operations-handbook/` from the real Vite config, `frontend/nginx.conf.template`, `frontend/docker-entrypoint.sh`, Compose service, and CI jobs. Required topics: frontend architecture, React and TypeScript overview, browser-to-FastAPI lifecycle, browser developer tools, authentication, CORS, Nginx reverse proxy, Docker networking, CI/CD, API latency and availability. Each exercise records symptoms, investigation, root cause, remediation, validation, and rollback, and uses a safe local or simulated failure. Do not add a backend fault route. This plan does not create the handbook.

## Constitution Check (post-design)

Re-checked against the contracts and data model. Results are in the table above. No gate fails.

## Complexity Tracking

No constitution violations.

## Resolved before task generation

These were open in the spec's planning notes. They are decided in [research.md](./research.md). None of them block `/speckit-tasks`.

| Question | Decision |
|----------|----------|
| Vulnerability tool | `npm audit --audit-level=high`. Moderate and low print and do not fail. |
| Playwright launch | New temp SQLite file. `frontend/scripts/playwright-servers.sh` delegates to Python 3: `subprocess.Popen(..., start_new_session=True)` and `os.killpg`. New Uvicorn and Vite processes on `127.0.0.1:8001` and `127.0.0.1:5174`. No `setsid` executable. `reuseExistingServer` is false. A busy port fails visibly and the occupant is left running. Cleanup runs once and signals only sessions this run created. Chromium only. |
| Same browser session | One page. Another tab is another client and is outside the edit lock. |
| Stale account response | Session generation plus abort. A late response from the previous generation is dropped after the new generation's request has completed. Vitest covers that order. |
| `401` versus "keep the last list" | `401`, logout, and credential replacement clear the list. `404`, `422`, client timeout, 502, 504, other 5xx, and network failure keep the current account's list. |
| Transport failures | Five fixed sentences: client timeout at 10 seconds, HTTP 502, HTTP 504, other HTTP 5xx, and browser network failure. No body and no token. |
| Handbook files | Named after implementation. This phase does not add `tutorials/frontend-operations-handbook/`. |
| Image tags | `node:22-alpine` and `nginx:1.28-alpine`, confirmed to exist at implementation time. Not `latest`. |

No architectural conflict with the constitution or the existing API contract remains.
