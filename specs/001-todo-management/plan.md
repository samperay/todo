# Implementation Plan: Basic Todo Management

**Branch**: `001-todo-management` | **Date**: 2026-10-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-todo-management/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Identified people manage their own todos: create, list, retrieve, partial update of title and description, mark completed, mark incomplete, and permanent delete. Another person's id is reported as not found. Overlapping writes do not return a conflict; the later committed write replaces the earlier one for the fields it sets.

The backend is a FastAPI service on Python 3.12 or newer. Route handlers stay thin and receive an identified user plus a service through dependency injection. Pydantic v2 schemas are the only request and response models. SQLAlchemy 2.x models are persistence-only. Services own the rules and do not mention the database engine. Repositories own database access. Local development and the default tests use SQLite. Startup creates the schema with `Base.metadata.create_all()`. There is no migration toolchain in this version.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: FastAPI, Pydantic v2, Pydantic Settings, SQLAlchemy 2.x asyncio, aiosqlite

**Storage**: SQLite for local development and the default test configuration. The URL comes from settings. A later engine change must not require service or API edits.

**Testing**: pytest, pytest-asyncio, HTTPX. Service tests use a stand-in repository. Repository and API tests use SQLite.

**Target Platform**: Linux server process (local development on macOS is fine)

**Project Type**: web-service (HTTP API only; no UI in this feature)

**Performance Goals**: A list of 100 todos for one person returns completely, newest first. No separate product latency budget was set in the spec. Single-item calls and that list should stay interactive on local SQLite (target p95 under 300ms, excluding cold start).

**Constraints**: Layered dependencies only (API → service → repository → database). Handlers contain no business rules and no SQL. Request and response models are Pydantic. Persistence models are SQLAlchemy. Services and API modules contain no engine, dialect, or driver details. Schema setup for this version is `Base.metadata.create_all()` in the database infrastructure, not Alembic. Secrets come from the environment. The local SQLite URL may be a non-secret default. Unidentified callers are rejected before any write. Cross-owner access returns the same not-found outcome as an unknown id. No optimistic concurrency and no conflict warning.

**Scale/Scope**: One API, two persisted entities (person and todo). Success checks use two people and 100 todos for one person. No pagination, search, or shared lists.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Pre-research | Post-design |
|------|-------------|--------------|-------------|
| I. Layered architecture | API, service, and repository stay separate. Handlers delegate. Database access stays in the repository. Dependencies are injected. | Pass | Pass. Routes depend on a service. The service depends on a repository interface. The session and repository are built in API dependencies, not inside handlers. |
| II. Typed contracts | Typed boundaries. Pydantic v2 for requests, responses, and settings. SQLAlchemy 2.x mappings for rows. The two model types stay separate. | Pass | Pass. `schemas/` and `db/models.py` do not share classes. |
| III. Tested features | pytest. Service unit tests without a live database when the repository can be substituted. Repository tests on the configured database. Default tests use SQLite. API tests cover status, validation, and success bodies. | Pass | Pass. Layout under `backend/tests/` matches those three layers. See [quickstart.md](./quickstart.md). |
| IV. RESTful HTTP boundary | Noun resources, matching methods, one domain-error schema. Services raise domain errors. Validation uses the framework error format and leaks no stack, SQL, or secrets. | Pass | Pass. Contract in [contracts/todos.openapi.yaml](./contracts/todos.openapi.yaml). `TodoNotFound` becomes 404 in the API layer. Pydantic failures stay 422. |
| V. Secure configuration | Settings from the environment. No committed secrets. Local defaults are allowed when they are not secrets. Production fails startup when a required secret is missing. | Pass | Pass. The local database default is a SQLite file URL, not a credential. Only a token hash is stored. The plaintext token is returned once and is not logged. |
| VI. Portable persistence | SQLAlchemy is the only persistence abstraction. SQLite is the local and default test database. Engine details stay in the repository and infrastructure. Business logic does not use SQLite-specific features. This phase may use `metadata.create_all()` and does not require migrations. | Pass | Pass. `create_all` runs from database infrastructure at startup. Services depend on a repository interface. Queries use portable SQLAlchemy constructs. |
| Stack | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite, pytest. Waiting I/O uses async APIs when the library supports them. PostgreSQL is optional later, not required now. | Pass | Pass. Runtime driver is aiosqlite. No Alembic project. |
| Workflow | New behavior ships with service, repository, and HTTP tests. Exceptions use shared handlers. | Pass | Pass. No one-off error bodies in route functions. |

No gate fails. No exception is recorded in Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-management/
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
│       ├── main.py
│       ├── core/
│       │   └── config.py
│       ├── api/
│       │   ├── deps.py
│       │   ├── errors.py
│       │   └── routes/
│       │       ├── users.py
│       │       └── todos.py
│       ├── schemas/
│       │   ├── errors.py
│       │   ├── user.py
│       │   └── todo.py
│       ├── services/
│       │   ├── errors.py
│       │   └── todo_service.py
│       ├── repositories/
│       │   └── todo_repository.py
│       └── db/
│           ├── session.py
│           ├── schema.py
│           └── models.py
└── tests/
    ├── unit/
    ├── integration/
    └── api/
```

**Structure Decision**: Backend-only web service under `backend/`. There is no frontend in this feature. `schemas/` holds Pydantic models. `db/models.py` holds SQLAlchemy models. `db/schema.py` calls `Base.metadata.create_all()` and is the only schema initializer. `api/routes/` is the HTTP boundary. `services/` holds rules and imports neither the engine nor the models' query API. `repositories/` holds queries. `api/deps.py` is the only place that wires a session, repository, and service into a handler.

## Complexity Tracking

No constitution violations require justification.
