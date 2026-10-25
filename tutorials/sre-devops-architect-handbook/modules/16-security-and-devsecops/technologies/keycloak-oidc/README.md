# Keycloak and OIDC — Learn → Integrate → Operate

## Todo use case

Current Todo uses bearer identity; Keycloak is an optional proposed migration.

## Restaurant analogy

Restaurant badge issuer verifies staff identity; the kitchen still decides who may modify a specific order.

## Learn — safe standalone experiments

1. [Authentication vs authorization](learn/01-authentication-vs-authorization.md)
2. [OAuth2 and OIDC roles](learn/02-oauth2-and-oidc-roles.md)
3. [Local identity provider](learn/03-local-identity-provider.md)
4. [JWT validation requirements](learn/04-jwt-validation-requirements.md)
5. [Legacy token migration](learn/05-legacy-token-migration.md)
6. [Identity operations and rotation](learn/06-identity-operations-and-rotation.md)

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
