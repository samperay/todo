# Redis caching — Learn → Integrate → Operate

## Todo use case

Authenticated GET /api/v1/todos may use owner-scoped cache-aside; SQLite remains authoritative.

## Restaurant analogy

A busy restaurant keeps a short-lived list of popular dishes at the counter; the kitchen ledger remains authoritative.

## Learn — safe standalone experiments

1. [Redis fundamentals and architecture](learn/01-redis-fundamentals-and-architecture.md)
2. [Redis CLI and data types](learn/02-redis-cli-and-data-types.md)
3. [Python Redis client](learn/03-python-redis-client.md)
4. [Cache-aside and key design](learn/04-cache-aside-and-key-design.md)
5. [TTL and invalidation](learn/05-ttl-and-invalidation.md)
6. [Failure handling and fallback](learn/06-failure-handling-and-fallback.md)
7. [Redis performance and architecture trade-offs](learn/07-redis-performance-and-architecture-trade-offs.md)

## Integrate — Spec-Driven Development

1. [Todo requirements and acceptance criteria](integrate/01-todo-requirements-and-acceptance-criteria.md)
2. [SDD specification and design](integrate/02-sdd-specification-and-design.md)
3. [Implementation boundaries and contracts](integrate/03-implementation-boundaries-and-contracts.md)
4. [Tests, rollout and rollback](integrate/04-tests-rollout-and-rollback.md)

## Operate — production-style SRE thinking

1. [Deployment and health](operate/01-deployment-and-health.md)
2. [Metrics, logs and alerts](operate/02-metrics-logs-and-alerts.md)
3. [Failure injection and recovery](operate/03-failure-injection-and-recovery.md)
4. [Security and capacity](operate/04-security-and-capacity.md)
5. [Architecture decision and runbook](operate/05-architecture-decision-and-runbook.md)

## Completion criteria

Learn: run and explain evidence. Integrate: write a reviewed spec and tests before changing Todo. Operate: document health, failure, recovery, security and architecture trade-offs. **All additions to Todo are proposed until verified in code.**
