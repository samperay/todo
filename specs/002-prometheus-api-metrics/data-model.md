# Data Model: Prometheus API Metrics

No new persisted entity. The process registry holds the measurements below and drops them when the process stops. Field rules for persons and todos are unchanged from [../001-todo-management/data-model.md](../001-todo-management/data-model.md).

Series names, labels, and types are the contract in [contracts/metrics-catalog.md](./contracts/metrics-catalog.md).

## Metrics snapshot

The document returned by `GET /metrics`.

| Field | Rule |
| --- | --- |
| Format | Prometheus text exposition |
| Contents | The completed-request, latency, and active-request series currently in that process |
| Excluded values | Todo titles, descriptions, bearer tokens, user ids, and raw resource ids |
| Lifetime | Computed when scraped. Not stored as a row. |

## Completed-request measurement

| Field | Rule |
| --- | --- |
| Series | `http_requests_total` |
| method | HTTP method of the finished request |
| handler | Matched route template, or `unmatched` |
| status | Numeric status as text |
| value | Count of finished requests with that method, handler, and status since process start |

A scrape of `/metrics` or `/metrics/` does not increment this series.

Client errors are observations whose status is in 400–499. Server errors are 500–599. Any other finished status is success. These classes are queries over `status`, not separate stored fields.

## Latency measurement

| Field | Rule |
| --- | --- |
| Series | `http_request_duration_seconds` |
| method, handler, status | Same meanings as the completed-request measurement |
| value | Distribution of elapsed seconds from the time the middleware saw the request until the response finished |
| Buckets | Library default buckets, in seconds. The snapshot exposes `_bucket`, `_sum`, and `_count` so `histogram_quantile()` can estimate a 50th and a 95th percentile. The estimate is not required to lie inside the raw minimum and maximum of a sample. |

Every finished request that increments the counter also contributes one observation here, including client and server errors. Scrapes of the metrics path do not.

## Active-request measurement

| Field | Rule |
| --- | --- |
| Series | `http_requests_in_progress` |
| method | HTTP method of the open request. This is the only label. |
| value | Requests of that method that have entered the app and have not finished |

The series MUST NOT include `handler` or `status`. The value is a level, not a total since startup.

### State

1. A non-scrape request enters: increase the gauge for that method by one.
2. The request finishes with a response, fails, or the caller disconnects: decrease that same method series by one in `finally`, including when recording the completion counter or histogram fails.
3. With nothing in flight, every series of this gauge is zero.

A scrape does not enter this state machine.

## API action

Not a stored record. It is the `handler` label on the completed-request counter and the latency histogram. It is not a label on the in-progress gauge.

| Handler | When it is used |
| --- | --- |
| `/api/v1/users` | Create person |
| `/api/v1/todos` | Create or list todos |
| `/api/v1/todos/{todo_id}` | Retrieve, update, or delete one todo |
| `/api/v1/todos/{todo_id}/complete` | Mark completed |
| `/api/v1/todos/{todo_id}/incomplete` | Mark incomplete |
| Framework template such as `/docs` or `/openapi.json` | Requests that hit those routes |
| `unmatched` | No route matched |

The value inside `{todo_id}` is never a label. Method distinguishes list from create, and retrieve from update or delete, on a shared template.

## Relationships

- One snapshot reads all three measurements for the process that served it.
- Each completed request updates one completed-request series and one latency series, and closes one active-request increment.
- Measurements do not reference Person or Todo rows.

## Validation

- Counter and histogram label values are the method, the template or `unmatched`, and the status. They must not be taken from the JSON body or the `Authorization` header.
- The in-progress gauge label is only the method.
- Completed and latency observations are written only after the request finishes.
- The active gauge for a request cannot stay increased after that request ends.
- The method series increased at the start of a request is the series decreased in `finally`.
