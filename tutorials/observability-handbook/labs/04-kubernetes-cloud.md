# Lab 04 — From local Docker to Kubernetes and cloud

## Stage 1: Local architecture review

Document the current services, scrape paths, volumes, configuration files, and secrets. Identify which settings must change across environments.

## Stage 2: Disposable Kubernetes cluster

Use kind or minikube. Build the Todo API image and deploy it with 2–3 replicas, a Service, readiness/liveness probes, and a metrics port. Install Prometheus using a supported approach and verify pod discovery. RBAC must permit Kubernetes API discovery. Compare `up` per pod and `sum by (instance)(...)`.

**Exercise:** Delete one pod. Explain how its replacement is discovered and why its new instance label may differ. Measure the scrape gap.

## Stage 3: Reliability and cardinality

Estimate series count as the product of relevant label values. Avoid user IDs, Todo IDs, URLs with raw path parameters, and trace IDs as Prometheus labels. Document retention, resource limits, backup, and alerting ownership.

## Stage 4: Cloud architecture design

Design, but do not deploy by default, a secure cloud setup with private networking, TLS, authentication, RBAC, remote storage, HA collection, Alertmanager redundancy, cost controls, and disaster recovery. Choose one provider only after clarifying budget and available access.

## Exit criteria

Explain discovery, per-instance health, data durability, scale bottlenecks, and security boundaries; provide a teardown plan for all billable resources.
