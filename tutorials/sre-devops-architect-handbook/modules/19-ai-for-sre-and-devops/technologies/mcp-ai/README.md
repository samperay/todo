# MCP and AI-assisted Todo — Learn → Integrate → Operate

## Todo use case

Proposed read-only Todo tools first; no autonomous write access.

## Restaurant analogy

Restaurant concierge can look up orders, but changing an order requires the customer’s permission.

## Learn — safe standalone experiments

1. [MCP concepts](learn/01-mcp-concepts.md)
2. [Tool contracts](learn/02-tool-contracts.md)
3. [Identity propagation](learn/03-identity-propagation.md)
4. [Write confirmation and auditing](learn/04-write-confirmation-and-auditing.md)
5. [Prompt injection and validation](learn/05-prompt-injection-and-validation.md)
6. [Tool failure and observability](learn/06-tool-failure-and-observability.md)

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
