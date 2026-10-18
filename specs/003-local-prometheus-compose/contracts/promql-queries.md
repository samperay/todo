# Contract: PromQL queries

Run these against `http://127.0.0.1:9090`. The window is one minute so a baseline scrape and the next scrape, 15 seconds apart, both fall inside it. The Phase 002 five-minute expressions remain valid for a longer look and are not the local verification window.

Labels stay `method`, `handler`, and `status` on `http_requests_total` and `http_request_duration_seconds`. `status` is the numeric code as text. `http_requests_in_progress` is not part of these three questions.

An empty result means the selector matched no series. It is not the number 0. Only the server-error query substitutes 0 for that empty case.

## Throughput

Completed API requests per second, split by method, action, and outcome:

```promql
sum by (method, handler, status) (rate(http_requests_total[1m]))
```

Verification uses the total of that rate and expects a number greater than 0 after the baseline-to-post-traffic increase:

```promql
sum(rate(http_requests_total[1m]))
```

Before any completed request has been stored, this result is empty.

## Client-error rate

```promql
sum(rate(http_requests_total{status=~"4.."}[1m]))
```

Successful responses are not in this selector. After the verification's HTTP 4xx response has been scraped, the result is a number greater than 0. If no 4xx series exists, the result is empty, not 0.

## Server-error rate

```promql
sum(rate(http_requests_total{status=~"5.."}[1m])) or vector(0)
```

When no 5xx series exists, the `rate()` selector is empty and `or vector(0)` returns the number 0. When 5xx series exist, the result is their per-second rate. The verification does not create a 5xx response, so the expected result is the number 0.

## Latency

Median:

```promql
histogram_quantile(
  0.50,
  sum by (le) (rate(http_request_duration_seconds_bucket[1m]))
)
```

95th percentile:

```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[1m]))
)
```

These are Prometheus estimates from the existing histogram. The application does not calculate them. The verification expects a numeric result for each after the baseline sample and the post-traffic sample are both inside the window. It does not require either estimate to lie between the fastest and slowest request.

## What a non-zero rate requires

`rate()` is the per-second increase between the first and last sample of one series inside the window. A series is `http_requests_total` plus one `method`, `handler`, and `status` combination. The counter must be higher on the later sample.

A newly created series with only one sample cannot produce a meaningful rate. `rate()` has no earlier sample to subtract, so Prometheus omits that series. The lone sample is the counter total at the first scrape, not an increase per second. Requests that created the series, and any other increments before that scrape, are already inside that total. They do not appear as a rate. A 4xx or success series that shows up for the first time on the post-traffic scrape therefore leaves `rate()` empty for that series.

The verification window avoids that:

- The baseline scrape already contains at least one `2xx` series and one `4xx` series.
- The next scrape, after at least 10 additional requests, contains those same series with higher values. The additional requests include successes and at least one HTTP 4xx, and they repeat the baseline label sets rather than only creating new ones.
- The `[1m]` window includes both scrapes, and the query runs before the baseline sample ages out.
- Two samples that both occur after the additional traffic, with no further requests between them, can show the same counter value. `rate()` over that pair can be 0 and does not satisfy this contract.
