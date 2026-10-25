# Kubernetes — Learn → Integrate → Operate

## Todo use case

Proposed orchestration for Todo API and workers; local SQLite prevents naive multi-replica scaling.

## Restaurant analogy

Restaurant manager assigns chefs to stations, replaces absent staff and controls service capacity.

## Learn — safe standalone experiments

1. [Cluster and workloads](learn/01-cluster-and-workloads.md)
2. [Local kind cluster](learn/02-local-kind-cluster.md)
3. [Deployments and Services](learn/03-deployments-and-services.md)
4. [Probes and resource limits](learn/04-probes-and-resource-limits.md)
5. [Ingress and network policy](learn/05-ingress-and-network-policy.md)
6. [State and scaling](learn/06-state-and-scaling.md)
7. [Rollout and recovery](learn/07-rollout-and-recovery.md)

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
