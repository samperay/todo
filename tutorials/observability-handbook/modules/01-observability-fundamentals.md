# Module 01 — Observability Fundamentals

**Prerequisite:** Lab setup. **Lab environment:** development-only Todo API and observability stack.

> For every exercise, save commands, screenshots or query results, and a 2–3 sentence interpretation. When an endpoint/feature is not yet implemented, implement it on a disposable branch before testing.

## Class 01: Monitoring versus observability

### Concept
Explain known-failure monitoring versus investigating unknown failures; signals, symptoms, and hypotheses.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Sketch a request path for Todo API and list three unknowns when it is slow.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **monitoring versus observability** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Compare successful /metrics scrapes with actual user success. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 02: Metrics, logs, and traces

### Concept
Metrics aggregate measurements; logs record events; traces connect work across components.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Map one Todo request to metric, JSON log, and trace span.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **metrics, logs, and traces** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Choose the best signal for a failed login versus slow database call. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 03: Golden signals and telemetry design

### Concept
Latency, traffic, errors, saturation; RED and USE methods; measurement boundaries.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Define four Todo API SLIs and where each originates.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **golden signals and telemetry design** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain why 200 OK on /metrics is not business availability. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.
