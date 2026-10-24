# Todo Architecture — Current Baseline vs Possible Target

## Observed local development baseline (verify branch)

```text
Browser (React + localStorage token)
    | HTTP to :5173
    v
Vite dev server /api proxy
    | forwards to :8000
    v
FastAPI routes → services → repositories → SQLite file
    |
    +-- Prometheus /metrics endpoint (existing implementation; inspect current branch)
```

**Boundaries:** Browser state and localStorage are client-side; FastAPI authenticates bearer tokens; SQLite is durable local application storage. Vite is a dev server, not a production load balancer.

## Proposed event-driven extension — not implemented by this handbook

```text
Browser → FastAPI → [one SQLite transaction: Todo change + outbox event]
                               |
                               v
                         Outbox publisher
                               |
                               v
                            RabbitMQ
                               |
                               v
                      Notification worker → Email simulator
```

**Critical guarantee:** The Todo change and outbox insert must be atomic. Publishing and consuming can be retried; consumers must tolerate duplicates. An in-memory queue is only a teaching aid.

## Possible deployment evolution — design only

```text
Browser → production static frontend / gateway → FastAPI replicas
                                                 |
                                                 v
                                          shared managed database
```

Do not assume multiple independent SQLite files provide a shared database. Document migration and recovery before replica scaling.

## Architecture questions to revisit

- How do we handle token lifecycle and XSS risks?
- What data consistency guarantees are required?
- What is the cost/benefit of an external broker?
- Which SLOs represent successful user actions?
- What is the backup and restore plan?
- Which parts can fail without blocking Todo CRUD?
