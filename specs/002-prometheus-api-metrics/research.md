# Research: Prometheus API Metrics

## Decision: Put Prometheus metrics in an observability package

**Decision**: Application observability lives in `backend/src/todo_api/observability/`. This feature adds only `observability/metrics/`, split into `registry.py`, `definitions.py`, `middleware.py`, and `endpoint.py`. `main.py` wires the registry, middleware, and `GET /metrics`. It does not define instruments or call `generate_latest` itself. `prometheus-client` is imported only inside `observability/metrics/`.

**Rationale**: Traffic, latency, status, and in-progress work are properties of the HTTP call, not of todo rules. A dedicated package keeps that cross-cutting code off the todo and user routers and gives later specs a place for tracing or structured logging without putting those capabilities in this feature. Splitting registry, definitions, middleware, and exposition matches the responsibilities of this feature without empty modules for work that is not specified.

**Alternatives considered**:

- One module at `backend/src/todo_api/api/metrics.py`. Smaller, but it treats Prometheus as an API-package detail and leaves no boundary for later observability work.
- `prometheus-fastapi-instrumentator`. It wraps the same client, and its default latency series is not labeled by status. The spec requires latency to be separable by outcome.
- OpenTelemetry metrics, tracing, Loki, Tempo, Grafana, Alertmanager, or a Compose observability stack. Out of scope. Collectors scrape the text endpoint this feature publishes.
- Counting inside each route handler. That duplicates bookkeeping and is easy to miss on docs routes and unmatched paths. It would also import `prometheus-client` from API routes.

## Decision: Three series, status as the outcome label

**Decision**: Publish only these series:

| Series | Type | Labels |
| --- | --- | --- |
| `http_requests_total` | counter | `method`, `handler`, `status` |
| `http_request_duration_seconds` | histogram | `method`, `handler`, `status` |
| `http_requests_in_progress` | gauge | `method` |

`status` is the numeric HTTP status as a string on the counter and the histogram. Client errors are `4xx`. Server errors are `5xx`. Successes are every other completed status. On those two series, `handler` is the API action and `status` is the response outcome. The in-progress gauge has neither label.

**Rationale**: One counter labeled by status answers both total traffic and the client/server split without a second series that can drift from the total. The same status label on the histogram lets an operator separate slow successes from slow errors. The gauge is method-only so saturation stays a single level per method and cannot leak across route labels.

**Alternatives considered**:

- Separate `http_client_errors_total` and `http_server_errors_total` counters. They duplicate `http_requests_total` and can disagree if one observation is missed.
- An `outcome=success|client_error|server_error` label instead of `status`. That hides 401 versus 404 versus 422. Status still groups into the two error classes in the query.
- A summary instead of a histogram. Summaries do not aggregate percentiles across instances. A histogram does.

## Decision: Histogram exposition supports histogram_quantile()

**Decision**: `http_request_duration_seconds` uses the prometheus-client default buckets. The scrape publishes the histogram family: `http_request_duration_seconds_bucket`, `http_request_duration_seconds_sum`, and `http_request_duration_seconds_count`. Operators read a 50th and a 95th percentile with `histogram_quantile()` over those buckets. The percentile is a bucket estimate. It is not required to fall inside the minimum and maximum raw durations of a sample.

**Rationale**: `histogram_quantile()` needs cumulative buckets plus the `_sum` and `_count` series. Default buckets are enough for this API. Interpolated quantiles can sit outside the observed sample range, so the success check is that the estimate is produced from the exposition, not that it lies between the fastest and slowest request.

**Alternatives considered**:

- Storing every raw duration and computing an exact percentile in the API. That is not the Prometheus histogram contract and grows without a bound.
- Custom bucket boundaries. The spec does not require them.

## Decision: Handler label is a bounded route template

**Decision**: `handler` is the matched route's full path template, such as `/api/v1/todos/{todo_id}`. Requests that match no route use the single value `handler="unmatched"`. The allowed set is the application's route templates plus `unmatched`. Two todo ids share one series. Path parameters, raw URLs, titles, descriptions, tokens, and user ids are never labels.

**Rationale**: The spec forbids a series per resource id. A closed template set keeps cardinality at methods × templates × status codes.

**Alternatives considered**:

- The raw request path. A distinct id would create a distinct series and could copy identifiers into the scrape.
- A temporary `unmatched` label that later moves to the template. That leaks gauge value on the temporary series. See the in-progress decision.
- The route name or a hand-maintained action enum. The path template is already the public action identity.

## Decision: In-progress gauge is labeled only by method

**Decision**: `http_requests_in_progress` has one label, `method`. It has no `handler` and no `status`. `middleware.py` increments that method series when a non-scrape request enters and decrements the same series in `finally` when the request finishes, fails, or the caller disconnects.

**Rationale**: The gauge is a level. A method-only series cannot be split across route templates, so the increment and the decrement always name the same series. Route detail stays on the counter and the histogram, where the template is known after the request is handled.

**Alternatives considered**:

- Labeling the gauge with `method` and `handler`. That requires a stable template before the request is counted and can leak a count if the label changes before `finally`.
- Increment `unmatched` at entry and decrement the template at exit. This splits one request across two series.
- Omit the gauge until the response finishes. That hides saturation while the request is open.

## Decision: Do not record the scrape

**Decision**: Paths `/metrics` and `/metrics/` skip the counter, the histogram, and the gauge. The scrape itself is still a normal HTTP response.

**Rationale**: Counting scrapes would make request rate track the collector interval. Skipping both the slash and non-slash forms avoids a redirect or a second path showing up as traffic.

**Alternatives considered**:

- Recording scrapes under `handler="/metrics"`. Honest, but it fails the spec rule that scrapes do not appear as API traffic.
- A separate process port for metrics. That changes how the API is deployed and is not required for a compatible endpoint.

## Decision: One registry per app instance

**Decision**: `registry.py` returns a new `CollectorRegistry`. `create_app` stores it on `app.state` and passes it to the middleware and the endpoint. The process-global default registry is not used.

**Rationale**: The existing `client` fixture calls `create_app` once per test. A global registry would leak counts between tests and make exact total checks order-dependent.

**Alternatives considered**:

- The default `REGISTRY`. Simpler in production, unreliable for the exact-count tests this feature needs.
- Resetting the global registry in a fixture. That couples every test to metrics cleanup, including tests that should not know about this feature.

## Decision: Scrape rendering stays off the event loop

**Decision**: `endpoint.py` awaits `asyncio.to_thread(generate_latest, registry)` and returns those bytes with the client's current exposition content type (`text/plain; version=0.0.4; charset=utf-8`). The handler reads the registry only. It does not query the database or make an external network call. There is no Pydantic response model and no wall-clock scrape limit.

**Rationale**: The constitution says CPU-bound work must not block the event loop. Rendering is synchronous, so it runs off the event loop. The body is the Prometheus text protocol, not a JSON API model. Metric increments are atomic in-process updates, not waiting I/O, and stay inline.

**Alternatives considered**:

- A Pydantic model around the text. Collectors would no longer scrape the endpoint without translation.
- Calling `generate_latest` directly in the async route. Acceptable at this size, but it conflicts with the constitution wording.
- A background thread that caches the latest scrape. Extra staleness and no benefit at this cardinality.

## Decision: Metrics failures do not change application behavior

**Decision**: Instrumentation exceptions stay inside `middleware.py`. If recording the counter or histogram raises, the middleware still returns the response the app produced. The in-progress gauge still decrements the same label in `finally`. An unexpected exception from the app is recorded as status `500` when no response was produced, then re-raised so the existing error behavior is unchanged. A failure inside `endpoint.py` affects only the scrape request.

**Rationale**: The spec says a recording or publishing failure must not change the todo action that was in progress. The gauge must not stay elevated after a failure or a disconnect.

**Alternatives considered**:

- Letting a metrics exception replace the todo response. That violates the spec directly.
- Swallowing application exceptions inside the middleware. That would hide the existing 500 behavior.

## Decision: No new settings, dashboard, or domain counters

**Decision**: Metrics are always on. No environment flag, no bearer auth on `/metrics`, and no committed Grafana dashboard, Prometheus server config, Alertmanager rule, or domain counter such as todos created. Network policy in front of the process stays outside this feature.

**Rationale**: The spec assumes collectors scrape without a person's todo credential, and that charts are operator work. A disable flag, a hosted collector, and domain counters would expand the feature. There is no new secret, so settings do not change.

**Alternatives considered**:

- Requiring the same bearer token as todos. Standard collectors would need a person's credential, and that credential must not be copied into labels.
- Shipping a Grafana JSON file or a Compose stack. Later specifications own that infrastructure.
