<!--
Sync Impact Report
- Version change: 2.0.0 → 3.0.0
- Modified principles:
  - III. Tested Features: migration-test obligation removed so the principle
    matches the initial phase, where migrations are not required
  - VI. Portable Persistence: Alembic requirement removed; schema MAY be
    created with SQLAlchemy metadata.create_all(); business logic MUST NOT
    depend on SQLite-specific functionality
- Added sections: none
- Removed sections:
  - Mandatory Alembic migrations in Technology Stack and Development Workflow
- Follow-up TODOs: none
-->

# Todo Constitution

## Core Principles

### I. Layered Architecture

The backend MUST separate the API, service, and persistence layers.
Dependencies flow inward: API depends on services, services depend on
repositories, and repositories depend on the database.

- The API layer MUST handle HTTP concerns only: routing, request and
  response models, status codes, and authentication context.
- Route handlers MUST NOT contain business logic. They MUST delegate to
  the service layer.
- The service layer MUST own business rules, orchestration, and
  domain decisions.
- The repository layer MUST own all database access. Services and route
  handlers MUST NOT issue queries or manage sessions directly.
- Cross-layer dependencies MUST be supplied through dependency injection.
  Concrete implementations MUST NOT be constructed inside the layer that
  consumes them when an injectable boundary exists.

Rationale: A fixed dependency direction keeps HTTP, domain rules, and
persistence independently testable and replaceable.

### II. Typed Contracts

Public and internal boundaries MUST be explicit and statically typed.

- Every function, method, and module-level variable that crosses a layer
  boundary MUST have type hints. Untyped public signatures are not
  acceptable.
- Request bodies, response bodies, and settings models MUST use
  Pydantic v2.
- Persistence models MUST use SQLAlchemy 2.x typed mappings. Pydantic
  models and SQLAlchemy models MUST remain separate types.
- Type checkers and the test suite MUST be able to import the application
  without ignoring missing annotations on new code.

Rationale: Typed contracts catch shape errors before runtime and keep API
schemas independent of the database schema.

### III. Tested Features

Every feature MUST ship with automated tests. A change that adds or
alters behavior without tests is incomplete.

- Tests MUST use pytest.
- Service behavior MUST be covered by unit tests that do not require a
  live database when the repository can be substituted.
- Repository behavior MUST be covered by tests that run against the
  configured database. Local and default test runs MUST use SQLite.
- API tests MUST exercise status codes, validation errors, and the
  success payload for each added or changed endpoint.
- A feature is not done until its tests fail for the missing behavior
  and pass once the behavior exists.

Rationale: Required tests are the enforcement mechanism for the layering
and contract rules above.

### IV. RESTful HTTP Boundary

The public API MUST follow REST resource design and a single exception
policy.

- Resources MUST be nouns addressed by stable paths. Unsafe operations
  MUST use the HTTP method that matches the intent (GET, POST, PUT,
  PATCH, DELETE).
- Success and error responses MUST use consistent status codes and a
  single error response schema.
- Domain and persistence exceptions MUST be translated to HTTP errors in
  the API layer. Services MUST raise domain errors, not HTTP exceptions,
  unless a documented boundary exception applies.
- Validation failures MUST return the framework's structured error
  format without leaking stack traces, SQL, or secret values.

Rationale: One error shape and a strict HTTP boundary make clients and
tests predictable.

### V. Secure Configuration

Runtime configuration MUST come from the environment. Secrets MUST NOT
be hardcoded.

- Application settings MUST be loaded from environment variables through
  a typed settings object.
- Passwords, API keys, tokens, and database credentials MUST NOT appear
  in source code, fixtures committed to the repository, or log output.
- Default values MAY exist for local development only when they are not
  secrets. Production MUST fail startup when a required secret is missing.
- Configuration files that are safe to commit MUST reference variable
  names, not secret values.

Rationale: Environment-backed settings keep deployments portable and
prevent accidental secret disclosure.

### VI. Portable Persistence

SQLAlchemy 2.x MUST be the only persistence abstraction. The database
engine is a deployment choice, not a business-logic dependency.

- SQLite MUST be the default database for local development and for the
  default test configuration.
- The database URL MUST come from environment-backed configuration.
  Introducing another database later MUST NOT require changes to service
  or API code.
- Persistence MUST remain behind the repository layer. Database-specific
  types, SQL dialects, session handling, and driver details MUST stay
  inside the repository and infrastructure boundary. They MUST NOT appear
  in service or API modules.
- Business logic MUST NOT depend on SQLite-specific functionality.
- During the initial development phase, database migrations are not
  required. The development schema MAY be initialized with SQLAlchemy
  metadata.create_all().

Rationale: SQLAlchemy isolates the engine so local SQLite can later be
replaced through configuration without rewriting business logic.

## Technology Stack

The backend MUST use the following stack. Replacements require a
constitution amendment.

- Language: Python 3.12 or newer.
- HTTP framework: FastAPI.
- Validation and settings: Pydantic v2.
- Persistence: SQLAlchemy 2.x.
- Local development database: SQLite.
- Tests: pytest.
- I/O that waits on the network or database MUST use async APIs when the
  chosen library provides a supported async interface. CPU-bound work
  MUST NOT block the event loop; it MUST run in a thread or process pool
  or move out of the request path.

PostgreSQL is permitted as a future engine. It is not a mandatory part of
the stack.

## Development Workflow

- New behavior starts from a feature specification and lands with tests
  for the service rule, the repository query when persistence changes,
  and the HTTP contract when an endpoint changes.
- During the initial development phase, schema setup MAY use SQLAlchemy
  metadata.create_all(). A migration toolchain is not required.
- Pull requests MUST confirm the change respects layer boundaries, type
  hints, the error schema, the environment-only secret rule, and the
  ban on database-specific details in the service and API layers.
- Exceptions that escape a route MUST be handled by the shared exception
  handlers. New error cases MUST extend that policy rather than formatting
  a one-off response in the handler.

## Governance

This constitution supersedes informal practice for the backend. When a
spec, plan, or implementation conflicts with these principles, the
constitution wins until it is amended.

- Amendments MUST be proposed as a change to this file, with a version
  bump and a short rationale in the Sync Impact Report.
- Versioning follows semantic versioning:
  - MAJOR: a principle is removed or redefined in a way that invalidates
    existing governed practice.
  - MINOR: a new principle or materially expanded rule is added.
  - PATCH: wording clarifications that do not change obligations.
- Compliance is reviewed when a feature specification, plan, or pull
  request is written. Reviewers MUST reject changes that place business
  logic in route handlers, bypass the repository for database access,
  leak database-specific details into the service or API layer, omit
  tests for a new feature, or commit secrets.
- Runtime guidance for contributors lives in this file. Template copies
  under `.specify/templates/` MUST NOT be edited to record project rules.

**Version**: 3.0.0 | **Ratified**: 2026-10-02 | **Last Amended**: 2026-10-02
