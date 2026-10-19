# PromQL cookbook — Todo API

Use actual metric names and labels from `/metrics`; these examples assume the instrumented names discussed in the course.

```promql
# Target scrape health
up{job="todo-api"}

# Counter totals (not RPS)
sum by (method,status) (http_requests_total{job="todo-api"})

# Total RPS over five minutes
sum(rate(http_requests_total{job="todo-api"}[5m]))

# Per-handler RPS
sum by (handler) (rate(http_requests_total{job="todo-api"}[5m]))

# 5xx RPS
sum(rate(http_requests_total{job="todo-api",status=~"5.."}[5m]))

# 5xx error percentage (only meaningful with nonzero traffic)
100 * sum(rate(http_requests_total{job="todo-api",status=~"5.."}[5m]))
  / sum(rate(http_requests_total{job="todo-api"}[5m]))

# Estimated P95 in seconds by handler
histogram_quantile(0.95,
  sum by (le,handler) (rate(http_request_duration_seconds_bucket{job="todo-api"}[5m])))

# Active requests by method
sum by (method) (http_requests_in_progress{job="todo-api"})

# Requests increased over five minutes (estimated)
sum(increase(http_requests_total{job="todo-api"}[5m]))

# Detect absence of target time series
absent(up{job="todo-api"})
```

## Query pitfalls

- `sum(http_requests_total)` adds lifetime counters, not a rate.
- `sum by (method)` returns a separate series per method; `sum()` collapses labels.
- `rate` needs multiple samples; a newly started app may yield no data.
- `up=1` means a successful metrics scrape, not a healthy business API.
- `up=0` is different from an absent target; `absent()` handles the latter.
- Histogram buckets are cumulative. Always retain `le` for classic `histogram_quantile` aggregation.
- P95 from a histogram is an approximation; global P95 cannot be calculated by averaging per-handler P95s.
- `status=~"5.."` matches three-character 5xx codes; 4xx are excluded.
- Counter resets and process restarts affect raw totals; `rate` handles detectable resets.
- Request labels must avoid high-cardinality values such as raw Todo IDs.
