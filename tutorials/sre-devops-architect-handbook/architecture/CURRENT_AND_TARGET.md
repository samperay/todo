# Current and proposed architecture

**Current, subject to branch verification:** React/TypeScript/Vite browser app → FastAPI HTTP API → service/repository → SQLite. Bearer authentication and Prometheus `/metrics` exist in the baseline.

**Proposed only:** TodoCompleted event → transactional outbox → durable broker → notification worker → Slack/email. Kubernetes/cloud are later optional deployment exercises, not present-day guarantees.

**Rule:** Real source code overrides diagrams and simulated labs.
