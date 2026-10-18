# Data Model: Local Prometheus Monitoring

This feature does not add an application table or a metric series. The objects below are the local runtime a developer starts and inspects. Series names and labels are the Phase 002 contract in [../002-prometheus-api-metrics/contracts/metrics-catalog.md](../002-prometheus-api-metrics/contracts/metrics-catalog.md). This feature does not change them.

## Local monitoring stack

The two processes started and stopped together.

| Field | Rule |
|-------|------|
| Services | `todo-api` and `prometheus` only |
| Start | `docker compose up -d --build` from the repository root |
| Stop | `docker compose down` |
| API image command | `uvicorn todo_api.main:app --host 0.0.0.0 --port 8000` |
| API published address | `127.0.0.1:8000` only |
| Prometheus published address | `127.0.0.1:9090` only |
| API database | Default `sqlite+aiosqlite:///./todo.db` on the container filesystem. No volume. Rows may disappear when the API container is recreated. |
| Secrets | None in the Compose file or the Prometheus file |

Removing either service, or adding Grafana or Alertmanager, breaks the stack contract.

## Scrape target

The single Prometheus job that collects the existing metrics endpoint.

| Field | Rule |
|-------|------|
| Job name | `todo-api` |
| Target | `todo-api:8000` |
| Path | `/metrics` |
| Scheme | `http` |
| Interval | 15 seconds |
| Credential | None |
| Health | Up after a successful collection. Down, with the error visible, when the API cannot be collected. |
| Recovery | A later successful collection marks the target up without recreating Prometheus. |

`localhost` and `127.0.0.1` are not valid targets. Inside the Prometheus container those addresses are Prometheus, not the API.

State of the target:

1. **Unknown / down** while the API is not answering.
2. **Up** after a collection of `/metrics` succeeds.
3. **Down** again if a later collection fails. Samples already stored stay in the TSDB.

## Stored sample

One collected value in the Prometheus TSDB.

| Field | Rule |
|-------|------|
| Location | Named volume `prometheus-data` mounted at `/prometheus` |
| Survives | Prometheus container stop, start, and recreation |
| Removed by | `docker compose down -v`, or another explicit delete of `prometheus-data` |
| Not included | Todo rows, bearer tokens, titles, or descriptions |
| Retention | Prometheus default. No custom retention flag. |

A restart of the API process can reset in-memory counters. It does not delete samples already stored. A restart of the API container can also discard `todo.db`. That is not a stored sample.

## Operational query

A PromQL request against the stored samples. The expressions are in [contracts/promql-queries.md](./contracts/promql-queries.md).

| Query | Result when series exist | Result when the selector matches nothing |
|-------|--------------------------|------------------------------------------|
| Throughput | Per-second rate of `http_requests_total`, splittable by `method`, `handler`, and `status` | Empty. Not the number 0. |
| Client-error rate | Per-second rate of `status` matching `4xx` | Empty. Not the number 0. |
| Server-error rate | Per-second rate of `status` matching `5xx` | The number 0, including when a 5xx series has never existed |
| P50 and P95 | `histogram_quantile()` estimates from `http_request_duration_seconds` | Empty. Not the number 0. |

A non-zero throughput or client-error rate is the increase between two samples of the same counter series. The baseline scrape must already contain at least one `2xx` series and one `4xx` series. The later scrape, after at least 10 additional requests, must show those series at higher values. A series stored only once has no earlier sample. `rate()` drops it, so that single observation is not a throughput or a 4xx rate. Two samples taken only after the additional traffic, with no further increase between them, can also produce a rate of 0.

## Configuration check

The pass or fail result of `promtool check config` on the file the Prometheus service loads.

| Input | Result |
|-------|--------|
| `deploy/prometheus/prometheus.yml` as shipped | Pass |
| A file Prometheus rejects | Fail, and that file is not left as a healthy running target |

The check uses `promtool` from `prom/prometheus:v3.13.4`. It does not replace the pytest that locks the interval, target, loopback ports, and volume.
