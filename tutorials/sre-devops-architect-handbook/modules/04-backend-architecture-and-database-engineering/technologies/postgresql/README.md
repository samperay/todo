# PostgreSQL migration — Learn → Integrate → Operate

## Todo use case

Todo uses SQLite; PostgreSQL is optional and needs an explicit migration decision.

## Restaurant analogy

Restaurant moves from one paper ledger to a shared database that multiple cashiers can update safely.

## Learn — safe standalone experiments

1. [SQLite vs PostgreSQL](learn/01-sqlite-vs-postgresql.md)
2. [PostgreSQL local sandbox](learn/02-postgresql-local-sandbox.md)
3. [Transactions and isolation](learn/03-transactions-and-isolation.md)
4. [Schema migration planning](learn/04-schema-migration-planning.md)
5. [Connection pooling and indexes](learn/05-connection-pooling-and-indexes.md)
6. [Backup and restore](learn/06-backup-and-restore.md)
7. [Migration decision gate](learn/07-migration-decision-gate.md)

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
