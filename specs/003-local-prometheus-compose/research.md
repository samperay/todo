# Research: Local Prometheus Monitoring

## Runtime layout

**Decision**: Add `compose.yaml` at the repository root, `backend/Dockerfile` with `backend/.dockerignore`, and `deploy/prometheus/prometheus.yml`. Do not add a Grafana service, a dashboard file, an alert-rule file, or a production manifest.

**Rationale**: The repository has no Dockerfile and no Compose file. The API is started today with `uvicorn todo_api.main:app` from `backend/`, and `todo_api.main:app` is the FastAPI object `create_app()` builds. A root Compose file gives one `docker compose` command. The build context stays `backend/` because that directory holds `pyproject.toml` and `src/`.

**Alternatives considered**:

- Installing Prometheus on the host. Rejected because the spec requires one Compose action and no separate Prometheus install.
- Putting Compose inside `backend/`. Rejected because the Prometheus file is not Python package data, and the command would not match the repository root developers already use.
- Adding Grafana "for later." Rejected by the spec.

## API process inside the container

**Decision**: The image installs the existing project and runs `uvicorn todo_api.main:app --host 0.0.0.0 --port 8000`. The host publish is `127.0.0.1:8000:8000`. No new setting and no `DATABASE_URL` override. The default `sqlite+aiosqlite:///./todo.db` file stays on the container filesystem, with no volume.

**Rationale**: Prometheus reaches the API on the Compose network, so the process cannot listen only on container loopback. The spec's loopback rule applies to the published host ports. Binding Uvicorn to `0.0.0.0` does not publish the port on every host interface. Leaving SQLite unmounted keeps todo-row durability out of this feature. Startup still calls `init_schema()` through the existing lifespan, so the container needs no migration command. `--reload` is omitted; the spec does not require live code reload.

**Alternatives considered**:

- Publishing `8000:8000` without a host address. Rejected because Compose would bind every interface.
- A SQLite volume so todos survive API recreation. Rejected because FR-022 puts that persistence outside this feature.
- Changing the metrics middleware so counters exist before the first request. Rejected because FR-018 forbids metric changes. The verification procedure accounts for counters appearing on first use.

## Scrape target

**Decision**: One job, `todo-api`, with `metrics_path: /metrics`, `scrape_interval: 15s`, and target `todo-api:8000`. Global `scrape_interval` is also `15s`. No `rule_files`, no `alerting`, no honor-labels change, and no bearer token. Scrape timeout stays the Prometheus default, which is shorter than 15 seconds.

**Rationale**: Compose DNS resolves the service name `todo-api` to the API container. `localhost` inside Prometheus would be Prometheus itself. Phase 002 already serves `GET /metrics` without a credential and excludes that path from the three series. A single job with a 15-second global interval is what the targets page reports. Prometheus retries a down target on the next interval, so a slow API start becomes healthy without restarting Prometheus (FR-006).

**Alternatives considered**:

- `host.docker.internal` or the published host port. Rejected because the spec asks for service-name DNS, and the host port is loopback-only.
- `depends_on` with a health condition that blocks Prometheus until `/metrics` answers. Rejected because the spec requires Prometheus to tolerate starting first and recover on a later scrape.

## Prometheus image and TSDB volume

**Decision**: Pin `prom/prometheus:v3.13.4`. Mount `./deploy/prometheus/prometheus.yml` read-only at `/etc/prometheus/prometheus.yml`. Mount named volume `prometheus-data` at `/prometheus`, and set `--storage.tsdb.path=/prometheus`. Do not set `--storage.tsdb.retention.time`. Do not run the container as root.

**Rationale**: `v3.13.4` is the current LTS image (2026-09-29) and includes `promtool`. On 2026-10-18 the tag `prom/prometheus:v3.13.4` was present on Docker Hub for `linux/amd64` and `linux/arm64`, so the pin does not need a substitute. A pinned tag keeps the environment reproducible; `latest` does not. The image's default TSDB directory is `/prometheus`, and a named volume survives `docker compose restart`, `docker compose down`, and container recreation. `docker compose down -v`, or an explicit volume delete, is the reset in FR-013. Default retention matches the spec. The image's `/prometheus` directory is created for the Prometheus user, so a new named volume is writable without a root user.

**Alternatives considered**:

- `prom/prometheus:v3.15.0` (newer feature release) or `:latest`. Rejected in favor of the LTS tag.
- A bind mount of a repository directory for the TSDB. Rejected because it is easy to commit or delete by accident and is worse across machines.
- A custom retention flag. Rejected because the spec accepts ordinary default retention.

## Configuration check

**Decision**: Developers validate the file Prometheus loads with:

```bash
docker compose run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml
```

`promtool` exits non-zero for a configuration Prometheus would reject. The same image tag supplies the binary, so developers do not install Prometheus on the host. `--no-deps` keeps the check from starting the API.

pytest reads the committed `compose.yaml` and `deploy/prometheus/prometheus.yml` and asserts the loopback publishes, the 15-second interval, the `todo-api:8000` target, the `/metrics` path, the named volume, and the absence of Grafana, `rule_files`, and secrets. That test does not start Docker. The existing CI workflow is unchanged.

**Rationale**: `promtool check config` is the validity check the spec names. It does not assert the interval or the target address, so the pytest locks those committed values. The spec does not require this procedure in the current CI jobs. Keeping Docker out of default pytest avoids a new CI dependency.

**Alternatives considered**:

- A Python YAML parser as the only check. Rejected because FR-014 requires a check Prometheus itself accepts, which is `promtool`.
- Running `promtool` inside the default pytest job. Rejected for the current CI shape. The quickstart still runs it on every verification.

## PromQL

**Decision**: Document a one-minute window. Throughput and the 4xx rate use `rate()` without a zero substitution. The 5xx query appends `or vector(0)`. P50 and P95 use `histogram_quantile()` over `rate(http_request_duration_seconds_bucket[1m])`. Queries read the existing labels and do not introduce series.

**Rationale**: Two samples 15 seconds apart fit in `[1m]`, so verification does not wait five minutes. `sum(rate(http_requests_total{status=~"5.."}[1m]))` is an empty vector when no 5xx series has ever existed; `or vector(0)` is what turns that absence into the number 0. Applying the same substitution to throughput or the 4xx query would hide a missing series, which the spec forbids. `rate()` over two samples that both occur after the counters have stopped increasing can be 0. The verification window therefore includes the baseline sample and the next sample. A series with only the post-traffic sample is not enough: `rate()` needs an earlier sample of that same series.

**Alternatives considered**:

- Reusing the Phase 002 five-minute catalog queries as the local check. They stay valid, but a five-minute wait breaks SC-003.
- `increase()` instead of `rate()`. Rejected because the spec asks for throughput and error rates as per-second rates.

## Verification order

**Decision**: The written procedure is:

1. Build and start with `docker compose up -d --build`.
2. Confirm `http://127.0.0.1:8000/metrics` returns 200 and the Prometheus target is up, with a 15-second interval.
3. Before any verification traffic, create both kinds of counter series: one successful response (`POST /api/v1/users`, status 201, then `GET /api/v1/todos` with that token, status 200) and one HTTP 4xx (`POST /api/v1/todos` without the token, status 401). These requests are not part of the 10.
4. Wait for one successful scrape that stores both a `2xx` `http_requests_total` series and a `4xx` `http_requests_total` series. That scrape is the baseline.
5. Send at least 10 additional completed requests that raise those existing series: successful todo calls with the token, and at least one more 401 on the same unauthenticated write. Do not manufacture a 5xx, and do not use a new label set as the only 4xx.
6. Wait for the next successful scrape. Query immediately, while `[1m]` still contains the baseline sample and that later sample.
7. Expect a non-zero throughput, a non-zero 4xx rate, a 5xx result of the number 0, and numeric P50 and P95.
8. Restart or recreate the Prometheus container without deleting `prometheus-data`, and range-query the minute from before the restart.
9. Run the `promtool` check.

Do not treat a second post-traffic scrape as the proof of a non-zero rate.

**Rationale**: `http_requests_total` is a labeled counter. Each combination of `method`, `handler`, and `status` is its own series, and the child series is created on first use. `rate()` is the increase per second between samples of one series. It uses the first and last sample inside the window. One sample has no earlier value, so there is no increase to divide by time. Prometheus drops that series from `rate()`. The counter value on that single sample is only the total Prometheus first stored, including requests that happened before any scrape. Those requests never become a rate.

A 4xx series created during the additional traffic and seen by only the next scrape is that one-sample case. `sum(rate(http_requests_total{status=~"4.."}[1m]))` stays empty even though a 401 occurred. The same is true for a success series. The baseline scrape must already contain both a success series and a 4xx series, and the 10 later requests must increment those same series so the next scrape is the second sample and the value is higher. Histogram buckets for those same responses are created by the same calls, so the latency `rate()` also has two samples. Two scrapes that both happen after the counters have stopped rising can share one value and yield 0. The baseline calls, the 10 calls, and two 15-second intervals fit in the 5-minute query budget. A Prometheus restart after that still fits in 15 minutes.

**Alternatives considered**:

- Priming only `POST /api/v1/users` and sending the 4xx during the 10 requests. Rejected. The 4xx series would have a single post-traffic sample, and its rate would be empty.
- Waiting for two scrapes after the 10 requests and expecting a non-zero rate. Rejected. Those samples can be flat, and a series born on the first of them still has no increase until a later change.
- Initializing zero series in the application so the first healthy scrape is a counter baseline. Rejected because it changes the metrics.
- Forcing a 500 to prove the 5xx query. Rejected. The query must return numeric 0 when no 5xx series exists.

## Loopback and port conflicts

**Decision**: Compose port entries are `127.0.0.1:8000:8000` and `127.0.0.1:9090:9090`. If either host port is taken, `docker compose up` fails with the engine's address-in-use error. There is no fallback port and no `0.0.0.0` publish.

**Rationale**: That is the default the spec requires, and a failed publish cannot be mistaken for a healthy target on another process.

**Alternatives considered**: An automatic port search. Rejected because a silent move would hide a conflict.
