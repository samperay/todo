# Module 06 — Application Observability

**Prerequisite:** Previous module. **Lab environment:** development-only Todo API and observability stack.

> For every exercise, save commands, screenshots or query results, and a 2–3 sentence interpretation. When an endpoint/feature is not yet implemented, implement it on a disposable branch before testing.

## Class 21: FastAPI middleware instrumentation

### Concept
Instrument completed requests, in-flight gauge, handler and status; exclude /metrics.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Review Todo API middleware and compare before/after request metrics.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **fastapi middleware instrumentation** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain how uncaught exceptions affect request metrics. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 22: Instrumenting business operations

### Concept
Track todo creates/reads/errors without IDs or user identifiers in labels.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Propose todo_operations_total{operation,result}.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **instrumenting business operations** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Reject high-cardinality labels like todo_id. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 23: Database monitoring

### Concept
Query duration, pool utilization, slow queries, errors, and DB exporter options.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Instrument one database operation in a local-only branch.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **database monitoring** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Differentiate slow SQL from pool wait time. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 24: Load generation and profiling

### Concept
Repeatable load, concurrency, baselines, saturation, safe testing boundaries.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Generate bounded local traffic with a script.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **load generation and profiling** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain why localhost load is not production capacity proof. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.
