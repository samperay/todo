# Module 17 — Distributed Systems Architecture (Handbook v3)

**Purpose:** Learn distributed systems architecture through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-17.py`](../../labs/module-experiments/module-17.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [17.01 — partial failure and unreliable networks](lessons/17.01-partial-failure-and-unreliable-networks.md) | `python3 .../module-17.py --lesson 17.01` |
| [17.02 — latency and timeout uncertainty](lessons/17.02-latency-and-timeout-uncertainty.md) | `python3 .../module-17.py --lesson 17.02` |
| [17.03 — cap trade offs with assumptions](lessons/17.03-cap-trade-offs-with-assumptions.md) | `python3 .../module-17.py --lesson 17.03` |
| [17.04 — strong versus eventual consistency](lessons/17.04-strong-versus-eventual-consistency.md) | `python3 .../module-17.py --lesson 17.04` |
| [17.05 — replication and failover](lessons/17.05-replication-and-failover.md) | `python3 .../module-17.py --lesson 17.05` |
| [17.06 — leader election concepts](lessons/17.06-leader-election-concepts.md) | `python3 .../module-17.py --lesson 17.06` |
| [17.07 — distributed locks and fenCIng](lessons/17.07-distributed-locks-and-fencing.md) | `python3 .../module-17.py --lesson 17.07` |
| [17.08 — idempotency and deduplication](lessons/17.08-idempotency-and-deduplication.md) | `python3 .../module-17.py --lesson 17.08` |
| [17.09 — at least once versus at most once delivery](lessons/17.09-at-least-once-versus-at-most-once-delivery.md) | `python3 .../module-17.py --lesson 17.09` |
| [17.10 — transactional outbox and sagas](lessons/17.10-transactional-outbox-and-sagas.md) | `python3 .../module-17.py --lesson 17.10` |
| [17.11 — clock skew and ordering](lessons/17.11-clock-skew-and-ordering.md) | `python3 .../module-17.py --lesson 17.11` |
| [17.12 — architecture deCIsion trade offs](lessons/17.12-architecture-decision-trade-offs.md) | `python3 .../module-17.py --lesson 17.12` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
