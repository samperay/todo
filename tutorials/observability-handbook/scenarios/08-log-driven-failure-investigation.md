# Scenario 08: Log-driven failure investigation

**Difficulty:** guided → independent → incident commander. **Safety:** disposable local environment only; feature flags default OFF; do not use production credentials.

## Incident ticket

A user reports symptoms consistent with **log-driven failure investigation**. Your task is to determine impact, gather evidence, identify likely root cause, restore service, and verify recovery. Do not assume the fault until evidence supports it.

## Preparation and injection

Emit controlled test errors with request IDs. Record the exact start time and Git SHA. If this requires instrumentation not currently present, implement it behind an explicit development-only flag in a separate branch; skip injection until safe.

## Level 1 — Guided

1. Record baseline `up{job="todo-api"}`, request rate, 5xx percentage, and P95 by handler.
2. Inject the fault safely; compare before/after time windows.
3. Expected signal: Log errors correlate with 5xx metric.
4. Investigation direction: Search Loki/JSON logs and correlate timestamps.
5. Recovery: Remove fault; verify error disappearance.

## Level 2 — Independent

Without the hints, write the first three PromQL queries you would execute, the first log filter you would try, and the evidence that would disprove your leading hypothesis.

## Level 3 — Production-style challenge

Act as on-call SRE: declare impact, identify affected endpoints, choose mitigation over perfect diagnosis when warranted, communicate status, and create a five-event timeline. Distinguish telemetry failures from user-facing failures.

<details><summary>Hints and suggested checks (open after attempting)</summary>

- Start with `up{job="todo-api"}` and `sum(rate(http_requests_total{job="todo-api"}[5m]))`.
- Compare `sum by (handler,status)(rate(http_requests_total{job="todo-api"}[5m]))`.
- Check container logs and changes made just before the symptoms began.
- Do not treat `No data` as equivalent to numeric zero.
- Confirm recovery with new samples and successful business requests.

</details>

## Deliverable

A one-page incident report: symptoms, user impact, timeline, hypotheses, evidence, root cause (or unknown), mitigation, validation, and prevention actions.
