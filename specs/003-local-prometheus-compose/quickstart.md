# Quickstart: Local Prometheus Monitoring

Validation guide for [plan.md](./plan.md). The stack contract is [contracts/compose-stack.md](./contracts/compose-stack.md). The scrape file contract is [contracts/prometheus-scrape.md](./contracts/prometheus-scrape.md). Queries are [contracts/promql-queries.md](./contracts/promql-queries.md). The pass/fail order is [contracts/verification.md](./contracts/verification.md). Series and labels stay the Phase 002 catalog. This feature does not include Grafana or alerting.

## Prerequisites

- Docker Compose v2
- Nothing else. Prometheus is the `prom/prometheus:v3.13.4` image. Do not install it on the host.
- Ports `127.0.0.1:8000` and `127.0.0.1:9090` are free

## Automated checks

From `backend/`, with the virtual environment active:

```bash
pytest
```

Expected:

- Existing todo, user, and metrics tests still pass. Series names and labels are unchanged.
- `tests/compose/test_monitoring_config.py` passes and checks the committed files for:
  - publishes `127.0.0.1:8000:8000` and `127.0.0.1:9090:9090`
  - scrape interval `15s`, path `/metrics`, target `todo-api:8000`
  - named volume `prometheus-data` mounted at `/prometheus`
  - no Grafana service, no `rule_files`, and no secret

This pytest does not start containers. The existing CI workflow does not need a change.

## Validate the Prometheus file

From the repository root:

```bash
docker compose run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml
```

Expected: the command exits 0.

To see a failure, point the same `promtool check config` at a temporary copy that Prometheus rejects (for example a broken duration). Expected: non-zero exit. Do not start the stack with that broken file.

## Start

From the repository root:

```bash
docker compose up -d --build
```

Expected within 2 minutes:

- `http://127.0.0.1:8000/metrics` returns 200 and a Prometheus text body
- `http://127.0.0.1:9090` answers
- `docker compose port todo-api 8000` prints `127.0.0.1:8000`
- `docker compose port prometheus 9090` prints `127.0.0.1:9090`

Open the Prometheus targets page. Within 45 seconds of the API listening, the `todo-api` target is up, the scrape URL ends in `todo-api:8000/metrics`, and the interval is 15 seconds.

If the API is still starting, the target may be down for one interval. Leave Prometheus running. The next successful scrape marks it up.

## Baseline, then traffic

Do these steps without a long pause. The one-minute query window has to contain the baseline scrape and the next scrape.

`rate()` needs two stored samples of the same counter series. A series Prometheus has seen only once has no earlier value, so `rate()` omits it. The single sample is the counter total at the first scrape, not a per-second increase. Requests that created the series are already inside that total and do not produce a rate. Create both a success series and a 4xx series, let one scrape store both, then raise those same series.

1. Create a person and record one success and one client error. These calls are not part of the 10.

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/users
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/api/v1/todos
curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
```

The list call returns 200. The write without a token returns 401.

2. Wait until one scrape has stored both kinds of series. These instant queries each return at least one series:

```promql
http_requests_total{status=~"2.."}
```

```promql
http_requests_total{status=~"4.."}
```

That scrape is the baseline. Note the time.

3. Send at least 10 more completed requests that increase those series. Nine more authorized list calls and one more unauthenticated write is enough. Do not add a request meant to return 500, and do not use a different client error as the only 4xx.

4. Wait for the next successful scrape. Then run the queries in [contracts/promql-queries.md](./contracts/promql-queries.md) immediately, while the one-minute window still holds the baseline scrape and this scrape.

Expected:

- `sum(rate(http_requests_total[1m]))` is greater than 0
- `sum(rate(http_requests_total{status=~"4.."}[1m]))` is greater than 0
- `sum(rate(http_requests_total{status=~"5.."}[1m])) or vector(0)` is the number 0, not an empty result
- the P50 and P95 `histogram_quantile()` queries each return a number
- the results contain no token and no todo title

Do not use two scrapes that both happened after step 3 as the proof. If nothing was requested between them, `rate()` can be 0. A 4xx series that first appears on only one of those scrapes is also not a rate.

## Persistence

With samples stored, restart Prometheus without deleting the volume:

```bash
docker compose restart prometheus
```

After it is up, a range query whose window includes the minute before the restart still returns `http_requests_total` samples.

Recreate the container without the volume flag and repeat that range query. The samples are still there. Recreating the API container may drop todo rows. That is expected and is not a failure of this check.

Reset Prometheus only on purpose:

```bash
docker compose down -v
```

The next start has an empty TSDB and can become healthy again after new scrapes.

## Stop

```bash
docker compose down
```

The named volume remains. The targets page is gone until the next start.

## Out of scope

Grafana, alert rules, production hosting, and persisting the API's SQLite file are not part of this guide.
