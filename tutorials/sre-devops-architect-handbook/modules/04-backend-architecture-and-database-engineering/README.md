# Module 04 — Backend Architecture And Database Engineering

**Scope:** SQLite transactions and rollback.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Backend Architecture And Database Engineering**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **SQLite transactions and rollback**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [04.01-fastapi-request-lifecycle](lessons/04.01-fastapi-request-lifecycle.md) | FastAPI request lifecycle | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.02-route-versus-service-versus-repository](lessons/04.02-route-versus-service-versus-repository.md) | Route versus service versus repository | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.03-pydantic-v2-typed-contracts](lessons/04.03-pydantic-v2-typed-contracts.md) | Pydantic v2 typed contracts | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.04-authentication-and-authorization-boundaries](lessons/04.04-authentication-and-authorization-boundaries.md) | Authentication and authorization boundaries | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.05-sqlalchemy-sessions-and-transactions](lessons/04.05-sqlalchemy-sessions-and-transactions.md) | SQLAlchemy sessions and transactions | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.06-sqlite-locking-and-concurrency](lessons/04.06-sqlite-locking-and-concurrency.md) | SQLite locking and concurrency | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.07-schema-evolution-without-alembic](lessons/04.07-schema-evolution-without-alembic.md) | Schema evolution without Alembic | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.08-indexes-and-query-plans](lessons/04.08-indexes-and-query-plans.md) | Indexes and query plans | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.09-data-integrity-and-uniqueness](lessons/04.09-data-integrity-and-uniqueness.md) | Data integrity and uniqueness | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.10-api-error-contracts](lessons/04.10-api-error-contracts.md) | API error contracts | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.11-dependency-injection-and-testability](lessons/04.11-dependency-injection-and-testability.md) | Dependency injection and testability | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |
| [04.12-architecture-review-for-database-migration](lessons/04.12-architecture-review-for-database-migration.md) | Architecture review for database migration | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
