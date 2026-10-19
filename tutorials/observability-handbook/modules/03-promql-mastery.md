# Module 03 — Promql Mastery

**Prerequisite:** Previous module. **Lab environment:** development-only Todo API and observability stack.

> For every exercise, save commands, screenshots or query results, and a 2–3 sentence interpretation. When an endpoint/feature is not yet implemented, implement it on a disposable branch before testing.

## Class 08: Selectors and label matchers

### Concept
=, !=, =~, !~; selectors choose time series; regex matching is anchored.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Query GET and status=~"5.." series.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **selectors and label matchers** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain absent data versus zero requests. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 09: Aggregation and grouping

### Concept
sum, avg, max, count; by and without preserve or remove dimensions.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Compare sum(http_requests_total) with sum by (method)(...).
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **aggregation and grouping** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Calculate grouped values from a provided table. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 10: Rates and counter resets

### Concept
rate calculates per-second slope over range; increase estimates growth; counters can reset.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Generate traffic and query rate(...[5m]).
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **rates and counter resets** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain why raw counter values are not RPS. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 11: Histogram quantiles

### Concept
Classic histogram buckets use le; histogram_quantile estimates quantiles from bucket rates.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Calculate P95 by handler and compare with global P95.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **histogram quantiles** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain why P99 may be inaccurate with coarse buckets. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 12: PromQL for incidents

### Concept
Join filtering, aggregation, rates, ratio arithmetic, and absent-series checks.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Build 5xx percentage and per-handler request-rate queries.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **promql for incidents** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Guard against division by zero and low traffic. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.
