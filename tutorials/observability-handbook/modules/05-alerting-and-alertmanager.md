# Module 05 — Alerting And Alertmanager

**Prerequisite:** Previous module. **Lab environment:** development-only Todo API and observability stack.

> For every exercise, save commands, screenshots or query results, and a 2–3 sentence interpretation. When an endpoint/feature is not yet implemented, implement it on a disposable branch before testing.

## Class 17: Prometheus alert rules

### Concept
expr, for, labels, annotations; inactive, pending, firing.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Write an up==0 alert and test the pending interval.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **prometheus alert rules** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Distinguish three evaluations from three elapsed minutes. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 18: Service-level alerts

### Concept
5xx percentage, latency, traffic minimums, burn rates; alert on user impact.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Create a sustained high-5xx rule.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **service-level alerts** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Explain why up==1 can coexist with an outage. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 19: Alertmanager routing

### Concept
Receivers, grouping, deduplication, inhibition, silences, repeat intervals.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Run Alertmanager locally and inspect alert delivery.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **alertmanager routing** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Avoid routing test notifications to production Slack. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.

## Class 20: Slack alerts and runbooks

### Concept
Secure webhook delivery, severity, ownership, runbook links, actionable alerts.

**Why it matters:** An SRE must separate measurement from inference, then verify hypotheses with evidence.

### Level 1 — Guided lab
1. Confirm the stack is running: `docker compose ps` and `curl -fsS http://127.0.0.1:8000/metrics | head`.
2. Open Prometheus at `http://127.0.0.1:9090`, use the expression browser, and record the query and result.
3. Send a test notification to a dedicated test channel if credentials are available.
4. Write down what changed, what stayed constant, and what evidence supports your conclusion.

### Level 2 — Independent exercise
Without copying a solution, produce a short note explaining **slack alerts and runbooks** using one metric, query, configuration snippet, or diagram from your local environment. Define a pass/fail check and capture its output.

### Level 3 — Incident challenge
**Scenario:** Write an actionable runbook with validation and rollback. Form two competing hypotheses, select the first measurement to distinguish them, and document how you would validate a fix.

### Review questions
1. What does the observed signal prove, and what does it *not* prove?
2. How could the measurement be missing or misleading?
3. What would change if there were five replicas instead of one?

**Done when:** You can explain the concept, show one reproducible observation, and state a limitation.
