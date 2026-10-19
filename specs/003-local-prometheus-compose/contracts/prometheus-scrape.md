# Contract: Prometheus scrape

Source file to add at implementation: `deploy/prometheus/prometheus.yml`.

The collected document is the existing `GET /metrics` contract in [../../002-prometheus-api-metrics/contracts/metrics.openapi.yaml](../../002-prometheus-api-metrics/contracts/metrics.openapi.yaml). This file does not change that document.

## Required configuration

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: todo-api
    metrics_path: /metrics
    scrape_interval: 15s
    static_configs:
      - targets:
          - todo-api:8000
```

## Rules

- The target host is the Compose service name `todo-api`. It is not `localhost`, `127.0.0.1`, or a published host port.
- The path is `/metrics`. No bearer token and no extra header.
- The interval is 15 seconds on the global config and on this job.
- There is one job.
- `rule_files` and `alerting` are absent.
- `promtool check config` on this file exits successfully.
- The same `promtool` command exits unsuccessfully for a file Prometheus rejects, such as a file with a malformed duration or an unknown top-level key.

## Target health

Developers read health from Prometheus at `http://127.0.0.1:9090`. The `todo-api` target shows:

- **Up** after a successful scrape, with interval 15 seconds.
- **Down**, including the scrape error, when `todo-api:8000` does not answer.
- **Up** again on a later scrape after the API recovers, without recreating the Prometheus container.
