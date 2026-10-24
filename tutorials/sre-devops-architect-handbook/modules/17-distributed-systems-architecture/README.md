# Module 17 — Distributed Systems Architecture

**Scope:** Distributed systems duplicate delivery.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Distributed Systems Architecture**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Distributed systems duplicate delivery**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [17.01-partial-failure-and-unreliable-networks](lessons/17.01-partial-failure-and-unreliable-networks.md) | Partial failure and unreliable networks | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.02-latency-and-timeout-uncertainty](lessons/17.02-latency-and-timeout-uncertainty.md) | Latency and timeout uncertainty | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.03-cap-trade-offs-with-assumptions](lessons/17.03-cap-trade-offs-with-assumptions.md) | CAP trade-offs with assumptions | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.04-strong-versus-eventual-consistency](lessons/17.04-strong-versus-eventual-consistency.md) | Strong versus eventual consistency | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.05-replication-and-failover](lessons/17.05-replication-and-failover.md) | Replication and failover | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.06-leader-election-concepts](lessons/17.06-leader-election-concepts.md) | Leader election concepts | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.07-distributed-locks-and-fencing](lessons/17.07-distributed-locks-and-fencing.md) | Distributed locks and fencing | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.08-idempotency-and-deduplication](lessons/17.08-idempotency-and-deduplication.md) | Idempotency and deduplication | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.09-at-least-once-versus-at-most-once-delivery](lessons/17.09-at-least-once-versus-at-most-once-delivery.md) | At-least-once versus at-most-once delivery | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.10-transactional-outbox-and-sagas](lessons/17.10-transactional-outbox-and-sagas.md) | Transactional outbox and sagas | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.11-clock-skew-and-ordering](lessons/17.11-clock-skew-and-ordering.md) | Clock skew and ordering | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |
| [17.12-architecture-decision-trade-offs](lessons/17.12-architecture-decision-trade-offs.md) | Architecture decision trade-offs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
