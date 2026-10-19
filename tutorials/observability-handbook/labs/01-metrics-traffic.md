# Lab 01 — Traffic, errors, and latency

## 1. Request counts and RPS

Start from Lab 00. Generate bounded requests to a route that **actually exists**; `GET /` is only an example and may return 404, which still counts as an HTTP request if instrumented:

```bash
for i in $(seq 1 20); do curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/; done
```

Run in Prometheus:

```promql
sum by (method,status) (http_requests_total{job="todo-api"})
sum(rate(http_requests_total{job="todo-api"}[5m]))
sum by (handler) (rate(http_requests_total{job="todo-api"}[5m]))
```

**Interpretation:** Counters are cumulative since the process reset; `rate` is average per second over the window, not instantaneous RPS. Counter resets are handled by `rate` when sufficient samples exist.

## 2. Error counts vs. error rate

A 404 is a client-side status, not a 5xx. Test a nonexistent path to observe 404 without intentionally damaging the service. To test 5xx, first add a **development-only**, disabled-by-default fault endpoint or use an isolated test app; do not claim the current Todo API already has one.

```promql
sum by (status) (http_requests_total{job="todo-api"})
sum(rate(http_requests_total{job="todo-api",status=~"5.."}[5m]))
100 * sum(rate(http_requests_total{job="todo-api",status=~"5.."}[5m]))
  / sum(rate(http_requests_total{job="todo-api"}[5m]))
```

**Caveat:** No 5xx series can yield *no data*, not numeric zero; no traffic can make a ratio undefined. Decide explicitly how your dashboard should handle both cases.

## 3. Latency percentiles

```promql
histogram_quantile(0.95,
  sum by (le,handler) (
    rate(http_request_duration_seconds_bucket{job="todo-api"}[5m])
  )
)
```

Units are seconds. Histograms estimate quantiles from bucket boundaries. The global P95 is not the arithmetic average of per-handler P95s.

**Controlled latency exercise (requires code change):** Add a local-only delay behind `ENABLE_OBS_LABS=true`, with a bounded delay and an explicit non-production environment check. Restart, generate requests to that endpoint, compare P50/P95, then remove or disable the feature. Do not insert sleeps into normal production handlers.

## Independent challenge

Without looking at the query examples, calculate GET requests/second, 5xx percentage, and P95 by handler. Capture results before and after a traffic burst.

## Incident challenge

An API is scrapeable (`up=1`) but 25% of calls fail. Is it an incident? Identify status codes, affected handlers, request volume, and a likely mitigation. **Do not use `up` as a business availability SLI.**
