# Todo SRE/DevOps Architect Handbook — v3

**Mission:** Learn SRE/DevOps architecture through the Todo React/Vite → FastAPI → SQLite project, one lesson at a time.

**Important scope:** This package contains **20 executable Python module experiments** and a **Markdown lesson for each topic**. The general lesson pages guide code inspection and discussion; they share a module-level teaching simulation. **Lesson 03.02 has seven complete, independent hands-on exercises.** The other lessons do **not** yet have seven bespoke Python programs apiece; do not mistake the shared model for full technology-specific implementations.

## Current Todo baseline

- React/TypeScript/Vite frontend (`frontend/src/main.tsx`, `frontend/src/App.tsx`).
- FastAPI/Pydantic/SQLAlchemy/SQLite backend (`backend/src/todo_api`).
- Local development path: browser → Vite :5173 → `/api` proxy → FastAPI :8000 → SQLite.
- Prometheus `/metrics`; bearer authentication. Never share real bearer tokens.
- Queues, RabbitMQ, Kubernetes and cloud deployments are **proposed learning topics**, not verified deployed Todo features.

## Start

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py --lesson 03.02
```

Read the lesson file first, then run its lab. Stop after each exercise and discuss observed output before moving on.

## Modules

- [01 — Application Architecture Fundamentals](modules/01-application-architecture-fundamentals/README.md)
- [02 — Application Lifecycle And Resilience](modules/02-application-lifecycle-and-resilience/README.md)
- [03 — Asynchronous Processing And Event Driven Architecture](modules/03-asynchronous-processing-and-event-driven-architecture/README.md)
- [04 — Backend Architecture And Database Engineering](modules/04-backend-architecture-and-database-engineering/README.md)
- [05 — Linux And Operating Systems](modules/05-linux-and-operating-systems/README.md)
- [06 — Networking And Api Architecture](modules/06-networking-and-api-architecture/README.md)
- [07 — Containerization](modules/07-containerization/README.md)
- [08 — Ci Cd And Software Delivery](modules/08-ci-cd-and-software-delivery/README.md)
- [09 — Infrastructure As Code](modules/09-infrastructure-as-code/README.md)
- [10 — Kubernetes Fundamentals](modules/10-kubernetes-fundamentals/README.md)
- [11 — Advanced Kubernetes Architecture](modules/11-advanced-kubernetes-architecture/README.md)
- [12 — Cloud Architecture](modules/12-cloud-architecture/README.md)
- [13 — Observability Engineering](modules/13-observability-engineering/README.md)
- [14 — Sre Reliability Engineering](modules/14-sre-reliability-engineering/README.md)
- [15 — Performance And Scalability](modules/15-performance-and-scalability/README.md)
- [16 — Security And Devsecops](modules/16-security-and-devsecops/README.md)
- [17 — Distributed Systems Architecture](modules/17-distributed-systems-architecture/README.md)
- [18 — Disaster Recovery And Chaos Engineering](modules/18-disaster-recovery-and-chaos-engineering/README.md)
- [19 — Ai For Sre And Devops](modules/19-ai-for-sre-and-devops/README.md)
- [20 — Sre Devops Architect Capstone](modules/20-sre-devops-architect-capstone/README.md)

## Tutor instructions

Read `START_HERE.md`, the module README, the lesson Markdown and the referenced lab `.py` before explaining. Explain only one exercise at a time; wait for terminal output. Never claim simulated infrastructure exists. Inspect the actual Todo code before suggesting modifications. Record verified evidence in the learning log.

## Safety

Labs run locally with Python 3 standard library. The HTTP/network labs may attempt loopback connections. They do not write to Todo data, provision cloud resources, or deploy containers. Use SDD specs and a separate PR for any actual application changes.

## Version 4 lesson enhancements

All existing lessons retain their original content and now include **1. Real-world analogy**, **2. Understanding the core concept**, and **4. What to Observe**. Lesson 03.02 has a detailed `queue.Queue` reference and hands-on observation checklist. Module README indexes also explain how to use these additions. Shared baseline experiments remain introductory simulations and must not be mistaken for individual real-world implementations.
