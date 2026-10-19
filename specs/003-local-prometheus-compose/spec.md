# Feature Specification: Local Prometheus Monitoring

**Feature Branch**: `feature/prometheus-server-integration`

**Created**: 2026-10-18

**Status**: Draft

**Input**: User description: "Add a reproducible local monitoring environment for the Todo API using Docker Compose and Prometheus. Developers should be able to start the Todo API and Prometheus together, have Prometheus scrape the existing /metrics endpoint every 15 seconds, inspect target health, and query request throughput, HTTP error rates, and latency using PromQL. Prometheus data should persist across container restarts. The solution should include configuration validation, documentation, and a repeatable verification procedure. Grafana and alerting are outside the scope of this feature."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start a healthy local scrape (Priority: P1)

A developer starts the Todo API and Prometheus together with one documented action and then sees Prometheus collecting the API's existing metrics endpoint on a 15-second cadence. The developer can tell whether that target is healthy without reading application logs.

**Why this priority**: Nothing else in this feature is useful until both processes are running and Prometheus is actually collecting the endpoint that already exists.

**Independent Test**: From a clean checkout, follow only the documented start steps. Confirm the Todo API answers a normal request at `http://127.0.0.1:8000`, Prometheus is reachable at `http://127.0.0.1:9090`, both published ports are bound to `127.0.0.1`, the API metrics target is shown as healthy, and the target reports a 15-second collection interval. Confirm this does not require a separate Prometheus installation or a hand-edited scrape address.

**Acceptance Scenarios**:

1. **Given** a developer has the project and the documented prerequisites, **When** they run the single documented start action, **Then** the Todo API is reachable at `http://127.0.0.1:8000` and Prometheus is reachable at `http://127.0.0.1:9090`. Both published ports are bound to `127.0.0.1` and are not published on every network interface.
2. **Given** both are running, **When** the developer inspects Prometheus target health, **Then** the Todo API metrics target is healthy and its scrape address is the existing metrics endpoint.
3. **Given** the target is healthy, **When** the developer inspects the target, **Then** its configured collection interval is 15 seconds.
4. **Given** Prometheus starts before the API is ready to answer, **When** the API later becomes ready, **Then** the target becomes healthy on a later collection without restarting Prometheus.
5. **Given** the API is stopped while Prometheus keeps running, **When** the developer inspects target health, **Then** the target is shown as unhealthy and the failed collection is visible. Stored samples already collected are kept.
6. **Given** the documented local address is already in use, **When** the developer runs the start action, **Then** startup fails with a visible error instead of reporting a healthy target that belongs to some other process.

---

### User Story 2 - Query throughput, errors, and latency (Priority: P1)

A developer who has generated a known amount of API traffic can answer three questions in Prometheus with PromQL: how much traffic the API completed, how often that traffic failed, and how long requests took.

**Why this priority**: A healthy scrape target only shows that collection works. The reason to run the local environment is to answer these three operational questions.

**Independent Test**: With the target healthy, send successful HTTP responses and at least one HTTP 4xx response. Wait for a successful scrape that contains both a successful-response counter series and a 4xx counter series. That scrape is the baseline. Then send at least 10 additional completed API requests, including successful requests and HTTP 4xx responses, that increase those same series. Wait for another successful scrape. Run the documented PromQL rate queries over a window that contains the baseline sample and that later sample, and confirm throughput and the client-error rate are non-zero numbers, the server-error query returns the number 0 rather than an empty result, and the latency query returns a median and a 95th percentile.

**Acceptance Scenarios**:

1. **Given** completed API requests have been collected, **When** the developer runs the documented throughput query, **Then** it returns the recent rate of completed API requests and can be split by method, action, and outcome.
2. **Given** the same collection includes rejected requests and no server failures, **When** the developer runs the documented error queries, **Then** client errors and server errors are reported as separate rates, successful requests are not counted as errors, the client-error rate is a non-zero number, and the server-error query returns the number 0.
3. **Given** no HTTP 5xx observations exist, including when a 5xx series has never been created, **When** the developer runs the documented server-error query, **Then** the query succeeds and returns the number 0. An empty result from a selector that matches nothing is not that number.
4. **Given** completed requests have been collected, **When** the developer runs the documented latency query, **Then** it returns a median latency and a 95th-percentile latency for the recent window, estimated from the latency measurements the API already publishes.
5. **Given** the API has handled no todo traffic since startup, **When** the developer runs the documented throughput and latency queries, **Then** each query succeeds. A selector that matches no series returns an empty result. That empty result is not the number 0 and is not a query error.
6. **Given** these queries, **When** the developer reads their results, **Then** the results do not contain todo titles, descriptions, or access credentials, and collections of the metrics endpoint are not counted as API traffic. The queries read the existing HTTP measurements and their current labels. They do not add or rename a series or a label.

---

### User Story 3 - Keep collected samples across restarts (Priority: P2)

A developer stops, starts, or recreates the local Prometheus container and can still query samples that were collected before that change. Todo rows stored by the API are a separate store. This feature does not make those rows survive an API restart.

**Why this priority**: A local environment that forgets its Prometheus history on every restart cannot be used to compare a change before and after a restart. Collection and queries are already useful before persistence is present. Keeping todo rows is a different capability and is not part of this feature.

**Independent Test**: Collect a known sample, record a query result that includes it, stop and start the Prometheus container, and run a query whose time range includes the earlier sample. The earlier sample is still returned. Recreate that container without deleting its stored data and confirm the same sample is still returned. Then remove the stored data on purpose and confirm a later start begins with an empty store and can become healthy again. Confirm this check does not require todo rows to survive an API restart.

**Acceptance Scenarios**:

1. **Given** Prometheus has stored samples from a healthy target, **When** the developer stops and starts the Prometheus container, **Then** a query for the period before the stop still returns those samples.
2. **Given** the same stored samples, **When** the developer recreates the Prometheus container without deleting its stored data, **Then** those samples remain queryable.
3. **Given** the developer explicitly deletes the stored Prometheus data, **When** they start the environment again, **Then** queries begin with an empty store, and the API target can become healthy again after new collections.
4. **Given** Prometheus is restarted while the API keeps running, **When** collection resumes, **Then** new samples are added and the samples from before the restart are still present.
5. **Given** the API container is stopped, started, or recreated, **When** the developer looks for todo rows saved before that change, **Then** this feature does not require those rows to remain. Prometheus samples already stored still follow the persistence rules above.

---

### User Story 4 - Validate the setup and repeat the check (Priority: P2)

A developer can check that the Prometheus configuration is usable before trusting a running stack, and a second developer can follow one written procedure to reach the same pass or fail conclusion.

**Why this priority**: The running stack demonstrates the feature once. Validation, documentation, and a fixed procedure are what make that result reproducible for the next developer. They depend on the behavior in the earlier stories.

**Independent Test**: Run the documented configuration check against the delivered configuration and confirm it passes. Run the same check against a configuration Prometheus would reject and confirm it fails. A developer who was not involved in the change then follows the written verification procedure, including its baseline scrape of both a successful-response series and a 4xx series, the additional traffic that raises those series, and one post-traffic scrape, and records the same pass or fail for target health, the 15-second interval, throughput, both error rates, latency, and persistence.

**Acceptance Scenarios**:

1. **Given** the delivered Prometheus configuration, **When** a developer runs the documented validation check, **Then** the check passes and the configuration it checked is the one the running stack loads.
2. **Given** a Prometheus configuration that is not valid, **When** a developer runs the same check, **Then** the check fails and does not report that configuration as a healthy running target.
3. **Given** the project documentation, **When** a new developer looks up this environment, **Then** they can find how to start and stop it, the loopback addresses, how to inspect target health, the three PromQL queries and the difference between an empty result and the number 0, how Prometheus samples survive a restart or recreation, that Todo API SQLite persistence is outside this feature, how to validate the configuration, and the verification procedure.
4. **Given** that written verification procedure, **When** a second developer follows it from a clean start, **Then** the procedure first sends successful HTTP responses and at least one HTTP 4xx response, waits for a successful scrape that contains both a successful-response counter series and a 4xx counter series, then generates at least 10 additional completed API requests, including successful requests and HTTP 4xx responses, that increase those same series, then waits for another successful scrape.
5. **Given** the baseline sample and the post-traffic sample, **When** the developer runs the documented rate queries, **Then** the rate window includes both samples. The additional traffic has increased the same counter series that existed in the baseline. Two scrapes that both occur after the additional traffic are not treated as enough to show a non-zero rate.
6. **Given** that pair of samples, **When** the developer finishes the procedure, **Then** they confirm all of the following, without inventing steps: the API target is healthy, the collection interval is 15 seconds, throughput is a non-zero number, the client-error rate is a non-zero number, the server-error query returns the number 0, latency returns a median and a 95th percentile, Prometheus samples remain queryable after a container restart or recreation, and the configuration check passes. The query checks are observable within 5 minutes of the target becoming healthy, and the full procedure finishes within 15 minutes.

---

### Edge Cases

- Prometheus starts before the API can answer. The target shows unhealthy until a later collection succeeds, then becomes healthy without a manual Prometheus restart.
- The API stops after collection has begun. Target health changes to unhealthy, the failure is visible, and samples already stored remain queryable.
- The developer restarts Prometheus, or recreates its container, without deleting stored data. Earlier samples remain queryable. Restarting the API process may start its in-memory measurements again; that does not remove samples Prometheus has already stored.
- The developer explicitly deletes stored Prometheus data. The next start collects into an empty store. That deletion is the reset path, not a failure of persistence.
- The documented local address is already taken. Startup fails visibly and does not treat an unrelated process as the healthy API target.
- Published ports bind to `127.0.0.1` by default. The Todo API is published at `127.0.0.1:8000` and Prometheus at `127.0.0.1:9090`. A default start does not publish either port on every network interface.
- No todo traffic has been collected yet. Throughput and latency queries succeed. Where their selectors match no series, the result is empty. That empty result is not the number 0. Latency has no numeric estimate until at least one completed API request has been collected.
- No HTTP 5xx observations exist. The documented server-error query still returns the number 0. A selector that matches no 5xx series is an absent series, and that absence alone is not the number 0.
- A rate query whose window contains only one sample of a counter returns an empty result. The verification procedure places the baseline scrape and the post-traffic scrape inside the documented window before treating throughput or the client-error rate as verified.
- Two scrapes that both occur after the verification traffic can show the same counter value when no further requests happen between them. A rate over that pair can be the number 0. The procedure does not use that pair as evidence of a non-zero request rate. The non-zero rate is the increase between the baseline sample and the sample that contains the traffic.
- The verification procedure sends successful HTTP responses and at least one HTTP 4xx response before the baseline scrape. It waits until a successful scrape contains both a successful-response counter series and a 4xx counter series. That scrape is the baseline. One successful request is not a sufficient baseline, because the 4xx series would then be missing. The procedure then sends at least 10 additional completed API requests, including successful requests and HTTP 4xx responses, that increase those same series, and waits for another successful scrape. It does not need a forced server failure, and it does not wait for a second scrape after the additional traffic.
- A collection of the metrics endpoint is not recorded as API traffic, and query results do not include todo contents or access credentials.
- Restarting or recreating the API container may discard todo rows in its local database. That loss is outside this feature. It does not remove Prometheus samples that were already stored.
- An invalid configuration fails validation. It is not left running as a healthy target.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A developer MUST be able to start the Todo API and Prometheus together with one documented Docker Compose action, and stop them with one documented Docker Compose action.
- **FR-002**: That start action MUST be enough to reproduce the environment from the project, given the documented prerequisites. A developer MUST NOT need to install Prometheus separately or type a scrape address by hand.
- **FR-003**: Prometheus MUST collect the Todo API's existing metrics endpoint.
- **FR-004**: The time between those collections MUST be 15 seconds.
- **FR-005**: A developer MUST be able to inspect whether the API metrics target is healthy, including the last collection outcome when it is not.
- **FR-006**: If Prometheus collects before the API is ready, the target MUST become healthy on a later collection without restarting Prometheus.
- **FR-007**: If the API cannot be collected, the target MUST be shown as unhealthy while Prometheus keeps already stored samples.
- **FR-008**: A developer MUST be able to query recent request throughput with PromQL, as the rate of completed API requests, and split that rate by method, action, and outcome. Those labels are the existing `method`, `handler`, and `status` labels on `http_requests_total`.
- **FR-009**: A developer MUST be able to query recent HTTP client-error and server-error rates separately with PromQL, using the existing `status` label on `http_requests_total`. Client errors are `4xx` statuses and server errors are `5xx` statuses. Successful responses MUST NOT be counted as errors. The documented server-error query MUST return the number 0 when no HTTP 5xx observations exist, including when a 5xx series has never been created.
- **FR-010**: A developer MUST be able to query recent median latency and 95th-percentile latency with PromQL, using the existing `http_request_duration_seconds` histogram and its `method`, `handler`, and `status` labels.
- **FR-011**: A documented query whose selector matches no series MUST succeed with an empty result. That empty result is an absent series, not the number 0, and it is not a query error. The documented server-error query is the exception: it MUST return the number 0 when no 5xx series is present.
- **FR-012**: Samples Prometheus has already stored MUST remain queryable after the Prometheus container is stopped and started, and after that container is recreated, unless the developer explicitly deletes the stored data.
- **FR-013**: Explicitly deleting the stored Prometheus data MUST be the way to start again with an empty store.
- **FR-014**: A documented check MUST validate the Prometheus configuration the stack loads. The check MUST pass for the delivered configuration and MUST fail for a configuration Prometheus would reject.
- **FR-015**: Project documentation MUST explain how to start and stop the environment, the loopback addresses, how to inspect target health, the three PromQL queries, the difference between an empty result and the number 0, that Prometheus samples survive a restart or recreation, that Todo API SQLite persistence is outside this feature, how to validate the configuration, and how to run the verification procedure.
- **FR-016**: A written verification procedure MUST, in order, send successful HTTP responses and at least one HTTP 4xx response, wait for a successful Prometheus scrape that contains both a successful-response counter series and a 4xx counter series and record that scrape as the baseline, generate at least 10 additional completed API requests, including successful requests and HTTP 4xx responses, that increase those same counter series, wait for another successful scrape, and run the documented PromQL rate queries over a window that contains both the baseline sample and that post-traffic sample. One successful request MUST NOT be treated as a sufficient baseline. The procedure MUST NOT treat two scrapes that both occur after the additional traffic as sufficient to show a non-zero request rate. It MUST then confirm target health, a 15-second collection interval, a non-zero throughput, a non-zero client-error rate, a server-error result of the number 0, a median latency, a 95th-percentile latency, persistence of Prometheus samples across a container restart or recreation, and a passing configuration check. A second developer MUST be able to record the same pass or fail result on each run. The baseline, the additional traffic, the one post-traffic scrape, and the queries MUST be achievable within 5 minutes of the target becoming healthy, and the full procedure MUST be achievable within 15 minutes.
- **FR-017**: This feature MUST NOT add a dashboard product, a hosted dashboard, alerting, or a production deployment. Grafana and alerting are outside this feature.
- **FR-018**: Existing todo actions and the existing metrics endpoint MUST keep their current access rules, status outcomes, and measurement meanings. This feature MUST NOT add, remove, or redefine a metric or a label. The preserved measurements are `http_requests_total` (`method`, `handler`, `status`), `http_request_duration_seconds` (`method`, `handler`, `status`), and `http_requests_in_progress` (`method` only).
- **FR-019**: The local configuration committed for this environment MUST NOT contain passwords, tokens, or todo contents.
- **FR-020**: If a documented local address is already in use, startup MUST fail visibly rather than report an unrelated process as the healthy API target.
- **FR-021**: Published ports MUST bind to `127.0.0.1` by default. The Todo API MUST be published at `127.0.0.1:8000` and Prometheus MUST be published at `127.0.0.1:9090`.
- **FR-022**: Prometheus samples MUST persist across container restarts and recreation, as required by FR-012. Persistence of the Todo API's SQLite database is outside this feature. Restarting or recreating the API container is not required to keep todo rows.

### Key Entities

- **Local monitoring stack**: The Todo API and Prometheus started and stopped together for one developer machine.
- **Scrape target**: The API's existing metrics endpoint as Prometheus collects it, including whether the latest collection succeeded and how often collection is attempted.
- **Stored sample**: A measurement Prometheus has kept from a collection. Stored samples are what remain queryable after a Prometheus container restart or recreation. They are not todo rows.
- **Operational query**: One of the three documented PromQL questions: request throughput, HTTP error rate, or latency. A result is either a number or an empty result. An empty result means the selector matched no series. The number 0 is a present value, and the documented server-error query uses that value when no 5xx series exists.
- **Configuration check**: The pass or fail result of validating the Prometheus configuration the stack loads.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer who already has the documented prerequisites can start the Todo API and Prometheus with one action and reach the API at `http://127.0.0.1:8000` and Prometheus at `http://127.0.0.1:9090` within 2 minutes, without installing Prometheus separately. Both published ports are bound to `127.0.0.1`.
- **SC-002**: Once the API is ready, the metrics target is shown as healthy within 45 seconds, and the target reports a 15-second collection interval.
- **SC-003**: After successful HTTP responses and at least one HTTP 4xx response, a baseline scrape that contains both of those counter series, at least 10 additional completed API requests that increase those same series and include successful requests and HTTP 4xx responses and no server failure, and another successful scrape, a documented rate window that contains both the baseline sample and the post-traffic sample shows a non-zero throughput, a non-zero client-error rate, a server-error result of the number 0 rather than an empty result, a median latency, and a 95th-percentile latency. A developer can observe this within 5 minutes of the target becoming healthy.
- **SC-004**: After the Prometheus container is stopped and started, or recreated without deleting its stored data, a query whose time range includes the minute before that change still returns samples stored in that minute. Todo rows are not part of this outcome.
- **SC-005**: The configuration check passes for the delivered configuration and fails for a configuration Prometheus would reject. A second developer who follows the written verification procedure finishes it in under 15 minutes and records the same pass or fail for target health, the 15-second interval, throughput, both error rates, latency, persistence, and the configuration check.
- **SC-006**: The running local environment provides the Todo API and Prometheus only. It includes no dashboard product and no alerting component.

## Assumptions

- The audience is a developer working on the Todo API locally. People using todo actions do not start or query this environment.
- Docker Compose is already installed. This feature does not install or configure the container runtime.
- The API already publishes a metrics endpoint that a collector can scrape without a person's access credential. This feature uses that endpoint as it exists. It does not change which measurements are published, and collections of that endpoint stay excluded from API traffic. The preserved series and labels are `http_requests_total` (`method`, `handler`, `status`), `http_request_duration_seconds` (`method`, `handler`, `status`), and `http_requests_in_progress` (`method` only). `status` remains the numeric status code as text.
- Request throughput means completed API requests per second. HTTP error rate means the per-second rate of client errors and the per-second rate of server errors, reported separately. Median latency and 95th-percentile latency are estimates from the histogram the API already publishes. The application does not calculate those latency values.
- An absent series and the number 0 are different PromQL results. A selector that matches nothing produces an empty result. The documented server-error query is written so that this empty case becomes the number 0. Throughput, client-error, and latency queries are not given that substitution: when their series are absent, the result stays empty.
- The documented local rate window is long enough to contain the baseline scrape and the next scrape after the verification traffic. At a 15-second interval, a one-minute window does this, so verification waits for one post-traffic scrape and does not require a five-minute wait. Longer windows remain valid for a developer who wants them. The query checks stay inside the 5-minute limit, and the full procedure stays inside the 15-minute limit.
- A non-zero request rate is the increase between a baseline sample and a later sample of the same counter series. Before the baseline scrape, the procedure sends successful HTTP responses and at least one HTTP 4xx response, then waits for a scrape that contains both of those series. One successful request is not a sufficient baseline. The additional traffic increases those same series. Two scrapes taken only after that additional traffic, with no further requests between them, can both carry the same counter value and produce a rate of 0. The procedure does not treat that pair as a successful throughput or client-error check.
- Verification traffic uses the API's normal local actions. The requests that create the baseline series happen before the baseline scrape and are not part of the 10. After that scrape, the procedure sends at least 10 additional completed requests, including successful requests and HTTP 4xx responses, on those same series. Producing a server error on purpose is not part of this feature. The server-error query is still required and returns the number 0 when no 5xx observations exist.
- Persistence in this feature covers samples Prometheus has stored. Those samples survive stopping, starting, and recreating the Prometheus container. They do not survive an explicit deletion of that stored data. The Todo API's SQLite database is a different store. This feature does not require todo rows to survive an API container restart or recreation, and it does not add that persistence.
- Local retention uses the collector's ordinary default retention. A custom retention period is not required.
- The environment is for one developer machine. It is not a shared, hosted, or production deployment. No new secrets are required. Published ports bind to loopback by default, so the Prometheus query page is a local development tool.
- The default published addresses are the API at `http://127.0.0.1:8000` and Prometheus at `http://127.0.0.1:9090`. A conflict on either address fails startup rather than silently moving to another address or binding to every network interface.
- Grafana, dashboards, alert rules, a separate alerting component, and production deployment are out of scope. Logs, traces, and new business measurements such as "todos created" are also out of scope.
- The verification procedure is a local procedure. Adding it to the existing continuous-integration jobs is not required by this feature.
