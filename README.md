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

## Local Prometheus queries

Run these in Prometheus at `http://127.0.0.1:9090`. The window is one minute, so a scrape and the next scrape 15 seconds later both fit inside it. The series and labels are the existing ones: `http_requests_total` and `http_request_duration_seconds` use `method`, `handler`, and `status`. `status` is the numeric HTTP code as text. `http_requests_in_progress` uses `method` only and is not one of these queries.

Scrapes of `/metrics` and `/metrics/` are not recorded on those three series. A Prometheus collection therefore does not add a request, a latency observation, or an in-progress count.

An empty result means the selector matched no series. It is not the number 0, and it is not a query error. Throughput and the client-error query stay empty in that case. Only the server-error query turns that absence into the number 0.

### Request throughput

Completed API requests per second, split by method, action, and outcome. The value is requests per second.

```promql
sum by (method, handler, status) (rate(http_requests_total[1m]))
```

The same rate with the labels summed away. The value is still requests per second. Before any completed request has been stored, this result is empty.

```promql
sum(rate(http_requests_total[1m]))
```

### HTTP 4xx rate

Client errors per second. Successful responses are not in this selector. The value is requests per second. If no 4xx series exists, the result is empty, not 0.

```promql
sum(rate(http_requests_total{status=~"4.."}[1m]))
```

### HTTP 5xx rate

Server errors per second. The value is requests per second when a 5xx series exists. When no 5xx series exists, the `rate()` selector is empty, and `or vector(0)` returns the number 0 instead of that empty result. The local check does not create a server error, so the expected result is the number 0.

```promql
sum(rate(http_requests_total{status=~"5.."}[1m])) or vector(0)
```

### Latency

Median and 95th percentile of request latency, in seconds. Prometheus estimates both from the existing `http_request_duration_seconds` histogram. The application does not calculate them.

```promql
histogram_quantile(
  0.50,
  sum by (le) (rate(http_request_duration_seconds_bucket[1m]))
)
```

```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[1m]))
)
```

### What a non-zero rate requires

`rate()` is the per-second increase between the first and last sample of one series inside the window. A series is one `method`, `handler`, and `status` combination on `http_requests_total`. The counter must be higher on the later sample.

`rate()` needs two samples of that same series. A newly created counter with only one sample has no earlier value, so Prometheus omits it. That lone sample is the counter total at the first scrape, not a per-second rate. Requests that created the series are already inside that total.

The baseline scrape must already contain both a successful-response series and an HTTP 4xx series. Traffic sent only after that scrape can raise those same series. A success or 4xx series that appears for the first time on the later scrape has only one sample, so `rate()` omits it and the query stays empty for that series. Two scrapes that both happen after the traffic, with no further requests between them, can share the same counter value and produce a rate of 0.

## Prometheus Data Persistence

Prometheus stores its time-series samples in the Docker named volume `prometheus-data`. That volume is mounted at `/prometheus`. Samples survive a Prometheus stop, start, and `docker compose restart`. They also survive container recreation when the named volume `prometheus-data` is retained.

`docker compose down` removes the containers and preserves the named volume, so the stored samples survive. `docker compose down -v` removes the named volume and deletes its stored monitoring data. That command is the explicit delete.

`todo-api` has no database volume. Its SQLite database stays the default `sqlite+aiosqlite:///./todo.db` on the container filesystem. SQLite data stored inside the API container is lost when that container is removed. This setup does not keep todo rows across an API container restart.

## Verify the local stack

Run this from the repository root. The query checks fit in 5 minutes after the target is healthy, and the full procedure fits in 15 minutes. It is not part of the GitHub Actions workflow.

1. Validate the delivered Prometheus file. The command exits 0.

```bash
docker compose run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml
```

Copy that file to a temporary path, break the copy, and run `promtool check config` on the copy. The command exits non-zero. Leave the delivered file unchanged, and do not start the stack from the copy.

2. Start the stack.

```bash
docker compose up -d --build
```

3. The API answers at `http://127.0.0.1:8000` and Prometheus at `http://127.0.0.1:9090`. Both published ports bind to `127.0.0.1`.

4. The `todo-api` target becomes healthy and reports a 15-second interval. If Prometheus starts before the API accepts collections, the target is unhealthy at first and becomes healthy on a later scrape. Do not restart Prometheus for that recovery.

5. Before the 10 verification requests, create both a successful response and an HTTP 4xx response. These calls are not part of the 10. `POST /api/v1/users` returns 201 and a token. Authorized `GET /api/v1/todos` returns 200. Unauthenticated `POST /api/v1/todos` returns 401.

6. Wait for one successful scrape that contains both a `2xx` `http_requests_total` series and a `4xx` `http_requests_total` series. That scrape is the baseline. A one-sample counter is not a rate: `rate()` has no earlier sample to subtract, so Prometheus omits it.

7. Send at least 10 additional completed requests that increase those same series, including successes and another HTTP 4xx response. Do not send a request chosen to produce HTTP 5xx.

8. Wait for the next scrape. Do not wait for a second scrape after that traffic. Two scrapes that both happen after the additional traffic, with no further requests between them, can share the same counter value and produce a rate of 0.

9. Immediately run the one-minute queries above. The window must still contain the baseline scrape and this next scrape. Throughput is greater than 0, the 4xx rate is greater than 0, the 5xx query returns the number 0, and the P50 and P95 queries return numbers.

10. Restart or recreate the Prometheus container without deleting `prometheus-data`. Samples from before that change remain queryable.

11. `docker compose down` stops the stack and leaves the named volume in place.

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
