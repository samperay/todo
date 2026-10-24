# Technology Learning Index — v7

## One source of truth

Every track has exactly one canonical README and a numbered sequence of detailed Learn, Integrate, and Operate lessons. Existing v6 chapter names are compatibility redirects, not duplicated curricula. The actual Todo code is authoritative for what is implemented; repository-root `roadmap.md` is authoritative for planned technology phases.

## Tracks

- [Redis caching](modules/04-backend-architecture-and-database-engineering/technologies/redis/README.md) — 16 canonical lessons.
- [RabbitMQ messaging](modules/03-asynchronous-processing-and-event-driven-architecture/technologies/rabbitmq/README.md) — 16 canonical lessons.
- [API Gateway](modules/06-networking-and-api-architecture/technologies/api-gateway/README.md) — 15 canonical lessons.
- [Keycloak and OIDC](modules/16-security-and-devsecops/technologies/keycloak-oidc/README.md) — 15 canonical lessons.
- [CI/CD and supply chain](modules/08-ci-cd-and-software-delivery/technologies/cicd-supply-chain/README.md) — 15 canonical lessons.
- [PostgreSQL migration](modules/04-backend-architecture-and-database-engineering/technologies/postgresql/README.md) — 16 canonical lessons.
- [Kubernetes](modules/10-kubernetes-fundamentals/technologies/kubernetes/README.md) — 16 canonical lessons.
- [Terraform and cloud](modules/09-infrastructure-as-code/technologies/terraform-cloud/README.md) — 15 canonical lessons.
- [MCP and AI-assisted Todo](modules/19-ai-for-sre-and-devops/technologies/mcp-ai/README.md) — 15 canonical lessons.
- [Reliability architecture](modules/20-sre-devops-architect-capstone/technologies/reliability-capstone/README.md) — 15 canonical lessons.

## How to use with your tutor

1. Open the track README, then one lesson.
2. Read analogy, Todo mapping and explanation.
3. Run only the current guided exercise and compare expected output.
4. Share actual output and answer the knowledge check.
5. Advance only after reviewing observations.

## Project guardrails

- SQLite and existing bearer authentication remain the current baseline until live repository inspection confirms otherwise.
- No automatic edits, deployment, cloud costs, or production failures.
- For integration use Spec Kit: specify → clarify → plan → tasks → analyze → implement → test → PR.
- There is no `progress/` directory; the learner need not maintain a learning log.
