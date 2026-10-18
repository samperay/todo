# Implementation Plan: Prometheus API Metrics

**Branch**: `002-prometheus-api-metrics` | **Date**: 2026-10-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-prometheus-api-metrics/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Operators scrape one unauthenticated `GET /metrics` endpoint and read traffic, latency, HTTP errors, and in-progress requests in the Prometheus text format. Existing todo and user routes keep their current status codes, bodies, and access rules. Functional requirements and feature scope are unchanged. Grafana, a Prometheus server, alert rules, tracing, and log shipping are not part of this feature. The series are shaped so an operator can chart request rate, latency percentiles, error rate, and saturation from Prometheus.

Observability is a cross-cutting package, `todo_api.observability`. This feature adds only Prometheus metrics under `todo_api.observability.metrics`. `main.py` wires that package to the app. It does not define series or render the exposition itself. Business services, repositories, schemas, and the todo and user routes do not import `prometheus-client`.

The metrics package records three series on a registry owned by that app instance: a completed-request counter, a latency histogram, and an in-progress gauge. `http_requests_total` and `http_request_duration_seconds` use `method`, `handler`, and `status`. `handler` is a matched route template or the single value `unmatched`. `http_requests_in_progress` uses `method` only, with no `handler` and no `status`. Each request increments and decrements that same method series, and the decrement is in `finally`. `http_request_duration_seconds` is a Prometheus histogram with the default prometheus-client buckets. The exposition includes `http_request_duration_seconds_bucket`, `http_request_duration_seconds_sum`, and `http_request_duration_seconds_count`. Prometheus estimates P50 and P95 with `histogram_quantile()` over the bucket series (SC-003). The application does not calculate exact percentiles, and those estimates are not required to fall between the fastest and slowest samples. The scrape path is excluded. A failure while recording or rendering metrics does not change the todo response already produced for that call. `GET /metrics` performs no database query and no external network call. Snapshot rendering runs off the async event loop.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: FastAPI, Pydantic v2, Pydantic Settings, SQLAlchemy 2.x asyncio, aiosqlite, prometheus-client. Uvicorn serves the app. `prometheus-client` is imported only from `todo_api.observability.metrics`.

**Storage**: N/A for this feature. Measurements live in the process registry and reset when the process stops. SQLite remains the local and default test database for existing todo behavior and is unchanged.

**Testing**: pytest, pytest-asyncio, HTTPX. New coverage is an API test module against `create_app`. No new repository or service tests. Existing todo tests stay the regression check that responses are unchanged.

**Target Platform**: Linux server process (local development on macOS is fine)

**Project Type**: web-service (HTTP API only; no UI and no shipped Grafana dashboard)

**Performance Goals**: `GET /metrics` reads the in-process registry only (SC-001). It runs no database query and no external network call. `generate_latest` runs through `asyncio.to_thread`, so synchronous snapshot rendering does not block the async event loop. Recording a request must not change that request's status or body. There is no wall-clock scrape SLA.

**Constraints**: Do not change existing todo or user behavior. Exclude `GET /metrics` from the three series. On the counter and histogram, `handler` is the route template or `unmatched`, never a raw path, resource id, title, description, token, or user id, and `status` is the numeric code as text. `http_requests_in_progress` is labeled only by `method`. Client errors (4xx) and server errors (5xx) stay distinguishable from successes. A failure while recording or publishing metrics must not change the todo response. No new secrets and no new required environment variables. No Prometheus server config, Grafana, Alertmanager, OpenTelemetry, Loki, Tempo, or Compose observability stack.

**Scale/Scope**: One new route and three series. The counter and histogram handler set is the app's route templates plus one `unmatched` bucket. Their cardinality is methods × those templates × the small set of status codes this API returns. The in-progress gauge's cardinality is the set of HTTP methods in flight.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Pre-research | Post-design |
|------|-------------|--------------|-------------|
| I. Layered architecture | API, service, and repository stay separate. Handlers delegate. Database access stays in the repository. Dependencies are injected. | Pass | Pass. Observability is a cross-cutting package wired by `main.py`. Todo and user routes stay thin and do not record metrics. Services and repositories do not import `prometheus-client` or the observability package. The metrics package does not import services, repositories, or schemas. |
| II. Typed contracts | Typed boundaries. Pydantic v2 for structured JSON request and response bodies and for settings. A protocol-specific response MAY use its external representation. SQLAlchemy models stay separate. | Pass | Pass. New functions are typed. Settings stay Pydantic and gain no fields. JSON todo and user bodies stay on Pydantic v2 models. `GET /metrics` returns the Prometheus text exposition format, which constitution 3.1.0 permits. It is not a bypass of Pydantic for an ordinary JSON endpoint. |
| III. Tested features | pytest. API tests cover status and success body for each new or changed endpoint. Service tests when service behavior exists. Repository tests when persistence changes. Default tests use SQLite. | Pass | Pass. `backend/tests/api/test_metrics.py` covers the scrape document, that `GET /metrics` does not call a repository, database session, or external network client, an exact 100-request mix, error classes, histogram buckets, route templates, scrape exclusion, the method-only in-progress gauge, and recording failures. No persistence or service rule is added. Existing API tests guard unchanged todo behavior. |
| IV. RESTful HTTP boundary | Noun resources, matching methods, one domain-error schema. Services raise domain errors. Validation stays the framework error format. | Pass | Pass. `GET /metrics` is an operational read. Todo and user errors are unchanged and still produced by the existing handlers. The contract is [contracts/metrics.openapi.yaml](./contracts/metrics.openapi.yaml). |
| V. Secure configuration | Settings from the environment. No committed secrets. Local defaults are non-secrets. | Pass | Pass. No new setting and no credential on the scrape. Labels and the snapshot body exclude todo contents and tokens. |
| VI. Portable persistence | SQLAlchemy only. SQLite for local and default tests. Engine details stay behind the repository. No new migration requirement. | Pass | Pass. This feature does not touch the database. |
| Stack | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite, pytest. Waiting I/O uses async APIs. CPU-bound work must not block the event loop. | Pass | Pass. `prometheus-client` is an added library, not a replacement of the stack. `GET /metrics` does not query the database or call the network. Snapshot rendering is synchronous CPU work and runs through `asyncio.to_thread`. Counter updates are in-process. |
| Workflow | New HTTP behavior ships with HTTP tests. Shared exception handlers stay the error policy. | Pass | Pass. No new domain error and no one-off todo error body. Instrumentation failures are contained in the metrics middleware. |

No gate fails.

## Project Structure

### Documentation (this feature)

```text
specs/002-prometheus-api-metrics/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml
├── src/
│   └── todo_api/
│       ├── main.py                              # wiring only
│       └── observability/
│           ├── __init__.py
│           └── metrics/
│               ├── __init__.py                  # wiring exports used by main.py
│               ├── registry.py                  # per-app CollectorRegistry
│               ├── definitions.py               # counter, histogram, gauge
│               ├── middleware.py                # HTTP instrumentation
│               └── endpoint.py                  # Prometheus exposition for GET /metrics
└── tests/
    └── api/
        └── test_metrics.py
```

**Structure Decision**: Backend-only addition. `observability/` is the boundary for cross-cutting signals. This feature creates only the `metrics/` package above. It does not add modules for tracing, structured logging, OpenTelemetry, or a future exporter. `registry.py` builds a `CollectorRegistry` that is not the process-global registry. `definitions.py` declares `http_requests_total`, `http_request_duration_seconds`, and `http_requests_in_progress` on that registry. `middleware.py` records the counter and histogram after the response, using `method`, `handler`, and `status`. It increments and decrements `http_requests_in_progress` on the same `method` label, with the decrement in `finally`. `endpoint.py` turns the registry into exposition bytes and does not touch the database or the network. `main.py` constructs the registry, stores it on `app.state`, adds the middleware, and registers `GET /metrics`. Todo routes, user routes, schemas, services, repositories, and `db/` stay as they are and do not import `prometheus-client`.

## Complexity Tracking

No constitution violations require justification.
