# Terraform and cloud — Learn → Integrate → Operate

## Todo use case

Proposed reproducible Todo infrastructure; cloud provisioning is opt-in and billable.

## Restaurant analogy

Restaurant blueprint describes every kitchen station; the builder compares blueprint with what exists.

## Learn — safe standalone experiments

1. [Terraform lifecycle](learn/01-terraform-lifecycle.md)
2. [Declarative configuration](learn/02-declarative-configuration.md)
3. [Plan, state and drift](learn/03-plan-state-and-drift.md)
4. [Modules and variables](learn/04-modules-and-variables.md)
5. [IAM and networking](learn/05-iam-and-networking.md)
6. [Cloud cost and teardown](learn/06-cloud-cost-and-teardown.md)

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
