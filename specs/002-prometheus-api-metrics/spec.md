# Feature Specification: Prometheus API Metrics

**Feature Branch**: `002-prometheus-api-metrics`

**Created**: 2026-10-17

**Status**: Draft

**Input**: User description: "Add observability to the Todo API so operators can monitor API traffic, request latency, HTTP errors, and active requests using Prometheus. Metrics must be exposed through a Prometheus-compatible endpoint without changing existing Todo API behavior. The metrics should support visualization of traffic, latency, errors, and saturation in Grafana."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Scrape API metrics (Priority: P1)

An operator points a Prometheus-compatible collector at the Todo API and receives a current snapshot of API measurements in the text format that collector already understands. No existing todo action changes to make that snapshot available.

**Why this priority**: Nothing else in this feature is usable until an operator can collect the measurements from a stable scrape target.

**Independent Test**: With the API running and no collector installed, request the metrics snapshot and confirm it is a successful Prometheus-compatible document. Confirm that scrape does not call a Todo or User repository, a database session, or an external network client. Then perform one existing todo action and confirm its result is unchanged from before this feature.

**Acceptance Scenarios**:

1. **Given** the API is running, **When** an operator requests the metrics snapshot, **Then** the response is successful and is a Prometheus-compatible text document that a standard collector can ingest without a custom translation step.
2. **Given** the API has handled no todo traffic since startup, **When** an operator requests the metrics snapshot, **Then** the document is still valid and reports no completed API traffic.
3. **Given** a person uses an existing todo action, **When** that action succeeds or fails as it does today, **Then** the status, payload, and access rules for that action are the same as they were before metrics existed.
4. **Given** an operator requests the metrics snapshot repeatedly, **When** each scrape completes, **Then** those scrapes do not appear as todo API traffic in the measurements.
5. **Given** the API is running, **When** an operator requests the metrics snapshot, **Then** producing it performs no database query and no external network call, and synchronous snapshot rendering does not run on the async event loop.

---

### User Story 2 - Monitor traffic and HTTP errors (Priority: P1)

An operator sees how many API requests completed and how many of those finished with an HTTP error, split so client errors and server errors can be told apart. Counts increase only when a request finishes, and they can be grouped by the kind of request.

**Why this priority**: Request volume and error count are the first signals an operator uses to decide whether the API is healthy. They are useful as soon as the snapshot can be scraped.

**Independent Test**: Send a known mix of successful todo requests, rejected requests, and requests that fail inside the API. Scrape the snapshot and confirm the completed-request total and the client-error and server-error totals match that mix, grouped by request kind.

**Acceptance Scenarios**:

1. **Given** a set of API requests has completed, **When** an operator reads the snapshot, **Then** the completed-request count equals the number of completed requests, excluding scrapes of the metrics snapshot.
2. **Given** some completed requests returned a client error and some returned a server error, **When** an operator reads the snapshot, **Then** client errors and server errors are counted separately and successful requests are not counted as errors.
3. **Given** requests used different methods and different API actions, **When** an operator reads the snapshot, **Then** counts can be grouped by method and by action without a separate series for each individual resource identifier.
4. **Given** a request is rejected or fails, **When** the caller receives that error, **Then** the error the caller sees is the same error they would have seen before metrics were added.

---

### User Story 3 - Monitor request latency (Priority: P1)

An operator sees how long API requests take to finish, well enough to judge a typical request and the slow tail. Latency is recorded for successful and failed requests.

**Why this priority**: A rising error count does not show a slow API. Latency is independently useful for the same scrape target and the same traffic.

**Independent Test**: Complete a known set of fast and slow API requests, scrape the snapshot, and confirm each completed request adds one histogram observation. Confirm the exposition includes buckets, count, and sum so Prometheus can estimate P50 and P95 with `histogram_quantile()`. Do not require that estimate to lie between the fastest and slowest sample.

**Acceptance Scenarios**:

1. **Given** API requests have completed, **When** an operator reads the snapshot, **Then** each completed request, except a metrics scrape, contributes its duration from arrival to response.
2. **Given** both successful and failed requests completed, **When** an operator summarizes latency, **Then** both outcomes are included and can be separated by outcome.
3. **Given** the recorded durations, **When** an operator charts them, **Then** Prometheus can estimate P50 and P95 request latency with `histogram_quantile()` over `http_request_duration_seconds_bucket` for the chosen time window. The application does not calculate those exact percentiles.
4. **Given** requests for different actions, **When** an operator reads latency, **Then** it can be grouped by method and action, and individual resource identifiers do not create their own series.

---

### User Story 4 - Monitor active requests (Priority: P2)

An operator sees how many API requests are in progress at scrape time, which shows whether the API is saturated even before those requests finish.

**Why this priority**: In-progress work explains saturation that completed-request counts and latency only show after the fact. Traffic, errors, and latency already give a usable health view without it.

**Independent Test**: Start several requests and hold them open, scrape while they are in progress, then let them finish and scrape again. The in-progress count matches the open requests and returns to the prior level when they finish.

**Acceptance Scenarios**:

1. **Given** one or more API requests are in progress, **When** an operator scrapes during that window, **Then** the active-request measurement equals the number of API requests still open, excluding the scrape itself.
2. **Given** those requests later succeed or fail, **When** an operator scrapes after they have all finished, **Then** the active-request measurement has decreased by the number that finished.
3. **Given** a request ends in a client error, a server error, or a disconnected caller, **When** it is no longer in progress, **Then** it is no longer included in the active-request measurement.
4. **Given** no API requests are in progress, **When** an operator scrapes, **Then** the active-request measurement is zero.

---

### User Story 5 - Provide metrics for operational dashboards (Priority: P2)

An operator uses the scraped measurements to build panels for traffic, latency, errors, and saturation, without changing the Todo API again. Grafana and any other dashboard product stay outside this feature.

**Why this priority**: The measurements exist so operators can see them over time. The panel shapes depend on the scrape data from the earlier stories.

**Independent Test**: After a known set of API traffic, confirm the snapshot contains series for request rate, latency percentiles, error rate, and in-progress requests, with the labels defined for each series. Confirm the repository contains no dashboard file.

**Acceptance Scenarios**:

1. **Given** Prometheus is collecting the snapshot on a regular interval, **When** an operator charts request rate, **Then** the chart shows completed API requests per unit of time and can be split by method, action, and outcome.
2. **Given** the same collection, **When** an operator charts latency, **Then** the chart can show a middle value and a slow-tail value over the selected window.
3. **Given** the same collection, **When** an operator charts errors, **Then** the chart can show the share or rate of client errors and of server errors separately from successful requests.
4. **Given** the same collection, **When** an operator charts saturation, **Then** the chart shows how many API requests were in progress over time.
5. **Given** these four charts, **When** the operator views them, **Then** no chart contains todo titles, descriptions, bearer tokens, or a series per individual resource identifier.

---

### Edge Cases

- A request that never receives a response, because the caller disconnects or the attempt is abandoned, still stops counting as active once the API is no longer handling it, and does not leave the active count elevated.
- Requests that complete at the same time each change the completed, error, latency, and active measurements once, with no lost or double count.
- A failing attempt to record a measurement does not change the todo response the caller receives.
- Actions that address a specific todo, including unknown identifiers, share one series for that action. The identifier itself is not a measurement label.
- Client mistakes, missing identification, and missing todos count as client errors. Unexpected failures count as server errors. The caller's existing error behavior stays the same.
- The metrics snapshot omits todo contents, bearer tokens, and any other secret or personal value.
- Scraping the snapshot while other requests are in flight does not change those requests and does not count the scrape as one of them.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST publish a single metrics snapshot that a Prometheus-compatible collector can scrape and store without custom translation.
- **FR-002**: The snapshot MUST be available to operators without using a person's todo access credential.
- **FR-003**: The snapshot MUST include the count of completed API requests.
- **FR-004**: The snapshot MUST include HTTP client errors and HTTP server errors as separate counts. Successful responses MUST NOT be counted as errors.
- **FR-005**: The snapshot MUST include request duration for completed API requests as a Prometheus histogram so Prometheus can estimate a middle value and a slow-tail value with `histogram_quantile()` over a time window. The application MUST NOT calculate exact percentiles.
- **FR-006**: The snapshot MUST include the number of API requests in progress at the time of the scrape.
- **FR-007**: Completed-request, error, and latency measurements MUST be groupable by HTTP method, API action, and response outcome. The active-request measurement MUST be groupable by HTTP method only. It MUST NOT be labeled by API action or response outcome.
- **FR-008**: Completed-request and latency labels MUST identify the API action, not the individual resource identifier, todo title, description, or any caller credential. The active-request measurement MUST be labeled only by HTTP method.
- **FR-009**: Scrapes of the metrics snapshot MUST NOT be included in the traffic, error, latency, or active-request measurements.
- **FR-010**: Existing todo actions MUST keep their current access rules, status outcomes, and response contents. This feature MUST NOT add, remove, or redefine a todo action.
- **FR-011**: A failure while recording or publishing measurements MUST NOT change the outcome of the todo action that was in progress.
- **FR-012**: The published measurements MUST be sufficient for operational dashboard panels of request rate, latency percentiles, error rate, and in-progress requests, using a Prometheus-compatible source. This feature does not include a dashboard product.
- **FR-013**: The snapshot MUST NOT contain todo titles, descriptions, bearer tokens, or other secret or personal values.

### Key Entities *(include if feature involves data)*

- **Metrics snapshot**: The document an operator or collector reads. It contains the current traffic, latency, error, and active-request measurements and nothing about todo contents.
- **Completed-request measurement**: A count of finished API requests, distinguishable by method, action, and whether the outcome was success, client error, or server error.
- **Latency measurement**: The time from request arrival to response for each completed API request, retained so middle and slow-tail values can be charted and split by method, action, and outcome.
- **Active-request measurement**: How many API requests are still being handled, distinguishable by HTTP method only.
- **API action**: The stable kind of request, such as listing todos or retrieving one todo, shared by every identifier for that kind of request.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Producing a metrics snapshot performs no database queries and no external network calls. Synchronous Prometheus snapshot rendering does not run on the async event loop.
- **SC-002**: After a controlled set of 100 completed API requests with a known mix of successes, client errors, and server errors, the snapshot's completed and error totals match that mix exactly, excluding metrics scrapes.
- **SC-003**: `http_request_duration_seconds` is exposed as a Prometheus histogram. The exposition contains `http_request_duration_seconds_bucket`, `http_request_duration_seconds_sum`, and `http_request_duration_seconds_count`. Default prometheus-client histogram buckets are acceptable. Prometheus can estimate P50 and P95 request latency using `histogram_quantile()` over the exposed `http_request_duration_seconds_bucket` series. The application does not calculate exact percentiles, and the estimate is not required to fall between the fastest and slowest observed samples.
- **SC-004**: While 20 API requests are held open, a scrape reports 20 active API requests. After all 20 finish, the next scrape reports the prior active count.
- **SC-005**: Existing todo acceptance checks pass at the same rate as before this feature, with no change in status or response content for those actions.
- **SC-006**: An operator can build four operational dashboard panels—request rate, latency percentiles, error rate, and in-progress requests—from the scraped measurements alone, with no further change to the Todo API. This feature does not include Grafana.
- **SC-007**: In a review of the snapshot after traffic that includes titles, descriptions, and access credentials, none of those values appear.

## Assumptions

- Operators are the audience. People using the todo actions do not need to see or understand the measurements.
- The metrics snapshot is reachable without a person's bearer credential so a collector can scrape it on an operator-controlled network. Network controls that limit who can reach the API are outside this feature. The snapshot stays free of todo contents and secrets so a scrape is not a data export.
- "HTTP errors" means both client errors and server errors, reported separately. Successful requests are traffic, not errors.
- Latency is the time the caller waits for the API to finish the response. P50 and P95 are Prometheus `histogram_quantile()` estimates over the exposed histogram, not exact percentiles calculated by the application.
- Saturation means API requests still in progress. Host resources such as CPU, memory, and database connections are out of scope.
- Measurements cover HTTP requests the API handles, except scrapes of the metrics snapshot. A shipped Grafana dashboard, hosted Prometheus, hosted Grafana, alert rules, logs, and traces are out of scope. The measurements must be enough for an operator to build the four panels.
- Completed-request and latency labels stay low-cardinality: method, API action, and outcome. The in-progress gauge is labeled only by method. Resource identifiers and user identifiers are never labels.
- This feature does not add business totals such as "todos created." Those would be a separate feature.
- Recording measurements is incidental to serving a request. If recording fails, the caller still receives the todo result the API would have produced.
- Collectors scrape on their own schedule. The API only needs to answer with the current snapshot when asked.
