# Lab 03 — Dashboards, logs, and traces (incremental extension)

These components **are not assumed to exist in the current Todo branch**. Add each in a separate commit and confirm versions/configuration from the official project documentation appropriate to your installed release.

## A. Grafana

1. Add Grafana to Compose; persist `/var/lib/grafana` in a named volume.
2. Configure the Prometheus data source using **container networking** (`http://prometheus:9090`), not the host browser address.
3. Create four panels: total RPS, 5xx percentage, P95 by handler, and `up`.
4. Set appropriate units: requests/second, percent, seconds, and binary state.
5. Export dashboard JSON and keep it in version control.

## B. Structured logs + Loki

1. Add request ID, timestamp, method, route, status, and duration to development JSON logs; redact credentials and user content.
2. Add Loki and a compatible log collector. Prefer low-cardinality labels such as `service` and `environment`.
3. Query recent failures using a LogQL pattern adapted to your actual JSON fields:

```logql
{service="todo-api"} | json | status >= 500
```

4. Compare a 5xx spike in Prometheus with log messages in the same time range.

## C. OpenTelemetry + Tempo

1. Instrument FastAPI and database client with an OpenTelemetry SDK on a feature branch.
2. Export OTLP to a local collector, then to Tempo.
3. Trace a single GET request through application and database spans.
4. Put `trace_id` in JSON logs as a field, **not** as a Loki stream label.
5. Find a slow trace from a latency spike and verify whether database work explains it.

## Independent exercise

Build a dashboard with a service selector, then write a short investigation showing the same failure in a metric, a log, and a trace.

## Incident challenge

P99 rises after a deployment but the request rate is unchanged. Distinguish slow database operations from application CPU saturation using at least two signals.
