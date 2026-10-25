# Module 04 — Backend Architecture And Database Engineering (Handbook v5)

**Purpose:** Learn backend architecture and database engineering through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-04.py`](../../labs/module-experiments/module-04.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [04.01 — fastAPI request lifecycle](lessons/04.01-fastapi-request-lifecycle.md) | `python3 .../module-04.py --lesson 04.01` |
| [04.02 — route versus service versus repository](lessons/04.02-route-versus-service-versus-repository.md) | `python3 .../module-04.py --lesson 04.02` |
| [04.03 — pydantic v2 typed contracts](lessons/04.03-pydantic-v2-typed-contracts.md) | `python3 .../module-04.py --lesson 04.03` |
| [04.04 — authentication and authorization boundaries](lessons/04.04-authentication-and-authorization-boundaries.md) | `python3 .../module-04.py --lesson 04.04` |
| [04.05 — sqlalchemy sessions and transactions](lessons/04.05-sqlalchemy-sessions-and-transactions.md) | `python3 .../module-04.py --lesson 04.05` |
| [04.06 — SQLite locking and concurrency](lessons/04.06-sqlite-locking-and-concurrency.md) | `python3 .../module-04.py --lesson 04.06` |
| [04.07 — schema evolution without alembic](lessons/04.07-schema-evolution-without-alembic.md) | `python3 .../module-04.py --lesson 04.07` |
| [04.08 — indexes and query plans](lessons/04.08-indexes-and-query-plans.md) | `python3 .../module-04.py --lesson 04.08` |
| [04.09 — data integrity and uniqueness](lessons/04.09-data-integrity-and-uniqueness.md) | `python3 .../module-04.py --lesson 04.09` |
| [04.10 — API error contracts](lessons/04.10-api-error-contracts.md) | `python3 .../module-04.py --lesson 04.10` |
| [04.11 — dependency injection and testability](lessons/04.11-dependency-injection-and-testability.md) | `python3 .../module-04.py --lesson 04.11` |
| [04.12 — architecture review for database migration](lessons/04.12-architecture-review-for-database-migration.md) | `python3 .../module-04.py --lesson 04.12` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.

## Canonical roadmap technology tracks

- [Redis cache-aside for user-scoped Todo lists — Learn → Integrate → Operate](technologies/redis/README.md)

- [PostgreSQL decision and migration — Learn → Integrate → Operate](technologies/postgresql/README.md)

## Technology track: Redis caching

Start with [Redis caching — Learn → Integrate → Operate](technologies/redis/README.md).

## Technology track: PostgreSQL migration

Start with [PostgreSQL migration — Learn → Integrate → Operate](technologies/postgresql/README.md).
