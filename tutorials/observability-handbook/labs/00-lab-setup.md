# Lab 00 — Reproducible local baseline

## Objective
Verify the actual repository before adding anything. Prerequisites: Docker + Compose, curl, Git, a local clone of `samperay/todo`, and a shell. Commands below assume you are in the repository root and checked out `feature/prometheus-server-integration`.

```bash
git status --short
git branch --show-current
docker compose config --services
docker compose up -d --build
docker compose ps
curl -fsS http://127.0.0.1:8000/metrics | head -40
curl -fsS http://127.0.0.1:9090/-/ready
```

If a command fails, **do not assume the service name or port**: inspect `docker-compose.yml`/`compose.yaml`, `.env.example`, and the README. Verify Prometheus can resolve the API *from its container*:

```bash
docker compose exec prometheus wget -qO- http://todo-api:8000/metrics | head
```

Open Prometheus UI at `http://127.0.0.1:9090` and run:

```promql
up{job="todo-api"}
http_requests_total
sum by (method,status) (http_requests_total)
```

**Expected:** `up=1` if the target scrape succeeds. Request counters may have no series until the first matching request. `up=1` is not proof the business endpoints work.

## Capture a baseline

Record time, Git SHA, Compose services, metric names and labels, target status, and screenshots/PromQL outputs. Do not paste secrets into the workbook.

## Troubleshooting decision tree

- `docker compose ps` shows no service → inspect build logs: `docker compose logs --tail=100 todo-api prometheus`.
- Host `/metrics` fails → check API process, host binding and published ports.
- Host `/metrics` works but `up=0` → check Prometheus target URL and Docker network DNS.
- `up=1` but HTTP counters absent → send a request to an instrumented endpoint; inspect metric naming and `/metrics` exclusion.
- `rate(...[5m])` empty → wait for at least two samples and ensure matching series exist.

## Exit criteria
Show one successful scrape, one instrumented request series, and explain host-vs-container addressing.
