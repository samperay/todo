# CI/CD and supply chain — Learn → Integrate → Operate

## Todo use case

Todo already has Ruff, mypy, pytest and GitHub Actions; extend rather than replace.

## Restaurant analogy

Restaurant quality inspector checks each meal before it reaches the serving counter.

## Learn — safe standalone experiments

1. [Inspect existing quality gates](learn/01-inspect-existing-quality-gates.md)
2. [Reproducible builds](learn/02-reproducible-builds.md)
3. [Container image inspection](learn/03-container-image-inspection.md)
4. [SBOM and dependency scanning](learn/04-sbom-and-dependency-scanning.md)
5. [Release promotion and rollback](learn/05-release-promotion-and-rollback.md)
6. [Pipeline failure diagnosis](learn/06-pipeline-failure-diagnosis.md)

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
