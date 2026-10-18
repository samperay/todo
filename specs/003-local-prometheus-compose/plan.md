# Implementation Plan: Local Prometheus Monitoring

**Branch**: `feature/prometheus-server-integration` | **Date**: 2026-10-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-local-prometheus-compose/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Developers start the existing Todo API and Prometheus with one Docker Compose command. Prometheus scrapes the existing `GET /metrics` endpoint every 15 seconds through Compose DNS, on loopback-only published ports. Prometheus samples survive container restart and recreation in a named volume. Todo SQLite data does not. Grafana, alerting, and production deployment stay out of scope.

No application series, labels, routes, or settings change. The API image packages the current `todo_api.main:app` entry point. Configuration validity is checked with `promtool`. Documented PromQL covers throughput, separate 4xx and 5xx rates, and P50/P95 latency. Verification first stores a baseline scrape that already contains both a successful-response counter and an HTTP 4xx counter. It then sends at least 10 more requests, including successes and at least one 4xx, waits for the next scrape, and reads `rate()` across those two samples. A counter series seen only once has no earlier value, so `rate()` cannot describe it.

## Technical Context

**Language/Version**: Python 3.12+ for the existing API. The API image uses `python:3.12-slim`. Prometheus is `prom/prometheus:v3.13.4` (LTS, 2026-09-29), which includes `promtool`. That tag is published on Docker Hub for `linux/amd64` and `linux/arm64`.

**Primary Dependencies**: Existing FastAPI, Pydantic v2, Pydantic Settings, SQLAlchemy 2.x asyncio, aiosqlite, prometheus-client, and Uvicorn. Docker Compose v2 is a developer prerequisite. No new Python dependency. No Grafana and no Alertmanager.

**Storage**: Prometheus TSDB on the named volume `prometheus-data`, mounted at `/prometheus`. The API keeps the default `sqlite+aiosqlite:///./todo.db` inside the container filesystem. That file is not on a volume. SQLite persistence is out of scope.

**Testing**: pytest for the committed Compose file and Prometheus file: loopback publishes, 15-second interval, `todo-api:8000` target, `/metrics` path, the Prometheus volume, and the absence of Grafana, alert rules, and secrets. `promtool check config` is the validation command developers run. The existing GitHub Actions jobs do not need Docker. Existing `backend/tests/api/test_metrics.py` remains the guard that series and labels are unchanged.

**Target Platform**: A developer machine with Docker Compose. Containers are Linux. The host publish addresses are loopback on macOS or Linux.

**Project Type**: Local web-service runtime. One API process and one Prometheus process. No UI product and no production deployment.

**Performance Goals**: Both published endpoints answer within 2 minutes of `docker compose up -d --build` (SC-001). The API target is healthy within 45 seconds of the API listening, at a 15-second interval (SC-002). Baseline, traffic, one post-traffic scrape, and the PromQL checks finish within 5 minutes of the target becoming healthy (SC-003). The full procedure, including a Prometheus restart, finishes within 15 minutes (SC-005).

**Constraints**: Do not change `http_requests_total`, `http_request_duration_seconds`, or `http_requests_in_progress`, their labels, or `GET /metrics`. Scrape that path without a bearer token. Publish `127.0.0.1:8000` and `127.0.0.1:9090` only. Inside the API container, Uvicorn listens on `0.0.0.0:8000` so the Compose network can reach it. Prometheus uses the hostname `todo-api`, not `localhost`. No secrets in committed files. No Grafana service, dashboard file, `rule_files`, or Alertmanager config. Default Prometheus retention stays in place.

**Scale/Scope**: Two Compose services, one scrape job, one named volume, and the documented queries and verification steps. One developer machine.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Pre-research | Post-design |
|------|-------------|--------------|-------------|
| I. Layered architecture | API, service, and repository stay separate. Handlers delegate. Database access stays in the repository. | Pass | Pass. No route, service, or repository change. The image starts the existing `create_app()` path in `todo_api.main`. |
| II. Typed contracts | Pydantic v2 for JSON bodies and settings. Protocol-specific responses may use their external form. | Pass | Pass. No new JSON endpoint and no settings field. `GET /metrics` stays the Prometheus text document from Phase 002. |
| III. Tested features | pytest. API tests for changed endpoints. Service and repository tests only when those layers change. Default tests use SQLite. | Pass | Pass. New pytest covers the committed runtime files. No service or repository behavior is added. Existing metrics tests guard the series. `promtool` is the local validity check and is not a new CI job. |
| IV. RESTful HTTP boundary | Noun resources, matching methods, one error schema. | Pass | Pass. No new route and no error-schema change. |
| V. Secure configuration | Environment-backed settings. No committed secrets. Local defaults are non-secrets. | Pass | Pass. Published ports bind to loopback. The scrape has no credential. Compose and Prometheus files contain no passwords, tokens, or todo contents. `DATABASE_URL` stays the default SQLite URL. |
| VI. Portable persistence | SQLAlchemy only. SQLite for local and default tests. Engine details stay behind the repository. | Pass | Pass. The API container does not gain a database volume or a second engine. Prometheus TSDB is collector storage, not application persistence. |
| Stack | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite, pytest. | Pass | Pass. Docker and Prometheus are the local collector runtime. They do not replace the application stack. |
| Workflow | New behavior ships with tests. Shared exception handlers stay the error policy. | Pass | Pass. No new domain error. |

No gate fails.

## Project Structure

### Documentation (this feature)

```text
specs/003-local-prometheus-compose/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
compose.yaml                              # todo-api and prometheus; loopback publishes
backend/Dockerfile                        # packages the existing API; listens on 0.0.0.0:8000
backend/.dockerignore                     # keeps the local venv, db, and caches out of the image
deploy/prometheus/prometheus.yml          # one job, 15s interval, target todo-api:8000
backend/tests/compose/test_monitoring_config.py
README.md                                 # short local-monitoring section pointing at the commands
```

Existing application modules stay as they are. The entry point remains `backend/src/todo_api/main.py` (`app = create_app()`). Metrics stay in `backend/src/todo_api/observability/metrics/`. Settings stay in `backend/src/todo_api/core/config.py` with the default SQLite URL.

**Structure Decision**: Runtime files live at the repository root and under `deploy/prometheus/` because Compose is a developer workflow, not an API-layer module. The image build context is `backend/`, which already holds `pyproject.toml` and `src/`. Tests that read those runtime files live under `backend/tests/` so the existing pytest configuration picks them up. The Phase 002 metrics contract is referenced and not copied or changed.

## Complexity Tracking

No constitution violations.
