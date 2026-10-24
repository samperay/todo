# Roadmap, dependencies and milestones

## Milestones

1. **Understand the running Todo system (01–02).** Trace frontend code, HTTP, sessions, and failures. Previously guided; re-verify evidence.
2. **Design reliable backend communication (03–04).** Prototype worker + outbox, then decide whether the Todo app needs integration.
3. **Operate the application (05–08).** Linux, networking, containers, CI/CD. Build repeatable local deployment and rollback.
4. **Design the platform (09–12).** IaC, Kubernetes, cloud; start locally and document costs/security before cloud resources.
5. **Prove reliability (13–18).** Observability, SLOs, load tests, security, distributed-systems reasoning, restore exercises.
6. **Demonstrate leadership (19–20).** Read-only AI operations POC and evidence-backed architecture capstone.

## Dependencies

- Module 03 queue experiments can be standalone; RabbitMQ integration benefits from Module 07 Docker skills.
- Module 10 assumes container fundamentals (07); Module 11 assumes Kubernetes fundamentals (10).
- Module 14 SLOs benefit from Module 13 metrics; Module 18 recovery tests benefit from Module 04 persistence.
- Module 20 consumes evidence and ADRs from every earlier module.

## Git workflow for each implementation milestone

1. Inspect current branch and code; create a new feature branch.
2. Define user stories and acceptance criteria in `specs/<feature>/spec.md`.
3. Update `plan.md`, `tasks.md`, API/data contracts and architecture decision records as needed.
4. Implement the smallest vertical slice; run tests, type checks and lint.
5. Add a failure lab and operational runbook.
6. Open PR, review independently, merge only when checks pass.

## Current checkpoint (as of handbook creation)

- Module 01: guided sessions completed; lab evidence may need recording.
- Module 02: guided sessions completed through circuit-breaker concepts; verify lab evidence.
- Module 03: 03.1 conceptual introduction; next guided hands-on is 03.2 producer–consumer.
- Modules 04–20: planned, not yet completed.

These are **learning-status notes**, not claims that all labs or implementations have been independently validated.
