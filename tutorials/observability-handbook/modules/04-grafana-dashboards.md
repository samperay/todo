# Module 04 — Grafana Dashboards

**Prerequisite:** Previous module. **Lab environment:** development-only Todo API and observability stack.

> For every exercise, save commands, screenshots or query results, and a 2–3 sentence interpretation. When an endpoint/feature is not yet implemented, implement it on a disposable branch before testing.

## Class 13: Grafana architecture and data sources

### Concept
Prometheus is a data source; Grafana queries and visualizes but does not replace the TSDB.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Add Grafana container and Prometheus data source.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **grafana architecture and data sources** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain container DNS versus browser localhost. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 14: Dashboard design and variables

### Concept
Panels, legends, dashboard variables, templating, units and intervals.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Create RPS, error %, P95 panels.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **dashboard design and variables** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Design an endpoint selector that does not hide important failures. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 15: Investigating trends

### Concept
Time ranges, comparison windows, annotations, deploy correlation.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Simulate a traffic spike and locate its start.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **investigating trends** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain why 5-minute rate smooths short spikes. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 16: Dashboards as code

### Concept
Provision data sources and dashboards with version-controlled files.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Export a dashboard JSON and commit it.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **dashboards as code** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Recover dashboards after deleting a disposable Grafana container. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.
