# Metrics catalog

HTTP scrape contract: [metrics.openapi.yaml](./metrics.openapi.yaml). Label meanings: [../data-model.md](../data-model.md).

Collectors ingest the Prometheus text exposition format. The content type is `text/plain; version=0.0.4; charset=utf-8`.

## Series

### `http_requests_total`

- **Type**: counter
- **Help**: Completed HTTP requests.
- **Labels**: `method`, `handler`, `status`
- **Excluded**: requests whose path is `/metrics` or `/metrics/`

`status` is the numeric code as text. Sum series with `status=~"4.."` for client errors and `status=~"5.."` for server errors. Other statuses are successes.

### `http_request_duration_seconds`

- **Type**: histogram
- **Help**: HTTP request latency in seconds.
- **Labels**: `method`, `handler`, `status`
- **Buckets**: prometheus-client default buckets
- **Exposition**: `http_request_duration_seconds_bucket`, `http_request_duration_seconds_sum`, and `http_request_duration_seconds_count`. Prometheus can estimate P50 and P95 with `histogram_quantile()` over `http_request_duration_seconds_bucket`. The application does not calculate exact percentiles. Those estimates are bucket interpolations and are not required to fall between the fastest and slowest observed samples.
- **Excluded**: the same scrape paths as the counter

One completed request produces one histogram observation and one counter increment with the same labels.

### `http_requests_in_progress`

- **Type**: gauge
- **Help**: HTTP requests currently in progress.
- **Labels**: `method` only. This series MUST NOT include `handler` or `status`.
- **Label stability**: one request increments and decrements the same `method` series. The decrement runs in `finally`.
- **Excluded**: the same scrape paths

## Operational dashboard queries

These are the panels an operator can build from the snapshot. This feature does not include Grafana or any other dashboard product.

Request rate, split by method, handler, and status:

```promql
sum by (method, handler, status) (rate(http_requests_total[5m]))
```

95th percentile latency:

```promql
histogram_quantile(
  0.95,
  sum by (le, method, handler) (rate(http_request_duration_seconds_bucket[5m]))
)
```

Use `0.50` for the P50 estimate. Add `status` to the `sum by` clause to separate outcomes. The application does not compute either value.

Client-error rate:

```promql
sum(rate(http_requests_total{status=~"4.."}[5m]))
```

Server-error rate uses `status=~"5.."`.

In-progress requests:

```promql
sum by (method) (http_requests_in_progress)
```
