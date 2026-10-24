# Module 03 — Asynchronous Processing And Event Driven Architecture (Handbook v3)

**Purpose:** Learn asynchronous processing and event driven architecture through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-03.py`](../../labs/module-experiments/module-03.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [03.01 — synchronous versus asynchronous requests](lessons/03.01-synchronous-versus-asynchronous-requests.md) | `python3 .../module-03.py --lesson 03.01` |
| [03.02 — python queue queue producer consumer](lessons/03.02-python-queue-queue-producer-consumer.md) | `python3 .../module-03.py --lesson 03.02` |
| [03.03 — threads and worker lifecycle](lessons/03.03-threads-and-worker-lifecycle.md) | `python3 .../module-03.py --lesson 03.03` |
| [03.04 — messages commands and events](lessons/03.04-messages-commands-and-events.md) | `python3 .../module-03.py --lesson 03.04` |
| [03.05 — TodoCompleted event contract](lessons/03.05-todocompleted-event-contract.md) | `python3 .../module-03.py --lesson 03.05` |
| [03.06 — durability and acknowledgment semantics](lessons/03.06-durability-and-acknowledgment-semantics.md) | `python3 .../module-03.py --lesson 03.06` |
| [03.07 — SQLite transactional outbox](lessons/03.07-sqlite-transactional-outbox.md) | `python3 .../module-03.py --lesson 03.07` |
| [03.08 — retry poliCIes and poison messages](lessons/03.08-retry-policies-and-poison-messages.md) | `python3 .../module-03.py --lesson 03.08` |
| [03.09 — dead letter queues and replay](lessons/03.09-dead-letter-queues-and-replay.md) | `python3 .../module-03.py --lesson 03.09` |
| [03.10 — idempotent consumer and deduplication](lessons/03.10-idempotent-consumer-and-deduplication.md) | `python3 .../module-03.py --lesson 03.10` |
| [03.11 — rabbitmq exchange queue routing key](lessons/03.11-rabbitmq-exchange-queue-routing-key.md) | `python3 .../module-03.py --lesson 03.11` |
| [03.12 — python publisher and consumer integration](lessons/03.12-python-publisher-and-consumer-integration.md) | `python3 .../module-03.py --lesson 03.12` |
| [03.13 — docker compose multi service topology](lessons/03.13-docker-compose-multi-service-topology.md) | `python3 .../module-03.py --lesson 03.13` |
| [03.14 — competing consumers and scaling](lessons/03.14-competing-consumers-and-scaling.md) | `python3 .../module-03.py --lesson 03.14` |
| [03.15 — queue depth and age observability](lessons/03.15-queue-depth-and-age-observability.md) | `python3 .../module-03.py --lesson 03.15` |
| [03.16 — failure injection and recovery](lessons/03.16-failure-injection-and-recovery.md) | `python3 .../module-03.py --lesson 03.16` |
| [03.17 — broker security TLS and secrets](lessons/03.17-broker-security-tls-and-secrets.md) | `python3 .../module-03.py --lesson 03.17` |
| [03.18 — architecture review and delivery guarantees](lessons/03.18-architecture-review-and-delivery-guarantees.md) | `python3 .../module-03.py --lesson 03.18` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
