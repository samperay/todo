# Data Model: React and TypeScript Todo Frontend

No new table, column, or migration. SQLite stays behind the existing repository layer. The objects below are what the browser holds and what the screen shows. The stored todo shape is the existing `TodoResponse` in `backend/src/todo_api/schemas/todo.py`.

## Person

An account the existing `POST /api/v1/users` creates. The request has no body.

| Field | Rule |
|-------|------|
| id | UUID string from the `201` body. Displayed. Not chosen by the person. |
| token | String from that same body. Shown once. Stored in `localStorage` under `todo.token`. Never placed in the URL, logs, errors, or the repository. |

The screen has no name, email, or password. Logout deletes the browser copy of `id` and `token` and leaves the server credential in place.

## Access credential

The bearer token for todo calls.

| Field | Rule |
|-------|------|
| Storage | `localStorage` keys `todo.accountId` and `todo.token` |
| Header | `Authorization: Bearer <token>` on every todo call. Absent on `POST /api/v1/users`. |
| Lifetime in the browser | Until logout or until site data is cleared |
| Lifetime on the server | Until the server row is removed by means this feature does not add. Logout does not revoke it. |
| Replacement | Create-account or paste replaces both keys and clears the visible list first |
| Unknown token | `401` with `error.code` `unauthenticated`. Clear the visible list. |

A script on this origin can read `localStorage`. That is the accepted XSS limitation.

## Todo

One row the service already stores. The client does not invent fields.

| Field | Rule |
|-------|------|
| id | UUID. Stable. Not editable. |
| title | Required after trim. At most 200 characters. |
| description | String or `null`. At most 2000 characters. Whitespace-only becomes `null`. |
| completed | Boolean. Create starts `false`. Changed only by complete and incomplete. |
| priority | `low`, `medium`, or `high`. Omitted on create becomes `medium`. |
| created_at | ISO datetime. Not edited. List order is the array order from `GET /api/v1/todos`, newest `created_at` first. |
| updated_at | ISO datetime from the service. The client does not invent a new one. |

Ownership is not a response field. The client must not add one.

Create body fields are only `title`, and `description` or `priority` when the person set them. Update body fields are only the title, description, or priority that changed. Clearing a description sends `description: null`. An empty update is not sent.

## List view

A filter over the array already returned. It is not a request parameter.

| Value | Shows |
|-------|--------|
| all | Every todo in the returned order. This is the initial value. |
| pending | Items with `completed === false`, same relative order |
| completed | Items with `completed === true`, same relative order |

The empty-account state, the empty-filter state, and a failed first load are three different screens.

## Edit session

Page-local. Not stored on the server.

| Field | Rule |
|-------|------|
| openTodoId | The todo whose editor is open, or none |
| savingTodoId | The todo whose patch is in flight, or none |
| Same id | A second editor does not open and a second patch is not sent |
| Other id | May open |
| Other tab or client | Not tracked. No version field. |

Complete, reopen, and delete do not use this session. Each has its own in-flight flag so the same action is not sent twice.

## Screen session

React state in the page. Not a global store library.

| Field | Rule |
|-------|------|
| accountId | From storage or from the latest `201`, or none |
| token | From storage or from the latest `201` or paste, or none. Not rendered except the one-time reveal and the paste field. |
| revealToken | True only immediately after account creation, until the person dismisses it |
| todos | The last successful list for the current generation, or empty |
| listStatus | `idle`, `loading`, `ready`, or `error` |
| notice | The current failure notice, or none |
| filter | `all`, `pending`, or `completed` |
| pendingAction | The in-flight create, complete, reopen, or delete, or none |
| sessionGeneration | Integer. Starts at 0. Increases on logout, create-account success, paste, and `401`. |

Every in-flight request stores the generation that started it and an abort handle. Logout, create-account success, paste, and `401` increment `sessionGeneration`, abort the previous generation, set `todos` to empty, and clear `openTodoId`, `savingTodoId`, and `notice`. A response whose generation is no longer current is discarded. That includes a response that arrives after the new generation's request has already completed. Do not leave the previous account's rows mounted.

## Failure notice

One plain message. It does not include the token, a stack trace, SQL, or a raw error body.

| Kind | When | Fixed sentence | List for the current generation |
|------|------|----------------|--------------------------------|
| unauthenticated | No token, or `401` | The person must be identified. | Cleared |
| rejected | `422`, mapped to the rule sentence | The failed rule. | Unchanged |
| not_found | `404` | The todo was not found. | Unchanged. Do not say another person owns the id. |
| timeout | This request's 10-second timer aborted it, and the generation is still current | The request timed out. | Unchanged if a list was already ready. First-load failure stays on the error screen. |
| bad_gateway | HTTP `502` | The proxy could not get a valid response from the service. | Same as timeout |
| gateway_timeout | HTTP `504` | The proxy timed out waiting for the service. | Same as timeout |
| server | Any other HTTP `5xx`, or a success status whose JSON is not the expected shape | The action could not be completed. | Same as timeout |
| unreachable | The browser reports a network failure. This is not an abort. | The service could not be reached. | Same as timeout |

A session-change abort is not `timeout` and not `unreachable`. That request's result is discarded. No sentence from it is shown.

The sentence is chosen by the client. The response body is not shown. The bearer token is not shown. `502` and `504` are not folded into the other `5xx` sentence.

Loading is not a failure notice. An empty list is not a failure notice.

## What this feature does not store

- No new SQLAlchemy model and no change to `todo.db` schema.
- No volume for the API container's SQLite file.
- No todo contents or tokens in Compose, Nginx, images, or CI config.
- Prometheus samples stay on the existing `prometheus-data` volume and are not a frontend entity.
