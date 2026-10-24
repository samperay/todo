# API Gateway — Learn → Integrate → Operate

## Todo use case

Proposed gateway routes client traffic to FastAPI; existing app authorization must remain.

## Restaurant analogy

Restaurant host directs customers to the correct counter, limits crowding, and checks reservations; chefs still enforce order ownership.

## Learn — safe standalone experiments

1. [Reverse proxy vs API gateway](learn/01-reverse-proxy-vs-api-gateway.md)
2. [Local gateway configuration](learn/02-local-gateway-configuration.md)
3. [Routing and forwarded headers](learn/03-routing-and-forwarded-headers.md)
4. [Rate limits and quotas](learn/04-rate-limits-and-quotas.md)
5. [TLS and upstream timeouts](learn/05-tls-and-upstream-timeouts.md)
6. [Gateway failure and recovery](learn/06-gateway-failure-and-recovery.md)

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
