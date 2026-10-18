# Tasks: Local Prometheus Monitoring

**Input**: Design documents from `/specs/003-local-prometheus-compose/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included for the committed runtime files. Constitution III requires pytest, and the plan names `backend/tests/compose/test_monitoring_config.py`. Write each story's file assertions first and confirm they fail before adding the files they describe. Do not add a Docker step to the existing GitHub Actions jobs. Do not change `backend/tests/api/test_metrics.py` except to keep running it as the guard that series and labels are unchanged.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Runtime**: `compose.yaml`, `deploy/prometheus/prometheus.yml`, `backend/Dockerfile`, `backend/.dockerignore`, `README.md`
- **Tests**: `backend/tests/compose/test_monitoring_config.py`
- **Application entry point, unchanged**: `backend/src/todo_api/main.py`
- Paths match `specs/003-local-prometheus-compose/plan.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Keep the API image free of local secrets and the host database. The FastAPI app, metrics, and tests already exist.

- [ ] T001 Add `backend/.dockerignore` so the image build excludes `.venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.env`, `todo.db`, and `*.db`. Do not add a Grafana file, an alert-rule file, or a new Python dependency in `backend/pyproject.toml`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Package the existing API so Compose can start it. No metric, route, or settings change.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T002 Add `backend/Dockerfile` from `python:3.12-slim` that installs the project in `backend/pyproject.toml` and `backend/src` and runs `uvicorn todo_api.main:app --host 0.0.0.0 --port 8000`. Do not pass `DATABASE_URL`, do not mount SQLite, do not use `--reload`, and do not edit `backend/src/todo_api/main.py` or `backend/src/todo_api/observability/metrics/`.

**Checkpoint**: The API image builds and listens on `0.0.0.0:8000` inside the container. Host publishing is not this phase.

---

## Phase 3: User Story 1 - Start a healthy local scrape (Priority: P1) 🎯 MVP

**Goal**: One Compose command starts the Todo API and Prometheus. Prometheus scrapes `GET /metrics` every 15 seconds at `todo-api:8000`, and both published ports bind to loopback.

**Independent Test**: From a clean checkout, `docker compose up -d --build` makes `http://127.0.0.1:8000/metrics` return 200 and Prometheus answer at `http://127.0.0.1:9090`. `docker compose port` prints `127.0.0.1:8000` and `127.0.0.1:9090`. The `todo-api` target is up within 45 seconds of the API listening, the scrape URL ends in `todo-api:8000/metrics`, and the interval is 15 seconds. A port already in use makes startup fail. No separate Prometheus install and no hand-typed scrape address.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T003 [US1] Add failing tests in `backend/tests/compose/test_monitoring_config.py` that read `compose.yaml` and `deploy/prometheus/prometheus.yml` without starting Docker. Assert the stack has services `todo-api` and `prometheus` only; Prometheus image is `prom/prometheus:v3.13.4`; published ports are `127.0.0.1:8000:8000` and `127.0.0.1:9090:9090` and neither uses `0.0.0.0`; the only scrape job is `todo-api` with target `todo-api:8000`, path `/metrics`, scheme `http`, and `scrape_interval: 15s` both globally and on that job; `rule_files` and `alerting` are absent; the file has no password, token, or todo contents; named volume `prometheus-data` is mounted at `/prometheus` and is not a bind mount of the repository. Tests must fail while those files are missing.

### Implementation for User Story 1

- [ ] T004 [P] [US1] Add `deploy/prometheus/prometheus.yml` with `global.scrape_interval: 15s` and one job `todo-api` whose `metrics_path` is `/metrics`, `scrape_interval` is `15s`, and `static_configs` target is `todo-api:8000`. Do not use `localhost` or `127.0.0.1` as the target. Omit `rule_files`, `alerting`, bearer tokens, and extra headers. Match `specs/003-local-prometheus-compose/contracts/prometheus-scrape.md`.
- [ ] T005 [P] [US1] Add root `compose.yaml` with services `todo-api` and `prometheus` only. Build `todo-api` from `backend/Dockerfile` and publish `127.0.0.1:8000:8000`. Use image `prom/prometheus:v3.13.4`, publish `127.0.0.1:9090:9090`, mount `./deploy/prometheus/prometheus.yml` read-only at `/etc/prometheus/prometheus.yml`, mount named volume `prometheus-data` at `/prometheus`, and set `--storage.tsdb.path=/prometheus` with no retention override and no root user. Do not add a healthcheck `depends_on` that waits for `/metrics`, a SQLite volume, `DATABASE_URL`, Grafana, or Alertmanager. Start command remains `docker compose up -d --build`. Match `specs/003-local-prometheus-compose/contracts/compose-stack.md`.

**Checkpoint**: User Story 1 is functional. The target becomes healthy on a later scrape if Prometheus starts before the API listens. `pytest backend/tests/compose/test_monitoring_config.py` passes the US1 assertions.

---

## Phase 4: User Story 2 - Query throughput, errors, and latency (Priority: P1)

**Goal**: A developer can run documented PromQL for throughput, separate 4xx and 5xx rates, and P50/P95 latency. An empty selector is not the number 0, except the server-error query.

**Independent Test**: After a baseline scrape that already contains a `2xx` series and a `4xx` series, and one scrape after at least 10 further requests, `sum(rate(http_requests_total[1m]))` and `sum(rate(http_requests_total{status=~"4.."}[1m]))` are greater than 0, `sum(rate(http_requests_total{status=~"5.."}[1m])) or vector(0)` is the number 0, and both `histogram_quantile()` queries return a number. A series with only one sample does not produce a rate.

### Tests for User Story 2 ⚠️

- [ ] T006 [US2] Extend `backend/tests/compose/test_monitoring_config.py` so it fails until `README.md` contains the throughput query `sum by (method, handler, status) (rate(http_requests_total[1m]))`, the total `sum(rate(http_requests_total[1m]))`, the client-error query `sum(rate(http_requests_total{status=~"4.."}[1m]))` without `or vector(0)`, the server-error query `sum(rate(http_requests_total{status=~"5.."}[1m])) or vector(0)`, and both `histogram_quantile(0.50, ...)` and `histogram_quantile(0.95, ...)` over `rate(http_request_duration_seconds_bucket[1m])`. Assert the client-error query is not given a zero substitution.

### Implementation for User Story 2

- [ ] T007 [US2] Add a PromQL section to `README.md` with the queries and the one-minute window from `specs/003-local-prometheus-compose/contracts/promql-queries.md`. State that `rate()` needs two samples of the same `method`, `handler`, and `status` series; a newly created counter with only one sample has no earlier value, so Prometheus omits it and that sample is not a per-second rate. Do not add a dashboard file or change series in `backend/src/todo_api/observability/metrics/definitions.py`.

**Checkpoint**: The three questions are documented and match the contract. Querying them still requires the running stack from User Story 1.

---

## Phase 5: User Story 3 - Keep collected samples across restarts (Priority: P2)

**Goal**: Prometheus samples remain queryable after the Prometheus container is stopped, started, or recreated. Deleting `prometheus-data` is the reset. Todo SQLite rows are not part of this persistence.

**Independent Test**: After samples exist, `docker compose restart prometheus` and a recreate without deleting the volume still return a range query for the minute before the restart. `docker compose down -v` starts the next stack with an empty store. Recreating the API container may drop todo rows and must not be treated as a failure.

### Tests for User Story 3 ⚠️

- [ ] T008 [US3] Extend `backend/tests/compose/test_monitoring_config.py` so it fails until `README.md` states that named volume `prometheus-data` survives `docker compose restart` and `docker compose down`, is removed by `docker compose down -v`, and that `todo-api` has no database volume so SQLite rows need not survive an API container restart.

### Implementation for User Story 3

- [ ] T009 [US3] Add that persistence section to `README.md`. Quote the stored-sample rules: the volume is mounted at `/prometheus`; samples survive Prometheus stop, start, and recreation; `docker compose down -v` is the explicit delete; the API database stays the default `sqlite+aiosqlite:///./todo.db` on the container filesystem with no volume. Do not add a SQLite volume to `compose.yaml`.

**Checkpoint**: Restart persistence is documented and the Compose file still has only the Prometheus volume.

---

## Phase 6: User Story 4 - Validate the setup and repeat the check (Priority: P2)

**Goal**: `promtool` accepts the shipped Prometheus file and rejects a file Prometheus would reject. A second developer can follow one written procedure and get the same pass or fail result.

**Independent Test**: `docker compose run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml` exits 0. The same command on a temporary broken file exits non-zero. The written procedure records a `2xx` series and a `4xx` series, waits for one scrape that contains both, sends at least 10 additional requests including successes and one more 4xx on that same series, waits for the next scrape, and queries while `[1m]` still holds both scrapes.

### Tests for User Story 4 ⚠️

- [ ] T010 [US4] Extend `backend/tests/compose/test_monitoring_config.py` so it fails until `README.md` contains `docker compose run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml`, the baseline calls `POST /api/v1/users`, authorized `GET /api/v1/todos`, and unauthenticated `POST /api/v1/todos`, the wait for both a `2xx` and a `4xx` `http_requests_total` series, and the following at least 10 additional requests before the next scrape. Assert the procedure says a one-sample counter is not a rate.

### Implementation for User Story 4

- [ ] T011 [US4] Add the validation command and the verification procedure to `README.md`, in the order in `specs/003-local-prometheus-compose/contracts/verification.md` and `specs/003-local-prometheus-compose/quickstart.md`. Baseline requests are not part of the 10. Do not tell the reader to prove a non-zero rate with two scrapes that both occur after the additional traffic. Do not add the procedure to `.github/workflows/ci.yml`.

**Checkpoint**: Config validation and the full local procedure are written down. Query checks fit the 5-minute budget and the full procedure fits the 15-minute budget.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Confirm the stories still pass together and the application metrics are untouched.

- [ ] T012 Run `pytest` from `backend/`, including `backend/tests/compose/test_monitoring_config.py` and `backend/tests/api/test_metrics.py`. Existing metrics tests must still pass with labels `method`, `handler`, and `status` on `http_requests_total` and `http_request_duration_seconds`, and `method` only on `http_requests_in_progress`.
- [ ] T013 Walk `specs/003-local-prometheus-compose/quickstart.md` and record each result. Run `promtool check config` on the delivered Prometheus file and confirm exit 0. Copy that file to a temporary path, make the copy invalid, run the same command on the copy, and confirm a non-zero exit. Leave the delivered file unchanged and do not start the stack from the copy. Confirm loopback ports `127.0.0.1:8000` and `127.0.0.1:9090`. Start Prometheus before the Todo API is accepting collections, confirm the target is unhealthy, then start the API and confirm the target becomes healthy on a later scrape without restarting Prometheus. With `127.0.0.1:8000` or `127.0.0.1:9090` already in use, confirm `docker compose up` fails with a visible address-in-use error. After the target is healthy, send successful responses and at least one HTTP 4xx response, wait for a scrape that contains both counter series, send at least 10 additional requests that increase those same series and include successes and an HTTP 4xx response, wait for the next scrape, and confirm non-zero throughput, a non-zero 4xx rate, numeric 0 for 5xx, and numeric P50 and P95 over a window that contains both samples. Stop only the Todo API container, confirm Prometheus shows the target unhealthy and the latest scrape error, and confirm previously collected samples remain queryable. Start the API again and confirm the target recovers without restarting Prometheus. Restart the Prometheus container and confirm samples from before the restart remain queryable. Recreate the Prometheus container without deleting named volume `prometheus-data` and confirm those samples still remain. Do not run `docker compose down -v` or otherwise delete `prometheus-data` during this walk.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup. Blocks every user story.
- **User Story 1 (Phase 3)**: Depends on Foundational. No dependency on later stories.
- **User Story 2 (Phase 4)**: Depends on Foundational for the docs test file created in US1. Running the queries requires the US1 stack.
- **User Story 3 (Phase 5)**: Depends on the `prometheus-data` volume from US1. README edits follow US2 because they share `README.md`.
- **User Story 4 (Phase 6)**: Depends on US1 for the files promtool checks, and follows US2 and US3 because it appends to `README.md`.
- **Polish (Phase 7)**: Depends on the stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: First increment. Starts after Phase 2.
- **User Story 2 (P1)**: Query text can be written after US1's test module exists. The live query check uses the US1 stack.
- **User Story 3 (P2)**: Uses the volume US1 mounts. Does not add a second service.
- **User Story 4 (P2)**: Uses the scrape config, the queries, and the volume. The procedure is the cross-story check.

### Within Each User Story

- File-content tests are written and fail before the matching file or README section is added.
- `deploy/prometheus/prometheus.yml` and `compose.yaml` are different files and can be written together after T003.
- README sections are sequential: queries, then persistence, then verification.

### Parallel Opportunities

- T004 and T005 can run together after T003.
- README tasks T007, T009, and T011 edit `README.md` and stay sequential.
- Test-module tasks T003, T006, T008, and T010 edit `backend/tests/compose/test_monitoring_config.py` and stay sequential.

---

## Parallel Example: User Story 1

```bash
# After T003 has defined the failing file assertions:
Task: "Add deploy/prometheus/prometheus.yml with the 15s todo-api:8000 job"
Task: "Add compose.yaml with loopback ports and the prometheus-data volume"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (User Story 1).
3. Stop and validate: both ports on `127.0.0.1`, target up, 15-second scrape of `/metrics`.

### Incremental Delivery

1. Setup and the API image.
2. User Story 1: the stack scrapes.
3. User Story 2: the three PromQL questions are documented, including why one counter sample is not a rate.
4. User Story 3: Prometheus samples survive restart; SQLite does not gain a volume.
5. User Story 4: promtool and the baseline-then-traffic procedure.
6. Polish: pytest and the quickstart walk-through.

### Parallel Team Strategy

After Phase 2, one person can write `deploy/prometheus/prometheus.yml` while another writes `compose.yaml`. Later stories share `README.md` and the test module, so they stay in order.

---

## Notes

- Do not modify `http_requests_total`, `http_request_duration_seconds`, `http_requests_in_progress`, their labels, or `GET /metrics`.
- Published ports stay `127.0.0.1:8000` and `127.0.0.1:9090`. Inside the API container, Uvicorn listens on `0.0.0.0:8000`.
- Prometheus image tag stays `prom/prometheus:v3.13.4`.
- Grafana, alerting, and production deployment are out of scope.
- [P] tasks touch different files and do not depend on each other.
