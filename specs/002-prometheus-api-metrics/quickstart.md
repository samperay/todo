# Quickstart: Prometheus API Metrics

Validation guide for the measurements in [plan.md](./plan.md). Series and labels are in [data-model.md](./data-model.md). The scrape response is in [contracts/metrics.openapi.yaml](./contracts/metrics.openapi.yaml). Queries for the four operational panels are in [contracts/metrics-catalog.md](./contracts/metrics-catalog.md). This feature does not include Grafana.

## Prerequisites

- Python 3.12 or newer
- The existing Todo API setup from the repository README
- No Prometheus or Grafana process is required for the automated checks

## Setup

From `backend/`, with the virtual environment active, after `prometheus-client` is in the project dependencies:

```bash
pip install -e ".[dev]"
```

## Automated checks

From `backend/`:

```bash
pytest
```

Expected:

- Existing todo and user tests still pass, including status codes and response bodies.
- `tests/api/test_metrics.py` passes and shows all of the following:
  - `GET /metrics` returns 200 and a Prometheus text body that includes `http_requests_total`, `http_request_duration_seconds`, and `http_requests_in_progress`. Handling that request does not invoke a Todo or User repository, database or session access, or an external HTTP or network client. There is no wall-clock assertion.
  - A scrape before any todo traffic does not report completed todo requests.
  - A known mix of successes, client errors 401, 404, and 422, and a server error matches `http_requests_total` exactly, with 4xx and 5xx separate from successes.
  - Two requests for different todo ids share `handler="/api/v1/todos/{todo_id}"`. The id, title, description, and token do not appear in the body. No raw path becomes a handler.
  - The histogram records those completed requests, including errors. The exposition includes `http_request_duration_seconds_bucket` with the default prometheus-client buckets, plus `http_request_duration_seconds_sum` and `http_request_duration_seconds_count`, so Prometheus can estimate P50 and P95 with `histogram_quantile()`. The check validates observations, buckets, count, and sum. It does not assert that an estimate lies between the fastest and slowest sample, and the application does not calculate exact percentiles.
  - Repeating `GET /metrics` does not increase `http_requests_total`.
  - While requests are held open, `http_requests_in_progress` for that HTTP method equals that number, with no `handler` or `status` label. After they finish, fail, or disconnect, that same method series returns to its previous level.
  - A failure while recording does not change the todo status or body. The in-progress gauge still returns to its previous level.

`pytest` uses a temporary SQLite file. It does not need `DATABASE_URL`.

## Manual scrape

From `backend/`, start the API:

```bash
uvicorn todo_api.main:app --reload
```

Request the snapshot with no bearer token:

```bash
curl -sD - http://127.0.0.1:8000/metrics -o /tmp/metrics.txt
```

Expected: HTTP 200, a Prometheus text content type, and the three series names in `/tmp/metrics.txt`.

Create a person and one todo the same way the README does, then scrape again. Expected: `http_requests_total` includes `handler="/api/v1/users"` and `handler="/api/v1/todos"`. Another scrape does not add a series for `/metrics`. The token and todo title are absent from `/tmp/metrics.txt`.

The queries in [contracts/metrics-catalog.md](./contracts/metrics-catalog.md) are what an operator uses for request rate, latency percentiles, error rate, and in-progress requests. This repository does not add Grafana.
