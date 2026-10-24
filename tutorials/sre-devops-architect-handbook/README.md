# Todo SRE/DevOps Architect — Engineering Handbook

> **Canonical learning index.** Commit this directory under `tutorials/sre-devops-architect-handbook/` in the Todo repository. This is a learning guide and target architecture, **not a claim that every technology is already implemented**.

## Mission

Learn development code, DevOps operation, and SRE/architecture decisions **together**, using the existing Todo application as a case study. Progress one lesson at a time: **concept → actual source code → infrastructure → safe lab → failure simulation → architecture trade-off → evidence**.

## Project baseline (verify against the active GitHub branch)

- Frontend: React + TypeScript + Vite; `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/session/useTodoSession.ts`, `frontend/src/api/client.ts`.
- Backend: FastAPI + Pydantic + SQLAlchemy + SQLite; `backend/src/todo_api/`.
- Development routing: browser → Vite `127.0.0.1:5173` → `/api` proxy → FastAPI `127.0.0.1:8000` → SQLite.
- Authentication: bearer token stored in browser `localStorage`; **never copy live tokens into issues, screenshots, or chat**.
- Existing capabilities: Todo CRUD foundation, tests/CI and Prometheus `/metrics`; re-check their current state before changes.
- SDD artifacts: `specs/`, `.specify/`, and GitHub PR reviews. Do not assume optional notification, RabbitMQ, Docker, or Kubernetes features already exist.

## How to use this with an AI tutor

1. Share the GitHub **branch URL** and the path to this `README.md`.
2. Say: `Resume Module NN, Lesson NN.MM. Read the handbook and actual repository files first. Teach one lesson only, with a small safe lab. Wait for my output before moving on.`
3. For implementation: `Before coding, inspect spec.md, plan.md, tasks.md and the constitution. Propose a small PR-sized change and its acceptance tests.`
4. Record actual outputs in `progress/LEARNING_LOG.md`. Mark complete **only after the lab and explanation are verified**.
5. If repository code differs from examples here, **actual code wins**. Update the handbook in the same PR when a documented contract changes.

## Safety and architecture guardrails

- Run destructive labs only against **disposable local data**; create backups first.
- Use the Ubuntu VM for `systemd` exercises; macOS commands differ.
- No real cloud resources without explicit billing, permission, and teardown review.
- Do not add new infrastructure merely to complete a lesson. Explain the design first.
- Keep SQLite for the current learning baseline; evaluate migration explicitly before shared-write horizontal scaling.
- Separate the **observed system**, **proposed design**, and **implemented system** in every architecture document.

## Completion criteria for each lesson

- Can explain the concept in plain language and point to the relevant Todo code.
- Can reproduce a successful path and one failure path.
- Can state what evidence supports the diagnosis.
- Can name at least one design trade-off and document it.
- Has recorded commands, outputs (with secrets redacted), and next action.

## Module map

| Module | Focus | Handbook |
|---|---|---|
| 01 | Application Architecture Fundamentals | [Open](modules/01-application-architecture-fundamentals/README.md) |
| 02 | Application Lifecycle and Resilience | [Open](modules/02-application-lifecycle-and-resilience/README.md) |
| 03 | Asynchronous Processing and Event-Driven Architecture | [Open](modules/03-asynchronous-processing-and-event-driven-architecture/README.md) |
| 04 | Backend Architecture and Database Engineering | [Open](modules/04-backend-architecture-and-database-engineering/README.md) |
| 05 | Linux and Operating Systems | [Open](modules/05-linux-and-operating-systems/README.md) |
| 06 | Networking and API Architecture | [Open](modules/06-networking-and-api-architecture/README.md) |
| 07 | Containerization | [Open](modules/07-containerization/README.md) |
| 08 | CI/CD and Software Delivery | [Open](modules/08-ci-cd-and-software-delivery/README.md) |
| 09 | Infrastructure as Code | [Open](modules/09-infrastructure-as-code/README.md) |
| 10 | Kubernetes Fundamentals | [Open](modules/10-kubernetes-fundamentals/README.md) |
| 11 | Advanced Kubernetes Architecture | [Open](modules/11-advanced-kubernetes-architecture/README.md) |
| 12 | Cloud Architecture | [Open](modules/12-cloud-architecture/README.md) |
| 13 | Observability Engineering | [Open](modules/13-observability-engineering/README.md) |
| 14 | SRE Reliability Engineering | [Open](modules/14-sre-reliability-engineering/README.md) |
| 15 | Performance and Scalability | [Open](modules/15-performance-and-scalability/README.md) |
| 16 | Security and DevSecOps | [Open](modules/16-security-and-devsecops/README.md) |
| 17 | Distributed Systems Architecture | [Open](modules/17-distributed-systems-architecture/README.md) |
| 18 | Disaster Recovery and Chaos Engineering | [Open](modules/18-disaster-recovery-and-chaos-engineering/README.md) |
| 19 | AI for SRE and DevOps | [Open](modules/19-ai-for-sre-and-devops/README.md) |
| 20 | SRE/DevOps Architect Capstone | [Open](modules/20-sre-devops-architect-capstone/README.md) |

## Suggested sequencing

- **01–06:** Application, resilience, messaging, backend, Linux, networking.
- **07–12:** Containers, delivery, IaC, Kubernetes, cloud.
- **13–18:** Observability, SRE, performance, security, distributed systems, disaster recovery.
- **19–20:** AI-assisted operations and architect capstone.

Lessons may be reordered when there is a practical reason, but record dependencies and avoid claiming a module complete without evidence.

## Navigation

- [Roadmap and module dependencies](ROADMAP.md)
- [Learning log](progress/LEARNING_LOG.md)
- [Lab record template](templates/LAB_RECORD.md)
- [Architecture decision record template](templates/ADR_TEMPLATE.md)
- [Incident runbook template](templates/RUNBOOK_TEMPLATE.md)
- [Architecture baseline](architecture/CURRENT_AND_TARGET.md)
- [Hands-on environment setup](labs/ENVIRONMENT_SETUP.md)
- [Glossary](GLOSSARY.md)
