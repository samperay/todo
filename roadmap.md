# Todo API — SRE / DevOps Architect Learning Roadmap

> **Purpose:** This is the durable learning contract and project handoff document for the `samperay/todo` repository. A future AI tutor or contributor should read this file **and inspect the current repository** before proposing a lesson, making a change, or claiming that a feature exists.
>
> **Repository:** `samperay/todo` · **Baseline branch:** `main` · **Suggested location:** `/roadmap.md` at repository root · **Status:** Planned, not an implementation specification for immediate wholesale delivery.
>
> **Learner's goal:** Progress from experienced SRE / DevOps automation engineer toward **SRE / DevOps Architect**, through hands-on engineering, architecture decisions, reliability trade-offs, and technical communication.

## 1. How to use this roadmap in a future chat

When the learner shares this file or its GitHub location, the tutor MUST:

1. Read `roadmap.md` and the latest `README.md`, `compose.yaml`, `backend/pyproject.toml`, application entry point, relevant routes/services/models, tests, CI workflow, and any stage-specific design notes. **Do not treat this roadmap as proof that the current code still matches the snapshot below.**
2. Inspect the `main` branch or the explicitly named working branch and record the branch name and commit SHA. Check whether the requested technology has already been introduced; never duplicate existing work.
3. Read `## 4. Current project snapshot` and reconcile discrepancies with live code. Report **verified**, **assumed**, and **not yet implemented** separately. If repository access fails, request the necessary file or output instead of guessing.
4. Check `## 10. Progress and resume checkpoint`. Ask which phase/class to resume **only if the answer is not already recorded**.
5. Teach **one small class/lab at a time**, with the cycle: **problem → analogy → architecture → design decision → executable steps → expected output → learner runs it → troubleshoot → verify → reflect**.
6. **Do not advance to the next exercise until the learner confirms completion or explicitly asks to skip.** Ask at most 1–3 targeted questions per turn; prioritize terminal evidence over multiple-choice quizzes.
7. Do not modify the repository, commit, push, open PRs, deploy, or create cloud resources without an explicit request. Suggest minimal diffs and explain them first. Treat destructive commands and billable resources as opt-in.
8. After each completed lab, help update the progress checkpoint with the commit/PR, evidence, problems encountered, decisions, and next exact step. This document is the durable handoff; chat memory is not the source of truth.

**Recommended user prompt for a new chat:**

> Read `roadmap.md` in `samperay/todo` on `main`, verify the current code and progress checkpoint, and resume the next incomplete SRE/DevOps Architect lab. Teach me one executable exercise at a time. Do not implement ahead of me; explain the reasoning and wait for my terminal output.

## 2. Outcomes and success criteria

By the end of this roadmap, the learner should be able to:

- **Application architecture:** Explain request lifecycle, async I/O, persistence, caching, messaging, auth, service boundaries, and failure modes.
- **Platform engineering:** Containerize and deliver a reproducible service; design CI/CD, environments, secrets, and infrastructure-as-code.
- **Reliability engineering:** Identify single points of failure; plan graceful degradation, retries, timeouts, idempotency, capacity, backups, recovery, and measurable SLOs.
- **Security:** Apply least privilege, token validation, secure configuration, supply-chain controls, and threat modeling.
- **Architectural judgment:** Compare alternatives, articulate constraints, draw diagrams, write Architecture Decision Records (ADRs), and defend trade-offs.
- **Communication:** Present a 3-minute design overview and a concise incident/postmortem summary for each major phase.

**Portfolio evidence:** Working branches/PRs, tests, runnable Compose manifests, architecture diagrams, ADRs, runbooks, failure-mode tables, cost notes, and concise demonstrations. Completing tutorials without these artifacts is not sufficient.

## 3. Learning principles and guardrails

- **20% concept, 80% hands-on**; begin with the smallest observable change.
- Every technology must solve a **specific Todo use case**. No tool is mandatory merely because it appears on this roadmap.
- Keep the existing Todo API functional and backward compatible unless a migration is intentionally approved.
- Prefer a single evolving project with **short-lived feature branches** and incremental PRs to `main`. Do not assume that two feature branches can be merged without integration work.
- Use local Docker Compose first; then local Kubernetes; use a cloud provider only after a cost/security/teardown review.
- Default to safe tests, mocked failures, and controlled container restarts. **No new artificial error endpoints, latency injection, or deliberate database corruption at present.** Revisit only if the learner explicitly opts in later.
- No production credentials, real user data, public webhook URLs, or secrets in Git. Avoid exposing services publicly by default.
- Define rollback/cleanup before each risky experiment. Record what was changed and how to reverse it.
- Distinguish **application behavior** from **infrastructure behavior**; distinguish **availability of `/metrics`** from **availability of Todo operations**.
- Prefer tests and observable outcomes to assumptions; preserve existing CI gates.

## 4. Current project snapshot — verified from `main` on 2026-10-19

This snapshot was based on direct reads of repository files. It is **not** a guarantee about future commits or runtime behavior.

| Area | Observed state / evidence |
|---|---|
| Repository | `samperay/todo`, default working baseline `main` |
| App | FastAPI, Python >=3.12, async SQLAlchemy >=2, Pydantic >=2; package in `backend/src/todo_api/` |
| API entry | `backend/src/todo_api/main.py`; `create_app()` and async lifespan create DB engine/schema/session factory |
| Database | **SQLite via aiosqlite by default**, `sqlite+aiosqlite:///./todo.db` — **not PostgreSQL currently** |
| Identity | `POST /api/v1/users` creates a person and issues a bearer token; Todo endpoints require token and are scoped to owner |
| Todo routes | `/api/v1/todos`: POST, GET list, GET by ID, PATCH, DELETE; POST `/{todo_id}/complete` and `/{todo_id}/incomplete` |
| Local stack | Root `compose.yaml`: `todo-api` on loopback port 8000; `prometheus` on loopback port 9090 |
| Prometheus | `prom/prometheus:v3.13.4`; `deploy/prometheus/prometheus.yml`; scrape `todo-api:8000/metrics` every 15s; named volume `prometheus-data` |
| Metrics | `http_requests_total`, `http_requests_in_progress`, `http_request_duration_seconds` (verify label sets against current middleware) |
| Persistence warning | README states API container's SQLite data is **not** persisted across container recreation; Prometheus TSDB has a named volume |
| Tests | Pytest, pytest-asyncio, HTTPX; temporary SQLite test database |
| CI | `.github/workflows/ci.yml`: Ruff lint, Ruff format, mypy, pytest with >=90% coverage threshold |
| Documentation | `tutorials/observability-handbook/` contains a separate 40-class observability curriculum; **currently paused** |

**Repository references to recheck:**

- `README.md`
- `compose.yaml`
- `backend/pyproject.toml`
- `backend/src/todo_api/main.py`
- `backend/src/todo_api/api/routes/todos.py`
- `backend/src/todo_api/api/routes/users.py`
- `backend/src/todo_api/core/config.py`
- `backend/src/todo_api/db/`
- `backend/src/todo_api/services/`
- `backend/tests/`
- `deploy/prometheus/prometheus.yml`
- `.github/workflows/ci.yml`
- `tutorials/observability-handbook/README.md`

**Important corrections to earlier generic suggestions:** Do not describe the current Todo application as PostgreSQL-backed. Do not claim Redis, RabbitMQ, an API Gateway, Keycloak, Grafana, Loki, Tempo, Kubernetes, Terraform, or MCP are implemented unless verified. GitHub Actions CI **already exists**; its phase should extend it rather than introduce it from scratch.

### Baseline commands (run from repository root unless noted)

```bash
git status --short
git branch --show-current
git rev-parse --short HEAD
docker compose config --services
docker compose up -d --build
docker compose ps
curl -fsS http://127.0.0.1:8000/openapi.json >/dev/null
curl -fsS http://127.0.0.1:8000/metrics | head -30
curl -fsS http://127.0.0.1:9090/-/ready
```

To run quality gates (from `backend/` with environment installed):

```bash
ruff check .
ruff format --check .
mypy src
python -m pytest --cov=todo_api --cov-report=term-missing --cov-fail-under=90
```

**Expected:** Containers running, HTTP API schema and metrics available, Prometheus ready, checks pass. **If not:** stop and diagnose actual outputs before starting a new technology. The commands are checks, not claims that they have been executed by the tutor.

## 5. Target architecture — evolutionary, not current

```text
                        Client / CLI / future MCP client
                                      |
                           [API Gateway, later]
                                      |
                           [OIDC/Keycloak, later]
                                      |
                            FastAPI Todo API
                             /      |       \
                            /       |        \
                     [Redis]   [SQLite -> DB]  [RabbitMQ]
                      cache     persistence       |
                                              [Worker(s)]

                GitHub Actions -> image -> Kubernetes / cloud
                Terraform -> optional cloud infrastructure
                Prometheus now; advanced observability paused
```

**Design rule:** Start with the verified existing application. The diagram depicts possible future components, not requirements to install all of them.

## 6. Phase roadmap — recommended order, with decision gates

| Phase | Stack / topic | Todo-specific problem | Architect competency | Prerequisite / decision gate | State |
|---|---|---|---|---|---|
| 00 | Baseline, architecture map, ADR workflow | Establish reproducible reference system | Requirements, constraints, risk assessment | None | **Next** |
| 01 | Redis caching | Avoid repeated reads for a user-scoped Todo list | Cache-aside, consistency, TTL, graceful degradation | Baseline stable; choose cache keys and invalidation policy | Planned |
| 02 | RabbitMQ + Python worker | Process Todo-created/completed events asynchronously | Delivery guarantees, idempotency, outbox trade-offs | Define an actual event consumer; Redis not required | Planned |
| 03 | API Gateway (e.g. Kong/Traefik) | Centralize routing, quotas, and edge controls | North–south traffic, TLS, trust boundaries | Working API; choose gateway after comparison | Planned |
| 04 | Keycloak / OIDC | Replace or bridge bespoke bearer-token identity | Authentication vs authorization, JWT, roles, migration | Threat model; **do not break existing users silently** | Planned |
| 05 | CI/CD hardening + supply chain | Safely ship multi-service changes | Pipelines, release gates, SBOM, image scanning, rollbacks | Existing GitHub Actions already running | Planned |
| 06 | PostgreSQL migration + data durability | Move beyond container-local SQLite and protect data | Migrations, backups, restore, pooling, consistency | Explicit decision: retain SQLite for now or migrate | Planned / optional until justified |
| 07 | Kubernetes (kind/k3d first) | Run API and dependencies as managed workloads | Scheduling, probes, config, scaling, stateful systems | Container images, health contracts, durable data plan | Planned |
| 08 | Terraform + cloud deployment | Reproduce infrastructure declaratively | State, drift, IAM, networking, cost, environments | Select provider/budget; local-first | Planned |
| 09 | MCP + optional AI assistant | Expose safe Todo tools to clients/agents | API contracts, tool security, human approval | Stable authenticated API | Planned / elective |
| 10 | Resume observability + reliability capstone | Diagnose full-stack user journeys | SLI/SLO, incident response, architecture review | Learner elects to resume observability | Paused |

**Ordering is advisory.** Redis, messaging, gateway, and identity can be learned independently. Preserve dependency reasoning: e.g., don't require Redis for RabbitMQ; don't assume Kubernetes requires Terraform. Re-evaluate the next stack after every phase.

## 7. Detailed phase curricula and practical challenges

### Phase 00 — Establish the architecture baseline (mandatory)

**Why:** An architect cannot make sound decisions without knowing the actual current system.

**Classes / exercises**

- **00.1 — Read the running system:** Trace request `POST /api/v1/users` → bearer token → authorized `POST /api/v1/todos` → SQLite. Use OpenAPI, route/service code, and test cases.
- **00.2 — Reproducible local stack:** Run Compose, inspect service DNS, ports, volumes, environment, and Prometheus scrape. Identify the API SQLite durability limitation.
- **00.3 — Architecture map:** Create a Mermaid context/container diagram and a dependency/failure-mode table. Explain sync request path vs background work.
- **00.4 — Quality and decision records:** Run CI-equivalent checks and write `docs/adr/0001-architecture-baseline.md` (proposed path; create only when approved).

**Exit gate:** Learner demonstrates a working authenticated Todo flow, passes checks, and explains at least three risks (e.g., SQLite persistence, token handling, API/Prometheus availability).

### Phase 01 — Redis: cache-aside for user-owned Todo lists (recommended next stack)

**Use case:** Repeated `GET /api/v1/todos` requests by the same authenticated owner. First establish whether caching is worthwhile; a small local app may not need it. The purpose is to learn trade-offs, not claim a performance win.

| Class | Guided work | Independent task | Architect question |
|---|---|---|---|
| 01.1 | Start a Redis container in Compose; verify connectivity with a CLI and network inspection | Explain host vs container DNS | What happens if Redis is unreachable? |
| 01.2 | Compare direct DB read with cache-aside read; design **owner-scoped keys** and bounded TTL | Sketch request sequence | How do we prevent cross-user data leakage? |
| 01.3 | Implement caching behind a feature flag with a fallback to DB; unit/integration tests | Measure hits/misses without assuming speedup | Is cache availability critical? |
| 01.4 | Invalidate list cache on create/update/complete/incomplete/delete | Demonstrate fresh reads after mutation | TTL vs write invalidation vs write-through? |
| 01.5 | Examine memory limits, eviction, serialization, and safe degradation | Produce an ADR comparing no-cache vs Redis | Is the complexity justified? |

**No implementation yet:** This roadmap does not add Redis or change Todo code. Confirm desired behavior, serialization, ownership, and testing strategy before implementation.

**Evidence:** Passing authenticated two-user isolation tests; cache hit/miss demonstration; stale-data test; recovery when Redis is stopped (prefer stopping only the Redis test container); ADR; rollback steps.

**Acceptance:** API still works when cache is disabled or unavailable; no owner can retrieve another owner's data; mutation invalidation is verified; existing tests and coverage gate pass.

### Phase 02 — RabbitMQ: asynchronous Todo events

**Use case:** When a Todo is created or completed, generate an **audit event** for a separate worker (local test output or audit table; don't introduce email/Slack credentials just to make a demo).

- **02.1:** Producer, broker, queue, exchange, routing key; run RabbitMQ locally.
- **02.2:** Define versioned event contract (`event_id`, `event_type`, `occurred_at`, `todo_id`, `owner_id`, minimal safe payload); discuss sensitive fields.
- **02.3:** Build a worker that consumes events and acknowledges after successful processing.
- **02.4:** Demonstrate bounded retries, dead-letter routing, poison messages, and consumer idempotency using safe test messages.
- **02.5:** Evaluate the dual-write problem (DB commit succeeds, publish fails). Design a transactional outbox or document why it is deferred.

**Acceptance:** Event processing is reproducible; duplicates do not create duplicate effects; worker downtime does not corrupt Todo CRUD; design records delivery guarantees and trade-offs.

### Phase 03 — API Gateway: traffic and trust boundaries

- **03.1:** Compare Kong, Traefik, and a simple reverse proxy against actual needs; write selection ADR.
- **03.2:** Route `/api/v1/*` to Todo API using Compose networking; preserve direct local debug path.
- **03.3:** Apply bounded rate limits; verify HTTP responses and client identity handling.
- **03.4:** Explore TLS termination, forwarded headers, request size limits, timeouts, and upstream failures.
- **03.5:** Draw threat boundary; distinguish edge checks from application authorization.

**Acceptance:** Authorized Todo requests work through gateway; limits and timeouts are testable; security decisions are explicit; no accidental public exposure.

### Phase 04 — Keycloak / OIDC: identity migration

- **04.1:** Map current user-issued bearer tokens and authorization checks; identify migration risk.
- **04.2:** Learn OAuth2 vs OIDC, issuer, audience, JWKS, scopes, token expiry, and rotation.
- **04.3:** Start local Keycloak, configure a development realm/client and test identities.
- **04.4:** Verify JWT signature, issuer, audience, and expiration in FastAPI; preserve owner isolation.
- **04.5:** Design role/scopes and coexistence or migration plan for legacy tokens; test denial paths.

**Acceptance:** Invalid/expired/wrong-audience tokens are rejected; one user cannot access another's Todo; migration and rollback documented. Do not claim Keycloak is necessary for every deployment.

### Phase 05 — CI/CD and supply-chain hardening

**Existing baseline:** Ruff, formatting, mypy, pytest coverage gate on GitHub Actions already exist.

- **05.1:** Read current workflow; map trigger → checks → merge gate.
- **05.2:** Add a reproducible container build and image tagging strategy.
- **05.3:** Evaluate dependency scanning, container scanning, and SBOM generation.
- **05.4:** Design deployment promotion, environment configuration, secret handling, and rollback.
- **05.5:** Build a release checklist and a safe staging deployment plan.

**Acceptance:** Existing quality gates preserved; new build artifacts traceable to commits; no secrets embedded in images or logs; rollback documented.

### Phase 06 — PostgreSQL and persistence engineering (optional decision gate)

**Current state is SQLite.** Migration is a deliberate architectural choice, not a prerequisite for Redis or RabbitMQ labs.

- **06.1:** Compare SQLite vs PostgreSQL for expected concurrency, operational burden, and persistence.
- **06.2:** Design data migration and schema versioning (e.g., Alembic) with rollback and validation.
- **06.3:** Introduce Postgres locally with a persistent volume only if selected.
- **06.4:** Explore pooling, indexes, transactions, backup/restore, and failure recovery.
- **06.5:** Verify migration preserves users, token semantics, and Todo ownership.

**Acceptance:** Data survives container recreation; restore test passes; schema changes are repeatable; choice documented. Never run a destructive migration against important data without a backup.

### Phase 07 — Kubernetes: platform operations

- **07.1:** Local kind/k3d cluster, images, namespaces, Deployments, Services.
- **07.2:** ConfigMaps/Secrets, health probes, resources, rolling updates.
- **07.3:** Ingress/gateway, service-to-service DNS, network policies.
- **07.4:** Stateful dependency strategy: persistent storage vs managed external services.
- **07.5:** Scaling and rollout recovery; demonstrate replica limitations of container-local SQLite.

**Acceptance:** API is reachable; rollout and rollback verified; data/state architecture is valid for multiple replicas; cost and operational trade-offs explained.

### Phase 08 — Terraform + cloud foundations

- **08.1:** Terraform workflow, providers, state, plan/apply/destroy, and drift.
- **08.2:** Select provider and minimal network/IAM design; estimate cost before provisioning.
- **08.3:** Modules, variables, outputs, remote state and locking concepts.
- **08.4:** Deploy a small nonproduction environment with explicit cleanup.
- **08.5:** Review least privilege, secrets, recovery, and architecture trade-offs.

**Acceptance:** Infrastructure reproducible and fully removable; no secrets in state committed to Git; billable resources approved first.

### Phase 09 — MCP and AI-assisted Todo workflows (elective)

- **09.1:** Understand MCP tools/resources/prompts and how they differ from REST endpoints.
- **09.2:** Implement read-only Todo tools first, preserving user identity and scope.
- **09.3:** Add create/update tools with explicit user confirmation for writes.
- **09.4:** Handle validation, tool errors, timeouts, and auditability.
- **09.5:** Threat-model prompt injection, unauthorized tool use, and secret leakage.

**Acceptance:** Read/write tools respect Todo authorization; destructive operations require confirmation; errors are safe and understandable.

### Phase 10 — Observability and SRE architecture capstone (paused)

Continue existing `tutorials/observability-handbook/` only when the learner chooses to resume. Reconcile its outdated branch references and commands with current `main` before executing. Add Grafana, Alertmanager, Loki, Tempo, and OpenTelemetry incrementally, not as presumed existing features.

**Capstone:** Define user-facing SLIs/SLOs; create service/dependency map; build incident runbooks; rehearse a safe service outage using non-destructive operations; compare architecture options for scaling, availability, security, and cost.

## 8. Standard class template — mandatory for every future lesson

Use the following headings when presenting a class (in chat or a tutorial file):

1. **Class ID, title, prerequisites, duration, current Git SHA.**
2. **Real Todo problem and user impact.** Why is this technology worth introducing?
3. **Theory + analogy (brief).** Define important terms without assuming prior knowledge.
4. **Before/after architecture.** Mermaid or ASCII; mark future components as proposed.
5. **Decision point.** At least two viable options, trade-offs, and chosen default.
6. **Guided lab (Level 1).** Exact directory, commands, code/config changes, explanation, expected output, verification, cleanup.
7. **Independent exercise (Level 2).** A clear requirement and acceptance criteria; no immediate answer.
8. **SRE incident/design challenge (Level 3).** Symptoms, constraints, evidence to collect, hypotheses; reveal hints only on request.
9. **Troubleshooting.** Common errors, first diagnostic command, likely causes, safe remediation.
10. **Review questions.** 2–4 questions emphasizing *why*, not memorization.
11. **Definition of done.** Tests, runtime behavior, security, rollback, documentation, and evidence.
12. **Progress update.** Mark checkpoint, link branch/PR/commit, record next exact action.

**Tutor pacing:** Present the objective and **only the first executable step** initially. Wait for the learner's output before issuing the next command. Don't dump an entire phase of code in one answer unless explicitly requested.

## 9. Architecture artifacts and review rubric

For each major phase, produce or update:

- **Context diagram** (users, API, dependencies, trust boundaries).
- **Container/component diagram** (services, persistence, protocols, ownership).
- **Sequence diagram** for one successful path and one failure path.
- **ADR**: Context, decision, alternatives, consequences, reversibility.
- **Failure-mode table**: dependency, symptom, user impact, detection, fallback, recovery.
- **Runbook**: prerequisites, safe commands, expected output, troubleshooting, rollback.
- **Verification**: tests, sample HTTP interactions, logs/metrics when already available.
- **Operational review**: security, performance, cost, maintenance, and migration.

Score each phase 0–3 in **Correctness**, **Reliability**, **Security**, **Operability**, **Architecture rationale**, and **Communication**:

- 0 = missing; 1 = described; 2 = demonstrated; 3 = demonstrated and trade-offs defended.
- Phase is complete only when all categories are at least 2 and the learner can explain the architecture without reading a script.

## 10. Progress and resume checkpoint — update after every class

> This is the **single most important handoff section** for continuing across chats. Update it in the GitHub file when a class is complete. Never mark a task complete without learner-confirmed evidence.

```yaml
roadmap_version: 1.0
last_updated: 2026-10-19
repository: samperay/todo
baseline_branch: main
verified_commit: null  # Fill after checking the current Git SHA
career_track: SRE / DevOps Architect
observability_status: paused
current_phase: '00'
current_class: '00.1'
current_state: not_started
next_action: 'Read live main branch and verify baseline; then run first Phase 00 exercise.'
completed_classes: []
working_branch: null
latest_pr: null
latest_commit: null
lab_evidence: []
open_questions:
  - 'Confirm whether Redis should be the first new stack after baseline.'
  - 'Decide whether to retain SQLite or plan PostgreSQL later, based on actual requirements.'
  - 'Choose a small, meaningful Todo use case for each new dependency before coding.'
known_blockers: []
architect_decisions: []
```

**Suggested per-class journal entry:**

```markdown
### YYYY-MM-DD — Phase XX / Class XX.Y
- Branch / SHA / PR:
- Goal:
- Commands executed:
- Observed output (sanitized):
- Tests and acceptance checks:
- Design decision and alternatives:
- Issues / troubleshooting:
- Cleanup or rollback completed:
- Learner explanation (2–3 sentences):
- Status: completed | blocked | skipped
- Next exact step:
```

## 11. Immediate next session: Phase 00 / Class 00.1

**Goal:** Understand the current Todo request lifecycle before adding any technology.

**First guided exercise:**

```bash
git checkout main
git pull --ff-only origin main
git rev-parse --short HEAD
docker compose config --services
```

**Expected:** Current commit SHA and service names (currently documented as `todo-api` and `prometheus`). If the working tree has uncommitted changes, stop before switching branches and ask how to preserve them. If Docker Compose differs, update the snapshot rather than forcing expected output.

**Next (only after user shares output):** Start the stack, create a test user with `POST /api/v1/users`, store its returned token locally without posting it, create and list a Todo using authenticated requests, inspect the route/service/database path, and run tests. Capture the system diagram and one ADR. Only then decide whether to start Redis.

**Suggested first architecture question:** "What failure or bottleneck in this particular Todo API would justify Redis, and what would be the simplest alternative?"

---

## 12. Document maintenance rules

- Keep this roadmap at the repository root for discoverability; link it from `README.md` when convenient.
- Update the snapshot when the app changes (SQLite → PostgreSQL, auth changes, services added, new CI checks).
- Keep future-state plans clearly marked **planned**, never **implemented** by implication.
- Use stable class IDs and append evidence instead of overwriting completed work.
- Link implementation PRs and ADRs as phases progress.
- Revisit roadmap ordering when a new real requirement makes another technology more useful.
- When using an AI tutor, provide the repo URL and ask it to **verify live files**; this document is a navigation map, not a substitute for reading code.
