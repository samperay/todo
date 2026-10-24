# Module 03 — Asynchronous Processing And Event Driven Architecture

**Scope:** Producer/consumer, acknowledgment and restart loss.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Asynchronous Processing And Event Driven Architecture**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Producer/consumer, acknowledgment and restart loss**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [03.01-synchronous-versus-asynchronous-requests](lessons/03.01-synchronous-versus-asynchronous-requests.md) | Synchronous versus asynchronous requests | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.02-python-queue-queue-producer-consumer](lessons/03.02-python-queue-queue-producer-consumer.md) | Python queue.Queue producer/consumer | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.03-threads-and-worker-lifecycle](lessons/03.03-threads-and-worker-lifecycle.md) | Threads and worker lifecycle | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.04-messages-commands-and-events](lessons/03.04-messages-commands-and-events.md) | Messages, commands, and events | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.05-todocompleted-event-contract](lessons/03.05-todocompleted-event-contract.md) | TodoCompleted event contract | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.06-durability-and-acknowledgment-semantics](lessons/03.06-durability-and-acknowledgment-semantics.md) | Durability and acknowledgment semantics | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.07-sqlite-transactional-outbox](lessons/03.07-sqlite-transactional-outbox.md) | SQLite transactional outbox | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.08-retry-policies-and-poison-messages](lessons/03.08-retry-policies-and-poison-messages.md) | Retry policies and poison messages | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.09-dead-letter-queues-and-replay](lessons/03.09-dead-letter-queues-and-replay.md) | Dead-letter queues and replay | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.10-idempotent-consumer-and-deduplication](lessons/03.10-idempotent-consumer-and-deduplication.md) | Idempotent consumer and deduplication | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.11-rabbitmq-exchange-queue-routing-key](lessons/03.11-rabbitmq-exchange-queue-routing-key.md) | RabbitMQ exchange, queue, routing key | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.12-python-publisher-and-consumer-integration](lessons/03.12-python-publisher-and-consumer-integration.md) | Python publisher and consumer integration | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.13-docker-compose-multi-service-topology](lessons/03.13-docker-compose-multi-service-topology.md) | Docker Compose multi-service topology | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.14-competing-consumers-and-scaling](lessons/03.14-competing-consumers-and-scaling.md) | Competing consumers and scaling | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.15-queue-depth-and-age-observability](lessons/03.15-queue-depth-and-age-observability.md) | Queue depth and age observability | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.16-failure-injection-and-recovery](lessons/03.16-failure-injection-and-recovery.md) | Failure injection and recovery | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.17-broker-security-tls-and-secrets](lessons/03.17-broker-security-tls-and-secrets.md) | Broker security, TLS, and secrets | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |
| [03.18-architecture-review-and-delivery-guarantees](lessons/03.18-architecture-review-and-delivery-guarantees.md) | Architecture review and delivery guarantees | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
