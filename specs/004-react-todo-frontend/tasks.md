# Tasks: React and TypeScript Todo Frontend

**Input**: Design documents from `/specs/004-react-todo-frontend/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included. The spec requires TypeScript checks, ESLint, Vitest, React Testing Library, Playwright, and the existing backend pytest gate. Write each story's tests first and confirm they fail before the implementation that makes them pass. Do not add a backend route, CORS middleware, fault-injection endpoint, or a change to bearer-token authentication.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/`, `frontend/tests/`, `frontend/e2e/`, `frontend/scripts/`
- **Runtime**: `compose.yaml`, `frontend/Dockerfile`, `frontend/nginx.conf.template`, `frontend/docker-entrypoint.sh`, `frontend/scripts/playwright-servers.sh`
- **Checks**: `.github/workflows/ci.yml`, `backend/tests/compose/test_frontend_compose.py`
- **Backend application, unchanged**: `backend/src/todo_api/`
- Paths match `specs/004-react-todo-frontend/plan.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the independent frontend toolchain. No todo behavior yet.

- [X] T001 Create `frontend/index.html`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, and directories `frontend/src/api/`, `frontend/src/auth/`, `frontend/src/session/`, `frontend/src/components/`, `frontend/tests/`, `frontend/e2e/`, and `frontend/scripts/`. `frontend/index.html` loads only `/src/main.tsx` and contains no third-party script. Add `frontend/.dockerignore` excluding `node_modules`, `dist`, `test-results`, `playwright-report`, and `.env`.
- [X] T002 [P] Add `frontend/package.json` and `frontend/package-lock.json` with React, React DOM, TypeScript, Vite, `@vitejs/plugin-react`, Vitest, jsdom, React Testing Library, `@testing-library/user-event`, `@testing-library/jest-dom`, `@playwright/test`, ESLint, `typescript-eslint`, and `eslint-plugin-react-hooks`. Scripts: `dev`, `build`, `typecheck` (`tsc --noEmit`), `lint`, `test` (`vitest run`), `e2e` (`playwright test`). Do not add Redux, Zustand, React Router, Next.js, Axios, or a component library.
- [X] T003 [P] Add `frontend/tsconfig.json` with strict TypeScript for `frontend/src/` and `frontend/tests/`. Do not allow implicit any on exported API types.
- [X] T004 [P] Add `frontend/eslint.config.js` for TypeScript and React hooks, covering `frontend/src/` and `frontend/tests/`.
- [X] T005 [P] Add `frontend/vite.config.ts` with `server.host` `127.0.0.1`, `server.port` `5173`, `server.strictPort` true, and a proxy of `/api` to `process.env.API_PROXY_TARGET` or `http://127.0.0.1:8000`. Do not read that target from a `VITE_` variable. Include the Vitest jsdom config in this file.
- [X] T006 [P] Add `frontend/src/config.ts` exporting only the relative base path `/api/v1`.
- [X] T007 [P] Add `frontend/src/styles.css` and import it from `frontend/src/main.tsx`. Plain CSS only.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared types and the empty page shell. Story behavior is not implemented here.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 [P] Add `frontend/src/api/types.ts` with `UserCreated` (`id`, `token`), `Todo` (`id`, `title`, `description` as `string | null`, `completed`, `priority`, `created_at`, `updated_at`), `Priority` limited to `low` | `medium` | `high`, `TodoCreate`, and `TodoUpdate`. Do not add an owner field. Title is required after trim and at most 200 characters. Description, when present, is at most 2000 characters.
- [X] T009 [P] Add `frontend/src/api/client.ts` exporting a `request` function that calls a relative `/api/v1` path, sends `Content-Type: application/json` only when a body is present, sends `Authorization: Bearer <token>` only when a token argument is present, aborts after 10 seconds, and accepts a numeric `sessionGeneration`. Do not log the token or the Authorization header. Story phases fill the status mapping.
- [X] T010 Add `frontend/src/session/useTodoSession.ts` with `sessionGeneration` starting at 0, `todos` empty, `filter` `all`, and `listStatus` `idle`. Export the hook and render its empty state from `frontend/src/App.tsx`. Do not fetch yet.

**Checkpoint**: `npm run typecheck` in `frontend/` succeeds. The page mounts with no account and no todos. User stories can begin.

---

## Phase 3: User Story 1 - Create an account and stay identified (Priority: P1) 🎯 MVP

**Execution warning**: T018 must execute after T015 and before T016, regardless of numeric task ordering. Do not create a duplicate implementation of `GET /api/v1/todos`.

**Goal**: A person creates an account with no name, email, or password, sees the bearer token once, stays identified after reload, logs out locally, and can paste the same token again.

**Independent Test**: Create an account, receive the bearer token, and store it. The session requests that account's todos and does not render the list markup. Reload restores the session without showing the token again and requests the same account's todos. Logout clears the local session and the stored todos and does not call a revoke route. Pasting the saved token requests that same account's todos. Replacing the token clears the previous account's stored todos before the new list returns. An unknown token says the person must be identified. The token is absent from the URL and from logs. A list response from the previous session does not change stored state after the new session's request has completed. A second account creation is not sent while the first is in flight. With no stored token, the screen says the service cannot replace a lost token.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Add failing tests in `frontend/tests/auth/tokenStore.test.ts`. Keys are `todo.accountId` and `todo.token`. Logout removes both keys and does not call the network. `console` output and thrown errors do not contain the token value.
- [X] T012 [P] [US1] Add a failing lifecycle test in `frontend/tests/components/AccountPanel.test.tsx`. Cover account creation, token persistence, session restoration, logout, token replacement, API request isolation, and session-state clearing. Run in this order: create the account with `POST /api/v1/users` and no body and no `Authorization` header; while that request is in flight, a second create sends no further `POST /api/v1/users`; receive `201` `{id, token}` and show that token once; store `todo.accountId` and `todo.token`; the session calls `listTodos` with `Authorization: Bearer` of that token; reload the application; restore the session from `localStorage` without showing the token again; the session calls `listTodos` again for that same token; logout; clear the local keys and the stored todos without a revoke request; paste the saved token; the session calls `listTodos` again for that same token. A further case pastes a different account's token and asserts the previous account's stored todo records are cleared before the new list returns, and that the new request carries only the new token. A `401` says the person must be identified and clears the stored todos. With no stored token, the screen says `The service cannot replace a lost token.` The address has no token in the path, query, or fragment. Do not require `TodoList`, `TodoItem`, rendered todo titles, or the final loading and empty-state markup.
- [X] T013 [P] [US1] Add a failing test in `frontend/tests/session/accountSwitch.test.tsx`. Start a list for account A and leave it pending. Switch to account B and let B's list complete with B's records in session state. Then resolve A's list. The stored todos are only B's records. A second case resolves A's list after logout and the stored todos stay empty. Assert the stale response is discarded and does not change the session. Do not require `TodoList`, `TodoItem`, or rendered titles.

### Implementation for User Story 1

- [X] T014 [US1] Implement `frontend/src/auth/tokenStore.ts` for the `todo.accountId` and `todo.token` keys. Logout removes those keys only. Do not add a revoke call. Do not write the token to `console`.
- [X] T015 [US1] Implement `frontend/src/api/users.ts` `POST /api/v1/users` with no body, reading `201` `{id, token}` through `frontend/src/api/client.ts`.
- [X] T018 [US2] Add `listTodos` in `frontend/src/api/todos.ts`. It calls `GET /api/v1/todos` through `frontend/src/api/client.ts`, requires `Authorization: Bearer`, and accepts a JSON array. Do not send a filter, search, or paging parameter. This is the only list request. Do it after T015 and before T016.
- [X] T016 [US1] Implement `frontend/src/components/AccountPanel.tsx` and the create, paste, logout, and one-time reveal paths in `frontend/src/session/useTodoSession.ts`. While the create-account request is in flight, do not send a second `POST /api/v1/users`. When no token is stored, show `The service cannot replace a lost token.` Do not add password recovery, email recovery, token regeneration, or a backend authentication change. After create, reload, and paste, load todos by calling `listTodos` from `frontend/src/api/todos.ts`. Do not call `request` for `GET /api/v1/todos` from the session or the panel. Increment `sessionGeneration`, abort the previous generation's requests, and clear the stored `todos` before that next list, including when the pasted token is a different account. Apply a response only when its generation is still current, including when the old response arrives after the new request completes. Render the panel from `frontend/src/App.tsx`. Do not render `TodoList` or `TodoItem` here.

**Checkpoint**: User Story 1 works against a mocked Fetch. Logout does not revoke the backend credential. The stale-response test passes.

---

## Phase 4: User Story 2 - See my todos (Priority: P1)

**Goal**: An identified person sees every todo they own, newest first in the order the service returned, with loading and empty states.

**Independent Test**: A known list renders once each, in returned order, with title, description when present, completed, priority, created time, and updated time. An empty `200` array is an empty state, not an error. A delayed list shows loading before items or the empty state. Markup in a title is visible as text and does not run.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T017 [US2] Add failing tests in `frontend/tests/components/TodoList.test.tsx`. Assert returned order is kept and not re-sorted. Assert fields `id`, `title`, `description`, `completed`, `priority`, `created_at`, and `updated_at` are visible. Assert an empty array is the empty-account state. Assert loading is shown while the request is pending. Assert a title `<script>alert(1)</script>` is text in the document and no script runs. Assert that when the stored rows change from account A to account B, the document shows B's titles and does not show A's titles. This is the visual check that switching accounts does not expose stale account data.

### Implementation for User Story 2

`listTodos` already exists from T018, which runs before T016. Do not add a second `GET /api/v1/todos`.

- [X] T019 [US2] Implement `frontend/src/components/TodoList.tsx` and `frontend/src/components/TodoItem.tsx` so title and description render as React text. Show description only when it is not null.
- [X] T020 [US2] Render the todos `frontend/src/session/useTodoSession.ts` already loaded through `listTodos`. Do not add another list request. Keep the array order from `GET /api/v1/todos`. Set `listStatus` to `loading` while that request is pending, then `ready` or `error`. Mount the list from `frontend/src/App.tsx`.

**Checkpoint**: User Story 2 shows only the todos returned for the current token. The empty and loading states are distinct.

---

## Phase 5: User Story 3 - Add a todo (Priority: P1)

**Goal**: An identified person adds a todo with a title, an optional description, and an optional priority. A new todo starts incomplete. Omitted priority is medium.

**Independent Test**: A title-only todo appears as incomplete, priority medium, with no description, without a manual reload. A blank or whitespace title, a title longer than 200 characters, and a description longer than 2000 characters add nothing and name the failed rule. Surrounding whitespace is not what the screen shows after save. Two todos may share a title. A second submit is not sent while the first create is in flight.

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T021 [US3] Add failing tests in `frontend/tests/components/TodoForm.test.tsx`. Title is required after trim and at most 200 characters. Description is at most 2000 characters, and a whitespace-only description is `null`. Priority is `low`, `medium`, or `high`; omitted priority is medium. Duplicate titles remain separate items. A second click while the request is pending does not send a second `POST`.

### Implementation for User Story 3

- [ ] T022 [US3] Add `POST /api/v1/todos` in `frontend/src/api/todos.ts`. Send `title`, plus `description` or `priority` only when the person set them. Do not send `completed` or `id`.
- [ ] T023 [US3] Implement `frontend/src/components/TodoForm.tsx` with a priority control of unset, `low`, `medium`, and `high` only.
- [ ] T024 [US3] On `201`, refresh the list by calling `listTodos` from `frontend/src/api/todos.ts` inside `frontend/src/session/useTodoSession.ts` so the screen uses service order. Do not add another list request. Block a duplicate submit while that create is in flight. Keep the selected filter. Mount the form from `frontend/src/App.tsx`.

**Checkpoint**: A title-only create shows an incomplete medium todo. Rejected values leave the list unchanged.

---

## Phase 6: User Story 4 - Complete a todo and make it pending again (Priority: P1)

**Goal**: An identified person marks a todo completed and later marks it pending. Repeating the action that already applies is not an error.

**Independent Test**: Complete an incomplete todo and see it completed with the same title, description, priority, id, and created time. Complete it again and no field changes and no error shows. Mark it pending and it shows incomplete with those same fields. An unknown id says the todo was not found and does not reveal another owner.

### Tests for User Story 4 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T025 [US4] Add failing tests in `frontend/tests/components/TodoItem.complete.test.tsx`. Complete calls `POST /api/v1/todos/{id}/complete` with no body. Pending calls `POST /api/v1/todos/{id}/incomplete` with no body. Marking an already completed todo completed again, or an already pending todo pending again, is not shown as a failure and leaves every field unchanged. A `404` body `{error:{code:"not_found", message:"Todo not found"}}` does not mention another owner. A second click of the same action is not sent while the first request is in flight.

### Implementation for User Story 4

- [ ] T026 [US4] Add complete and incomplete calls in `frontend/src/api/todos.ts`. Both are `POST` with no body and expect `200` and a todo.
- [ ] T027 [US4] Add complete and pending controls on `frontend/src/components/TodoItem.tsx`.
- [ ] T028 [US4] Handle both actions in `frontend/src/session/useTodoSession.ts`, then refresh the list by calling `listTodos` from `frontend/src/api/todos.ts`. Do not add another list request. Do not send `completed` on `PATCH`. An already-complete or already-pending `200` leaves every field as the service returned it.

**Checkpoint**: Complete and pending work on the current account's rows. The list is not reordered by the client.

---

## Phase 7: User Story 8 - Understand loading and failures (Priority: P1)

**Goal**: The person can tell a client timeout, HTTP 502, HTTP 504, another HTTP 5xx, a browser network failure, a rejected value, a missing todo, and a missing credential apart. Messages do not include bodies or tokens.

**Independent Test**: Force each of those results. Each shows its own fixed sentence. A later failure after a successful list keeps that list, except `401`, which clears it. The first failed load does not look like an empty account. A session-change abort does not show the timeout sentence.

### Tests for User Story 8 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T029 [P] [US8] Add failing tests in `frontend/tests/api/client.test.ts` for five results. The 10-second abort says `The request timed out.` HTTP 502 says `The proxy could not get a valid response from the service.` HTTP 504 says `The proxy timed out waiting for the service.` HTTP 500 says `The action could not be completed.` A Fetch rejection that is not an abort says `The service could not be reached.` None of the five strings includes the response body or the bearer token. A further case aborts the request because `sessionGeneration` changed and asserts that cancellation does not show `The request timed out.`
- [ ] T030 [P] [US8] Add failing tests in `frontend/tests/components/Notice.test.tsx` for `401` `You must be identified.`, a `422` rule sentence, and `404` `Todo not found`. A `422` whose `detail[].msg` contains `Title is required`, `Title must be at most 200 characters`, `Description must be at most 2000 characters`, `Priority is invalid`, or `At least one of title, description, or priority is required` shows that rule and not the raw `detail` array. Add a failing test in `frontend/tests/session/firstLoad.test.tsx`: the first `GET /api/v1/todos` fails before any successful list exists, loading ends, the error is shown, and the empty-account state is not shown. Write both tests before T031 and T033.

### Implementation for User Story 8

- [ ] T031 [US8] Map those statuses and aborts in `frontend/src/api/client.ts`. A session-generation abort is discarded and is not the timeout notice. Do not display response bodies for 502, 504, or other 5xx.
- [ ] T032 [US8] Implement `frontend/src/components/Notice.tsx` and render one notice from `frontend/src/App.tsx`.
- [ ] T033 [US8] In `frontend/src/session/useTodoSession.ts`, show loading while account creation, list, create, edit save, complete, reopen, or delete is in flight. Keep the current generation's list on timeout, 502, 504, other 5xx, network failure, 404, and 422. Clear the list on `401`. A failed first load uses the error screen, not the empty-account state.

**Checkpoint**: The five transport sentences differ. No notice contains a token. Stale account responses from User Story 1 still do not repaint.

---

## Phase 8: User Story 5 - Edit a todo (Priority: P2)

**Goal**: An identified person changes title, description, priority, or a combination. One page allows one editor for a given todo id.

**Independent Test**: Changing the title leaves description and priority. Clearing the description stores `null`. Saving with no change sends no request. A blank title is rejected and the todo stays. A second edit of the same id does not open while the first is open or saving. An edit of a different id may open. An unknown id says the todo was not found.

### Tests for User Story 5 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T034 [US5] Add failing tests in `frontend/tests/components/TodoEditor.test.tsx`. `PATCH /api/v1/todos/{id}` sends only changed `title`, `description`, or `priority`. Clearing description sends `description: null`. No changed field sends no request. `completed` and `id` are never in the body. A second edit of the same id does not open and does not send. A different id may open. Title is required after trim and at most 200 characters. Description is at most 2000 characters.

### Implementation for User Story 5

- [ ] T035 [US5] Add `PATCH /api/v1/todos/{id}` in `frontend/src/api/todos.ts` with only the changed fields and a `200` todo.
- [ ] T036 [US5] Implement `frontend/src/components/TodoEditor.tsx`.
- [ ] T037 [US5] Track `openTodoId` and `savingTodoId` in `frontend/src/session/useTodoSession.ts`. Block a second edit of that same id. Do not add a version field or `If-Match`. After a `200`, refresh the list by calling `listTodos` from `frontend/src/api/todos.ts`. Do not add another list request. Another browser tab is outside this lock.

**Checkpoint**: Edits match the service todo. The same-id editor lock holds in one page.

---

## Phase 9: User Story 6 - Delete a todo (Priority: P2)

**Goal**: An identified person permanently deletes one todo after confirming. Cancel leaves it.

**Independent Test**: Confirm removes the todo from a later list. Cancel leaves it. Other todos stay. An unknown id says the todo was not found. An unidentified person is told they must be identified and nothing changes.

### Tests for User Story 6 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T038 [US6] Add failing tests in `frontend/tests/components/TodoItem.delete.test.tsx`. Delete shows a confirmation. Cancel sends nothing. Confirm calls `DELETE /api/v1/todos/{id}` and treats `204` with no body as success. A `404` leaves the other rows. A second confirm is not sent while the delete is in flight.

### Implementation for User Story 6

- [ ] T039 [US6] Add `DELETE /api/v1/todos/{id}` in `frontend/src/api/todos.ts`. Do not parse a `204` body.
- [ ] T040 [US6] Add confirmation to `frontend/src/components/TodoItem.tsx` and the delete path in `frontend/src/session/useTodoSession.ts`. After `204`, refresh the list by calling `listTodos` from `frontend/src/api/todos.ts`. Do not add another list request. Do not restore a deleted id.

**Checkpoint**: Confirmed delete removes one row. Cancel does not.

---

## Phase 10: User Story 7 - Filter pending and completed todos (Priority: P2)

**Goal**: The person views all, pending, or completed todos from the list already loaded. Pending means `completed` is false.

**Independent Test**: The initial filter is all. Pending and completed show only matching rows in the same relative order. A filter with no rows is distinct from the empty account and from a failed load. Changing filter does not fetch. The selected filter remains after a successful add, edit, complete, reopen, or delete.

### Tests for User Story 7 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T041 [US7] Add failing tests in `frontend/tests/components/FilterBar.test.tsx`. Default is `all`. `pending` shows `completed === false`. `completed` shows `completed === true`. No `GET` is sent when the filter changes. Empty-filter copy differs from the empty-account copy. Relative order from the loaded array is kept.

### Implementation for User Story 7

- [ ] T042 [US7] Implement `frontend/src/components/FilterBar.tsx`.
- [ ] T043 [US7] Apply the filter in `frontend/src/session/useTodoSession.ts` over the array already stored. Do not add a query parameter. Keep the filter across successful mutations.

**Checkpoint**: All three views classify a mixed list correctly without another request.

---

## Phase 11: User Story 9 - Run the frontend locally and in the container stack (Priority: P2)

**Goal**: Local Vite on `127.0.0.1:5173` forwards `/api` to the existing API. Compose adds Nginx on `127.0.0.1:8080` without moving the API or Prometheus.

**Independent Test**: The dev page is `http://127.0.0.1:5173` and its `/api/v1` requests reach `http://127.0.0.1:8000`. Compose serves `http://127.0.0.1:8080`, leaves the API at `http://127.0.0.1:8000` and Prometheus at `http://127.0.0.1:9090`, and still scrapes `todo-api:8000/metrics`. A busy `5173` fails `npm run dev`. A busy `8080` is the manual check in `specs/004-react-todo-frontend/quickstart.md` and is not a CI test. The frontend image builds without the Python package. Services are `frontend`, `todo-api`, and `prometheus` only.

### Tests for User Story 9 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T044 [US9] Add failing tests in `backend/tests/compose/test_frontend_compose.py` that read `compose.yaml`, `deploy/prometheus/prometheus.yml`, `frontend/nginx.conf.template`, and `frontend/docker-entrypoint.sh` without starting Docker. Assert services are `frontend`, `todo-api`, and `prometheus` only. Assert publishes `127.0.0.1:8080:80`, `127.0.0.1:8000:8000`, and `127.0.0.1:9090:9090` with no `0.0.0.0` publish. Assert the Prometheus job still targets `todo-api:8000` path `/metrics`. Assert no new database volume is added for `todo-api`. Assert the template is rendered by `envsubst` of `API_UPSTREAM` only, then checked with `nginx -t`, and that `proxy_pass` has no extra URI path after the upstream. Tests fail while the frontend service or the template is absent.

### Implementation for User Story 9

- [ ] T045 [P] [US9] Add `frontend/Dockerfile` with build stage `node:22-alpine` and runtime `nginx:1.28-alpine` listening on container port 80. Add `frontend/nginx.conf.template` and `frontend/docker-entrypoint.sh`. Do not rely on Nginx to expand environment variables. The entrypoint must require `API_UPSTREAM`, run `envsubst '${API_UPSTREAM}'` so only that variable is replaced, write the generated config, run `nginx -t`, and exit non-zero with that output when the config is invalid or `API_UPSTREAM` is empty. `location /api/v1/` uses `proxy_pass` to the substituted upstream with no URI path after it, so `/api/v1/...` is forwarded unchanged. Do not proxy `/metrics`. Confirm the image tags exist for the host architecture before committing them. Do not use `latest`.
- [ ] T046 [P] [US9] Add service `frontend` to `compose.yaml` with build context `frontend/`, publish `127.0.0.1:8080:80`, and `API_UPSTREAM=http://todo-api:8000`. Leave the `todo-api` and `prometheus` services and `deploy/prometheus/prometheus.yml` otherwise unchanged. Do not add PostgreSQL, Redis, or a SQLite volume.
- [ ] T047 [US9] Write `frontend/README.md` and `frontend/ARCHITECTURE.md`, and add a short pointer in `README.md`. Document `127.0.0.1:5173`, `API_PROXY_TARGET`, `127.0.0.1:8080`, the browser-to-SQLite path, and that `frontend/docker-entrypoint.sh` substitutes `API_UPSTREAM` before Nginx starts. State that persistent `localStorage` is an accepted local-learning limitation and not production authentication, and that logout removes only the local token.

**Checkpoint**: `pytest backend/tests/compose/test_frontend_compose.py` passes. `docker compose up -d --build` serves the page on `127.0.0.1:8080` and does not move ports 8000 or 9090.

---

## Phase 12: User Story 10 - Check the frontend and troubleshoot it (Priority: P2)

**Goal**: Automated checks cover the frontend, Playwright uses a new disposable API, backend CI stays intact, and the operations handbook is written from the finished files.

**Independent Test**: `npx tsc --noEmit`, ESLint, `vitest run`, and `npm audit --audit-level=high` pass in `frontend/`. Playwright starts a new API on a new SQLite file at `127.0.0.1:8001` and Vite at `127.0.0.1:5174`, creates an account, and runs create, edit, complete, reopen, delete, and filter. It does not read `backend/todo.db`. A busy `8001` or `5174` fails and names the port without killing the occupant. Backend Ruff, format, mypy, and pytest `--cov-fail-under=90` still pass. After those files exist, `tutorials/frontend-operations-handbook/` contains the ten topics and one exercise with symptoms, investigation, root cause, remediation, validation, and rollback.

### Tests for User Story 10 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T048 [US10] Add a failing Playwright test in `frontend/e2e/todo-workflow.spec.ts` for account creation, create, edit, complete, reopen, delete, filter, one unknown token, and one HTTP error. Assert a title containing `<script>` is visible as text. Assert the unknown-token screen does not keep the previous account's todos. Do not point this test at `127.0.0.1:8000` or `backend/todo.db`.

### Implementation for User Story 10

- [ ] T049 [US10] Add `frontend/playwright.config.ts` with `reuseExistingServer: false` and Chromium only. Add `frontend/scripts/playwright-servers.sh`. The shell script delegates process creation and process-group termination to Python 3 on both macOS and Linux. Python creates a new temporary directory and a new SQLite file, and sets `DATABASE_URL` to that absolute path. Exit non-zero before starting anything if that path is `backend/todo.db`, the default `./todo.db`, or outside the new temporary directory. Start Uvicorn on `127.0.0.1:8001` and Vite on `127.0.0.1:5174` with `strictPort`. Python starts each server with `subprocess.Popen(..., start_new_session=True)`. The new session id equals the leader pid. Record only those ids. Children started by npm, Node, or Uvicorn stay in that session. If `8001` or `5174` is taken, print the port and exit non-zero without signalling the existing listener and without choosing another port. Install one cleanup function and a guard so its body runs once. Run it from traps on EXIT, INT, and TERM, including after a failed command. INT and TERM also trigger EXIT, and the guard skips that second run. Clear those traps at the start of cleanup. Cleanup calls Python `os.killpg` with SIGTERM for each recorded session, waits, then calls `os.killpg` with SIGKILL only for those same sessions if they are still alive, then deletes the temporary directory. Do not signal process group `0`, `-1`, or the runner's own group. Do not invoke the `setsid` executable, `kill`, GNU `kill -- -pgid`, `pkill`, `killall`, or a port scan. Do not signal a session this script did not create.
- [ ] T050 [US10] Add jobs `frontend-static`, `frontend-unit`, `frontend-e2e`, and `frontend-audit` to `.github/workflows/ci.yml` on the existing pull-request and main-branch triggers. Use Node.js 22 and `npm ci`. `frontend-static` runs `tsc --noEmit` and ESLint. `frontend-unit` runs `vitest run`. `frontend-e2e` installs Python 3.12, the backend package, and Chromium, then runs Playwright. `frontend-audit` runs `npm audit --audit-level=high` and must fail the workflow on a high or critical finding. Do not add `continue-on-error`, `|| true`, an audit allowlist, or an `.npmrc` setting that skips audit. Do not edit the Ruff, format, mypy, or pytest steps, and do not change `--cov-fail-under=90`. Moderate and low findings may print and must not fail this job.
- [ ] T051 [US10] After T045, T046, T047, T049, and T050 exist, write `tutorials/frontend-operations-handbook/` from those files. Cover frontend architecture, a React and TypeScript overview, the browser-to-FastAPI lifecycle, browser developer tools, authentication troubleshooting, CORS troubleshooting, the Nginx reverse proxy, Docker networking, CI/CD troubleshooting, and API latency and availability. Include the `envsubst` entrypoint and `nginx -t` failure from `frontend/docker-entrypoint.sh`, and the Playwright session cleanup from `frontend/scripts/playwright-servers.sh`, including that the shell script delegates to Python 3 `subprocess.Popen(..., start_new_session=True)` and `os.killpg` on both macOS and Linux and that cleanup runs once. Include safe local or simulated failure exercises. Each exercise has symptoms, investigation steps, root cause, remediation, validation, and rollback. Record the token-storage limitation, the XSS exposure, no token logging, no token in URLs, text rendering, no third-party scripts, and logout that does not revoke the backend credential. Add a dependency-vulnerability section that keeps `npm audit --audit-level=high` blocking and tells the reader how to inspect an advisory with `npm audit` and `npm audit --json`, tell a direct `frontend/package.json` dependency from a transitive path, apply a targeted update, regenerate `frontend/package-lock.json` with `npm install`, and re-run the audit. A temporary exception is a dated note naming the advisory, the reason, and the review date. That note must not be read by CI to skip a finding, and the handbook must not add an ignore flag or an allowlist. Do not add a backend fault route.

**Checkpoint**: Frontend checks and the unchanged backend checks pass. One handbook exercise can be followed and rolled back.

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Confirm the quickstart and the boundaries that apply to every story.

- [ ] T052 [P] Search `frontend/src/` and confirm no `dangerouslySetInnerHTML`, no `console` call that interpolates the token, and no `fetch` to `http://127.0.0.1:8000`. Titles and descriptions stay React text in `frontend/src/components/TodoItem.tsx` and `frontend/src/components/TodoList.tsx`.
- [ ] T053 Run the commands in `specs/004-react-todo-frontend/quickstart.md` from `backend/` and `frontend/`. Backend coverage stays at or above 90. Playwright's temporary directory is gone afterward. Do not weaken `backend/tests/` account or todo behavior.
- [ ] T054 [P] Re-read `frontend/README.md` against `specs/004-react-todo-frontend/contracts/runtime.md` and `specs/004-react-todo-frontend/contracts/checks.md`. The documented ports are `5173`, `8000`, `8080`, `9090`, and, for Playwright only, `5174` and `8001`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup. Blocks every user story.
- **User Stories (Phase 3+)**: Depend on Foundational. P1 stories proceed in spec order: US1, US2, US3, US4, then US8. P2 stories follow: US5, US6, US7, US9, US10.
- **Polish (Phase 13)**: Depends on the stories you include. The handbook task T051 stays after the runtime and CI tasks.

### User Story Dependencies

- **User Story 1 (P1)**: After Foundational. No other story required. MVP.
- **User Story 2 (P1)**: After US1. `listTodos` is already in `frontend/src/api/todos.ts` from T018. This story adds the visible rows.
- **User Story 3 (P1)**: After US2 so the new todo has a list to appear in.
- **User Story 4 (P1)**: After US2. Uses a row from the list. Does not require edit or delete.
- **User Story 8 (P1)**: After the client exists. Screen-level 422 and 404 checks use create and complete from US3 and US4. The five transport tests in `frontend/tests/api/client.test.ts` do not need those screens.
- **User Story 5 (P2)**: After US2. Independent of delete and filter.
- **User Story 6 (P2)**: After US2. Independent of edit.
- **User Story 7 (P2)**: After US2. Mutations from US3, US4, US5, and US6 are what prove the filter sticks.
- **User Story 9 (P2)**: After the page builds. Can start once `frontend/package.json` can build, in parallel with later UI stories if the files differ.
- **User Story 10 (P2)**: After US1 through US7 for the Playwright workflow, and after US9 for the handbook's Compose and Nginx examples.

### Within Each User Story

- Tests fail before implementation.
- API functions before components that call them.
- T018 runs after T015 and before T016. The account lifecycle calls `listTodos` and does not add a second `GET /api/v1/todos`.
- Session wiring after the component and the API function exist.
- Do not mark a story done while its new tests are still failing.

### Parallel Opportunities

- T002 through T007 touch different files and can run together after T001.
- T008 and the directories from T001 are the base for T009's client; T008 can run beside T002.
- US1 tests T011, T012, and T013 can run together.
- US8 tests T029 and T030 can run together.
- US9 files T045 and T046 can run together after T044 is failing.
- US9 can proceed beside US5, US6, and US7 because those tasks edit different files. Do not edit `frontend/src/session/useTodoSession.ts` in two stories at once.

---

## Parallel Example: User Story 1

```bash
# Tests together, before implementation:
Task: "T011 tokenStore tests in frontend/tests/auth/tokenStore.test.ts"
Task: "T012 AccountPanel tests in frontend/tests/components/AccountPanel.test.tsx"
Task: "T013 account-switch race test in frontend/tests/session/accountSwitch.test.tsx"

# Then, in order:
Task: "T014 tokenStore in frontend/src/auth/tokenStore.ts"
Task: "T015 POST /api/v1/users in frontend/src/api/users.ts"
Task: "T018 listTodos in frontend/src/api/todos.ts"
Task: "T016 AccountPanel and session generation in frontend/src/session/useTodoSession.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete T014, T015, and T018, then T016. T018 is the list request the account lifecycle calls. The visible list stays in Phase 4.
3. Stop and run `frontend/tests/auth/tokenStore.test.ts`, `frontend/tests/components/AccountPanel.test.tsx`, and `frontend/tests/session/accountSwitch.test.tsx`.

### Incremental Delivery

1. Setup and Foundational.
2. US1 account session.
3. US2 list, US3 create, US4 complete and pending.
4. US8 failure sentences and loading.
5. US5 edit, US6 delete, US7 filter.
6. US9 local and Compose runtime.
7. US10 Playwright, CI, then the handbook.
8. Polish against `specs/004-react-todo-frontend/quickstart.md`.

### Parallel Team Strategy

1. Everyone finishes Setup and Foundational.
2. One person takes US1 then US2. Another can start US9's Compose test and Nginx files without editing the session hook.
3. US3, US4, and US8 stay with the person who owns `frontend/src/session/useTodoSession.ts`.
4. US10 starts when the workflow screen and the Compose files both exist.

---

## Notes

- [P] tasks use different files and do not depend on an unfinished task in the same phase.
- Do not modify `backend/src/todo_api/api/routes/`, `backend/src/todo_api/schemas/`, or `backend/src/todo_api/api/deps.py`.
- Do not log tokens, put them in URLs, or render todo text as HTML.
- Playwright must not reuse an existing backend process or `backend/todo.db`. `frontend/scripts/playwright-servers.sh` delegates each server to Python 3 `subprocess.Popen(..., start_new_session=True)` and stops those sessions with `os.killpg`. Cleanup runs once.
- A busy `127.0.0.1:8080` is a manual check in `specs/004-react-todo-frontend/quickstart.md`. Do not add a CI test that binds port 8080.
- T018 runs before T016. US1 and US2 share `listTodos`. Do not implement `GET /api/v1/todos` twice.
- Nginx receives `API_UPSTREAM` through `frontend/docker-entrypoint.sh` and `envsubst`, not through Nginx's own environment expansion.
- `npm audit --audit-level=high` stays a blocking CI job. A written exception does not make that job ignore a finding.
- The handbook in T051 is written only after the implementation files it describes exist.
- Commit after each task or logical group.
