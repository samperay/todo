# Tasks: Prometheus API Metrics

**Input**: Design documents from `/specs/002-prometheus-api-metrics/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included. Constitution III requires pytest coverage, and a feature is not done until tests fail for the missing behavior and then pass. Write each story's tests first and confirm they fail before implementing that story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web service**: `backend/src/todo_api/`, `backend/tests/`
- Paths match `specs/002-prometheus-api-metrics/plan.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add the Prometheus client library. The FastAPI app, tests, and todo routes already exist.

- [x] T001 Add `prometheus-client` to the runtime dependencies in `backend/pyproject.toml`. Do not add a Grafana dashboard, a Prometheus server config, Alertmanager, OpenTelemetry, Loki, Tempo, or a new environment variable.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Observability package, per-app registry, and middleware shell that every story records into

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Create `backend/src/todo_api/observability/__init__.py` and `backend/src/todo_api/observability/metrics/`. Put a factory that returns a new `prometheus_client.CollectorRegistry`, never the process-global registry, in `backend/src/todo_api/observability/metrics/registry.py`. Add a pure ASGI middleware in `backend/src/todo_api/observability/metrics/middleware.py`, bound to that registry, that forwards the request and returns the app's response unchanged. Export only the wiring helpers `main.py` needs from `backend/src/todo_api/observability/metrics/__init__.py`. Do not define series or a route in this task, and do not add tracing, logging, or other observability modules.
- [x] T003 In `backend/src/todo_api/main.py`, build that registry inside `create_app`, store it on `app.state`, and add the middleware around the existing app. Keep `prometheus-client` imports inside `backend/src/todo_api/observability/metrics/`. Leave user routes, todo routes, schemas, services, repositories, and settings unchanged.

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Scrape API metrics (Priority: P1) 🎯 MVP

**Goal**: An operator can scrape a Prometheus text snapshot without a person's bearer token, and existing todo actions keep their current results.

**Independent Test**: `GET /metrics` returns 200 and a Prometheus text document that includes the three series names and reports no completed todo traffic. That request does not call a Todo or User repository, a database session, or an external network client. One existing todo action still returns its current status and body. Repeating the scrape does not add scrape traffic.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T004 [US1] Add failing API tests in `backend/tests/api/test_metrics.py` for `GET /metrics`: no bearer token; status 200; content type `text/plain; version=0.0.4; charset=utf-8`; body is Prometheus text containing `http_requests_total`, `http_request_duration_seconds`, and `http_requests_in_progress`; a scrape before todo traffic does not report completed todo requests; one existing todo or user call keeps its current status and body; a repeated scrape of `/metrics` does not add a completed-request sample for that path. While handling `GET /metrics`, assert that the call does not invoke a Todo or User repository, database or session access, or an external HTTP or network client. Do not assert a wall-clock limit.

### Implementation for User Story 1

- [x] T005 [US1] Register the three series on the app registry in `backend/src/todo_api/observability/metrics/definitions.py`: counter `http_requests_total` with help `Completed HTTP requests.` and labels `method`, `handler`, `status`; histogram `http_request_duration_seconds` with help `HTTP request latency in seconds.`, the same labels, and library default buckets; gauge `http_requests_in_progress` with help `HTTP requests currently in progress.` and label `method` only. The gauge MUST NOT have a `handler` or `status` label. On the counter and histogram, `handler` is the API action and `status` is the response outcome.
- [x] T006 [US1] Add exposition generation in `backend/src/todo_api/observability/metrics/endpoint.py`. `GET /metrics` goes to that endpoint, reads only the application `CollectorRegistry`, and calls `generate_latest` through `asyncio.to_thread`. It must not call a service, repository, database session, or external network client. Return the bytes with the prometheus-client exposition content type and no Pydantic response model. Register the unauthenticated route from `backend/src/todo_api/main.py` by calling that helper only. In `backend/src/todo_api/observability/metrics/middleware.py`, skip all observation when the path is `/metrics` or `/metrics/`. Do not add a wall-clock limit.

**Checkpoint**: User Story 1 is functional and testable on its own

---

## Phase 4: User Story 2 - Monitor traffic and HTTP errors (Priority: P1)

**Goal**: Completed requests are counted by method, route template, and numeric status, with client errors and server errors distinguishable from successes.

**Independent Test**: A known mix of successful todo requests, 401/404/422 responses, and one server error matches `http_requests_total`. Two different todo ids share one handler. Titles, descriptions, and tokens are absent. A recording failure does not change the todo response.

### Tests for User Story 2 ⚠️

- [x] T007 [US2] Extend `backend/tests/api/test_metrics.py` with a failing test that sends exactly 100 completed non-scrape requests in a fixed mix: 80 successes, 15 client errors covering 401, 404, and 422, and 5 server errors raised only from the test app. Assert the exact `http_requests_total` value for every `method`, `handler`, and `status` in that mix, including when requests in the set finish together. Client statuses are in `400–499` and server statuses are in `500–599`, as queries over `status`, not separate series. Within the 80 successes, two todo ids share `handler="/api/v1/todos/{todo_id}"`. An unmatched path uses `handler="unmatched"`. No raw path is a handler. The body must not contain the todo title, description, bearer token, user id, or raw resource id. A further request, not one of the 100, must still return its previous todo status and body if incrementing the counter raises.

### Implementation for User Story 2

- [x] T008 [US2] In `backend/src/todo_api/observability/metrics/middleware.py`, after a non-scrape request finishes, increment `http_requests_total` once with `method` set to the HTTP method, `handler` set to the matched route's full path template or `unmatched`, and `status` set to the numeric status as text. The allowed handlers are the application's route templates plus `unmatched`. Take label values only from the method, the template or `unmatched`, and the status; never from the JSON body, the raw path, or the `Authorization` header. The value inside `{todo_id}` is never a label. If the app raises before a response exists, record status `500` and re-raise. If recording raises, still return the response the app produced.

**Checkpoint**: Traffic and error counts work without changing User Story 1's scrape contract

---

## Phase 5: User Story 3 - Monitor request latency (Priority: P1)

**Goal**: Each completed API request, including errors, contributes its duration so a median and a slow tail can be read.

**Independent Test**: The same completed requests that increment the counter each add one histogram observation with the same labels. The exposition includes default buckets, count, and sum so `histogram_quantile()` can estimate P50 and P95. Scrapes add none. The test does not assert that an estimated percentile lies between the fastest and slowest sample.

### Tests for User Story 3 ⚠️

- [x] T009 [US3] Extend `backend/tests/api/test_metrics.py` with failing tests that each completed non-scrape request, including a client error and a server error, adds one `http_request_duration_seconds` observation with the same `method`, `handler`, and `status` as its `http_requests_total` increment. Assert the exposition includes `http_request_duration_seconds_bucket` with the default prometheus-client buckets, plus `http_request_duration_seconds_sum` and `http_request_duration_seconds_count`. Do not calculate P50 or P95 in the test, and do not assert that a `histogram_quantile()` estimate lies between the fastest and slowest observed sample. Scrapes of `/metrics` and `/metrics/` add no histogram observation.

### Implementation for User Story 3

- [x] T010 [US3] In `backend/src/todo_api/observability/metrics/middleware.py`, observe `http_request_duration_seconds` with the elapsed seconds from when the middleware saw the request until the response finished, using the same `method`, `handler`, and `status` labels as the counter increment for that request. Keep the default prometheus-client buckets so the scrape exposes `http_request_duration_seconds_bucket`, `http_request_duration_seconds_sum`, and `http_request_duration_seconds_count`. Do not observe scrape paths. Do not calculate P50 or P95 in the application, and do not store raw durations to produce an exact percentile.

**Checkpoint**: Latency can be charted from the same scrape as traffic and errors

---

## Phase 6: User Story 4 - Monitor active requests (Priority: P2)

**Goal**: The scrape shows how many API requests are in progress, and that count falls when they finish, fail, or the caller disconnects.

**Independent Test**: While held-open test requests are in flight, `http_requests_in_progress` equals that number. After they finish or fail, the gauge returns to its previous level. The scrape itself is not an active request.

### Tests for User Story 4 ⚠️

- [x] T011 [US4] Extend `backend/tests/api/test_metrics.py` with failing tests that hold 20 requests open on a route added only in that test, not in `backend/src/todo_api/api/routes/`. During that window, `http_requests_in_progress` labeled only by that HTTP method equals 20. The series has no `handler` label and no `status` label. After those requests succeed, fail, or are cancelled, that same method series is back to its previous level. `GET /metrics` does not increase the gauge. A scrape taken while those requests are open does not change their later todo or test-route results.

### Implementation for User Story 4

- [x] T012 [US4] In `backend/src/todo_api/observability/metrics/middleware.py`, increase `http_requests_in_progress` by one for the request's HTTP method when a non-scrape request enters. Decrease that same method-labelled series by one in `finally` when the request finishes, fails, or the caller disconnects, including when recording the completion counter or histogram raises. Do not add a `handler` or `status` label to this gauge. A scrape of `/metrics` or `/metrics/` must not enter this count.

**Checkpoint**: Saturation is visible without changing completed-request or latency totals

---

## Phase 7: User Story 5 - Provide metrics for operational dashboards (Priority: P2)

**Goal**: The published series are sufficient for request rate, latency percentiles, error rate, and in-progress panels. No dashboard product or dashboard file is added.

**Independent Test**: After traffic, the snapshot contains the series and labels used by the queries in `specs/002-prometheus-api-metrics/contracts/metrics-catalog.md`, and the repository still has no dashboard artifact.

### Tests for User Story 5 ⚠️

- [x] T013 [US5] Extend `backend/tests/api/test_metrics.py` with a failing test that, after a mix of successful and failed todo requests, the snapshot includes `http_requests_total` and `http_request_duration_seconds` bucket samples labeled `method`, `handler`, and `status`, and `http_requests_in_progress` labeled only by `method`. The gauge series must not contain `handler` or `status`. Assert the help lines `Completed HTTP requests.`, `HTTP request latency in seconds.`, and `HTTP requests currently in progress.`

### Implementation for User Story 5

- [x] T014 [US5] Check that series names, help strings, types, and label sets in `backend/src/todo_api/observability/metrics/definitions.py` match `specs/002-prometheus-api-metrics/contracts/metrics-catalog.md`. `http_requests_in_progress` has the `method` label only. Change a definition only if it differs. Do not add a Grafana JSON file, a Prometheus scrape config, Alertmanager, OpenTelemetry, or a domain counter such as todos created.

**Checkpoint**: All five stories are independently testable from the scrape endpoint

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Confirm the feature does not disturb existing todo behavior and passes the repo checks

- [x] T015 Run `pytest` from `backend/` and confirm the scenarios in `specs/002-prometheus-api-metrics/quickstart.md`, including the existing todo and user tests, pass with no status or response-body changes. Do not assert a wall-clock limit for `GET /metrics`.
- [x] T016 [P] Run `ruff check .`, `ruff format --check .`, and `mypy src` from `backend/` and fix any new findings in `backend/src/todo_api/observability/`, `backend/src/todo_api/main.py`, and `backend/tests/api/test_metrics.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 8)**: Depends on the user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational. No dependency on later stories. This is the MVP.
- **User Story 2 (P1)**: Starts after User Story 1, because the tests read counts from `GET /metrics`. Does not require latency or the in-progress gauge.
- **User Story 3 (P1)**: Starts after User Story 2, because each histogram observation must share labels with that request's counter increment. Does not require the in-progress gauge.
- **User Story 4 (P2)**: Starts after User Story 1's middleware and scrape exist. Does not require the counter or histogram to be correct, but it edits the same middleware, so implement it after User Story 3 to avoid conflicting edits.
- **User Story 5 (P2)**: Starts after User Stories 2, 3, and 4. It checks the four signals together and does not add a new measurement.

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Series definitions exist before the scrape route returns them (User Story 1)
- The counter exists before the histogram copies its labels (User Stories 2 and 3)
- The gauge decrement stays in `finally` so a recording failure cannot leave it raised (User Story 4)

### Parallel Opportunities

- T016 can run beside T015: one is the test suite, the other is lint and type checks, and neither depends on the other's output
- No other task is marked [P]. Story work shares `backend/src/todo_api/observability/metrics/middleware.py` and `backend/tests/api/test_metrics.py`, so those tasks stay sequential

---

## Parallel Example: Polish

```bash
# From backend/, after User Story 5:
pytest
ruff check . && ruff format --check . && mypy src
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: `GET /metrics` is Prometheus text, scrapes are excluded, and one existing todo action is unchanged

### Incremental Delivery

1. Setup + Foundational → registry and middleware shell
2. User Story 1 → scrape endpoint (MVP)
3. User Story 2 → traffic and HTTP error counts
4. User Story 3 → latency histogram
5. User Story 4 → in-progress gauge
6. User Story 5 → catalog alignment for the four operational dashboard queries
7. Polish → full pytest, ruff, and mypy

### Parallel Team Strategy

One implementer should own `backend/src/todo_api/observability/metrics/` and `backend/tests/api/test_metrics.py` through the stories, in phase order. A second person can run T016 only after those files stop changing.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence


## Validation record (2026-10-18)

The initial implementation already contained the dependency, observability package,
registry, middleware, definitions, and scrape response, but only two scrape tests.
Existing behavior was audited in dependency order; tests for behavior already present
passed on their first run. No historical failing-test run is claimed for that code.

New regression tests failed before the corresponding fixes:

- US2: a gauge label lookup exception escaped and replaced the existing todo result.
  Moving lookup inside the instrumentation exception boundary restored the response.
- US3: a counter increment failure skipped the histogram observation. Independent
  exception boundaries now isolate the two measurements.
- US3: latency included background work after the final response body (90 seconds
  instead of 2 on a controlled clock). Timing now ends after the final body is sent.
- US4: 20 cancelled requests without responses incorrectly became 20 completed 500s.
  Cleanup still decrements the gauge, without inventing completed responses.

The route registration helper now lives in the metrics package; `main.py` only wires
it. The dependency minimum is 0.25 because the implementation imports the explicit
0.0.4 exposition content type exported by that version.

Validated task groups:

- T001–T006: isolated registries, credential-free text snapshot, no initial completed
  samples, repeated scrape exclusion, unchanged user result, explicit repository,
  session/database and HTTP/network guards, and rendering off the event loop.
- T007–T008: exact concurrent 100-request mix (80 successes, 15 client errors covering
  401/404/422, 5 test-only server errors), template grouping for two todo ids,
  unmatched-path grouping, private-value exclusion, and recording failure isolation.
- T009–T010: histogram counts match completed-request labels, including errors;
  default buckets, sum/count, both scrape path exclusions, and response-finish timing.
- T011–T012: 20 held requests across success, failure, and cancellation; method-only
  labels, unchanged results, gauge cleanup, and counter/histogram failure isolation.
- T013–T014: catalog names, help text, types, and exact label sets verified. No
  dashboard, collector/server configuration, or domain instrumentation added.
- T015: `pytest` from `backend/`: **65 passed**, including all existing user/todo tests
  and the automated scenarios in `quickstart.md`.
- T016: `ruff check .`, `ruff format --check .`, and `mypy src` from `backend/`:
  **passed**. `git diff --check`: **passed**.
