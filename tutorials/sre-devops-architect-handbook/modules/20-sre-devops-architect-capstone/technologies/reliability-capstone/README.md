# Reliability architecture — Learn → Integrate → Operate

## Todo use case

Measure actual Todo user journeys, not only /metrics availability.

## Restaurant analogy

Restaurant manager measures order completion time, staff availability and recovery after kitchen equipment failure.

## Learn — safe standalone experiments

1. [SLIs and SLOs](learn/01-slis-and-slos.md)
2. [Error budgets](learn/02-error-budgets.md)
3. [Failure-mode analysis](learn/03-failure-mode-analysis.md)
4. [Incident response and runbooks](learn/04-incident-response-and-runbooks.md)
5. [Backup and recovery objectives](learn/05-backup-and-recovery-objectives.md)
6. [Architecture review](learn/06-architecture-review.md)

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
