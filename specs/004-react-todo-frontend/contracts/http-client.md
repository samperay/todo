# Contract: Browser HTTP Client

The client calls only the operations already implemented. Shapes are [the Phase 001 OpenAPI contract](../../001-todo-management/contracts/todos.openapi.yaml). Route modules win if that file and the code ever differ: `backend/src/todo_api/api/routes/users.py`, `backend/src/todo_api/api/routes/todos.py`, `backend/src/todo_api/schemas/user.py`, `backend/src/todo_api/schemas/todo.py`, and `backend/src/todo_api/api/errors.py`.

## Lifecycle

```text
Browser page
  -> React event
  -> Fetch API, relative /api/v1/...
  -> same origin
       local:  Vite on 127.0.0.1:5173 forwards /api to the FastAPI process
       container: Nginx on container port 80 forwards /api/v1/ to the FastAPI service
  -> FastAPI
  -> service
  -> repository
  -> SQLite
```

The browser does not call `127.0.0.1:8000` directly. The browser does not call `/metrics`.

## Common rules

| Rule | Behavior |
|------|----------|
| Paths | Relative `/api/v1/...` only |
| Timeout | Abort after 10 seconds. If the session generation is still the one that started the request, that abort is the timeout notice. |
| Session | Each call records the session generation. Logout, create-account, paste, and `401` increment it and abort older calls. A result is applied only when its generation is still current. |
| JSON | `Content-Type: application/json` only when a body is sent |
| Authorization | `Authorization: Bearer <token>` on todo calls. The header is omitted when no token is stored. The token is not logged. |
| Success JSON | Parse JSON and require the fields listed below. A success status with the wrong shape is the server notice, not a thrown stack in the UI. |
| `204` | Success with no body. Do not parse JSON. |
| Account change | Increment the generation, abort older calls, and clear todos and the open editor before the next list request. A late body from the old generation is ignored. See [data-model.md](../data-model.md). |
| List refresh | Every reload of the todo list calls `listTodos` in `frontend/src/api/todos.ts`. That function is the only `GET /api/v1/todos` implementation. |

## Operations

### Create account

| | |
|--|--|
| Method and path | `POST /api/v1/users` |
| Body | None |
| Auth | None |
| Success | `201` `{id, token}` |
| Client effect | Store both. Set the one-time reveal. Clear any previous list. Then `GET /api/v1/todos`. |

### List todos

| | |
|--|--|
| Method and path | `GET /api/v1/todos` |
| Body | None |
| Auth | Bearer |
| Success | `200` array of todos. Empty array is the empty-account state. |
| Order | Keep the array order. Do not sort again. |

### Create todo

| | |
|--|--|
| Method and path | `POST /api/v1/todos` |
| Body | `{title}` plus `description` and `priority` only when set |
| Auth | Bearer |
| Success | `201` todo, then call `listTodos`. Do not insert the body by a second list implementation. |

### Update todo

| | |
|--|--|
| Method and path | `PATCH /api/v1/todos/{id}` |
| Body | Only changed `title`, `description`, or `priority`. `description: null` clears it. |
| Auth | Bearer |
| Success | `200` todo, then call `listTodos` |
| Not sent | No changed field. `completed` and `id` are never sent. |

### Complete and incomplete

| | |
|--|--|
| Complete | `POST /api/v1/todos/{id}/complete` with no body |
| Incomplete | `POST /api/v1/todos/{id}/incomplete` with no body |
| Auth | Bearer |
| Success | `200` todo, then call `listTodos` |
| Already in that state | `200` and unchanged fields. Not an error. |

### Delete

| | |
|--|--|
| Method and path | `DELETE /api/v1/todos/{id}` |
| Body | None |
| Auth | Bearer |
| Success | `204` and no body, then call `listTodos` |

`GET /api/v1/todos/{id}` exists and is not used by this screen.

## Status handling

| Status | Body the service sends | Screen |
|--------|------------------------|--------|
| `401` | `{error:{code:"unauthenticated", message:"You must be identified."}}` | Unauthenticated notice. Increment the generation and clear the list. Do not show the token. |
| `404` | `{error:{code:"not_found", message:"Todo not found"}}` | Not-found notice. Do not add an ownership hint. Keep the current generation's list. |
| `422` | `{detail:[{loc, msg, type, ...}]}` | Plain rule sentence from [research.md](../research.md). Do not show the raw `detail` array. Keep the list. |
| `502` | Ignored | Bad-gateway notice. Do not show the body. Keep the list. |
| `504` | Ignored | Gateway-timeout notice. Do not show the body. Keep the list. |
| Other `5xx` | Ignored | Server notice. Do not show the body. Keep the list. |
| Client timer abort | None | Timeout notice, only if the generation is still current. |
| Session abort | None | Discard. No notice from that call. |
| Browser network failure | None. Fetch rejects before a status. | Unreachable notice. This is not the timeout notice. |

The five transport sentences are fixed:

| Class | Sentence |
|-------|----------|
| Client timeout | The request timed out. |
| HTTP 502 | The proxy could not get a valid response from the service. |
| HTTP 504 | The proxy timed out waiting for the service. |
| Other HTTP 5xx | The action could not be completed. |
| Browser network failure | The service could not be reached. |

Todo object fields required on every success todo: `id`, `title`, `description`, `completed`, `priority`, `created_at`, `updated_at`. `description` may be `null`. `priority` is `low`, `medium`, or `high`.
