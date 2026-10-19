# Contract: Verification procedure

This is the repeatable check for [spec.md](../spec.md) FR-016 and SC-003 through SC-005. Commands and expected observations are in [quickstart.md](../quickstart.md). Queries are in [promql-queries.md](./promql-queries.md).

## Order

The steps run in this order. A later step does not replace an earlier one.

1. **Config**. `promtool check config` passes for `deploy/prometheus/prometheus.yml`. A configuration Prometheus rejects fails that same command.
2. **Start**. `docker compose up -d --build` brings up `todo-api` and `prometheus` only.
3. **Ports**. The API answers at `http://127.0.0.1:8000` and Prometheus at `http://127.0.0.1:9090`. Both publishes are bound to `127.0.0.1`.
4. **Health and interval**. The `todo-api` target is up and reports a 15-second interval. This can happen within 45 seconds of the API listening.
5. **Baseline series**. Before the 10 verification requests, send a successful response and an HTTP 4xx response. `POST /api/v1/users` returns 201 and a token. `GET /api/v1/todos` with that token returns 200. `POST /api/v1/todos` without the token returns 401. These calls are not part of the 10.
6. **Baseline scrape**. Wait for one successful scrape that contains both a `2xx` `http_requests_total` series and a `4xx` `http_requests_total` series. That scrape is the baseline. A series that appears for the first time later has only one sample, and `rate()` cannot turn that sample into a per-second increase.
7. **Traffic**. Send at least 10 additional completed requests that increase the baseline series: successful todo requests with the token, and at least one more HTTP 4xx on the same unauthenticated write. Do not send a request chosen to produce HTTP 5xx.
8. **Next scrape**. Wait for the next successful scrape after that traffic. Do not wait for a second post-traffic scrape.
9. **Queries**. Immediately run the one-minute queries. The window includes the baseline scrape and this next scrape. Throughput is greater than 0, the 4xx rate is greater than 0, the 5xx query returns the number 0, and P50 and P95 are numeric.
10. **Persistence**. Restart or recreate the Prometheus container without deleting `prometheus-data`. A range query for the minute before the restart still returns samples. Todo rows are not checked.
11. **Stop**. `docker compose down` stops the stack and leaves the volume in place.

Steps 5 through 9 finish within 5 minutes of the target becoming healthy. Steps 1 through 10 finish within 15 minutes.

## Pass and fail

| Check | Pass | Fail |
|-------|------|------|
| `promtool` on the shipped file | Exit 0 | Non-zero exit |
| `promtool` on a file Prometheus rejects | Non-zero exit | Exit 0 |
| Published addresses | `127.0.0.1:8000` and `127.0.0.1:9090` | Any other bind, including every interface |
| Target | Up, path `/metrics`, interval 15 seconds | Down after the API is ready, or a different interval |
| Throughput and 4xx rate | Numbers greater than 0. The baseline scrape already had both a success series and a 4xx series, and the next scrape shows those series increased | Empty because a series has only one sample, or 0 from two flat post-traffic samples |
| 5xx rate | The number 0 | Empty, or a number greater than 0 |
| Latency | Numeric P50 and numeric P95 | Empty |
| Prometheus restart | Pre-restart samples still queryable | Those samples are gone while the volume was kept |
| Stack contents | `todo-api` and `prometheus` only | A Grafana or alerting service |

## Out of scope for this procedure

- Grafana panels and alert rules.
- A production deploy.
- Todo rows surviving an API container restart.
- A new metric or label.
- Running this procedure in the existing GitHub Actions jobs.
