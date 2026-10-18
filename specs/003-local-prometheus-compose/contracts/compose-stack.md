# Contract: Compose stack

Source file to add at implementation: `compose.yaml` at the repository root. The API image source is `backend/Dockerfile`.

## Services

| Service | Image | Published port | In-container listen |
|---------|-------|----------------|---------------------|
| `todo-api` | Built from `backend/Dockerfile` | `127.0.0.1:8000:8000` | `0.0.0.0:8000` |
| `prometheus` | `prom/prometheus:v3.13.4` | `127.0.0.1:9090:9090` | Prometheus default `9090` |

`prom/prometheus:v3.13.4` is the pinned tag. It is published on Docker Hub for `linux/amd64` and `linux/arm64`.

No other service is defined. Grafana and Alertmanager are not present.

## todo-api

- Build context: `backend/`.
- Command: `uvicorn todo_api.main:app --host 0.0.0.0 --port 8000`.
- No database volume.
- No extra environment variable is required. The default SQLite URL stays in application settings.
- No secret is passed in.

## prometheus

- Config file mount: `./deploy/prometheus/prometheus.yml` read-only at `/etc/prometheus/prometheus.yml`.
- Data mount: named volume `prometheus-data` at `/prometheus`.
- Storage flag: `--storage.tsdb.path=/prometheus`.
- No `--storage.tsdb.retention.time` override.
- No rule-file mount and no alertmanager URL.
- The process is not run as root.

## Volume

```yaml
volumes:
  prometheus-data:
```

`docker compose down` leaves `prometheus-data` in place. `docker compose down -v` deletes it and is the explicit reset.

## Commands

| Action | Command |
|--------|---------|
| Start | `docker compose up -d --build` |
| Stop | `docker compose down` |
| Reset Prometheus data | `docker compose down -v` |
| Validate config | `docker compose run --rm --no-deps --entrypoint promtool prometheus check config /etc/prometheus/prometheus.yml` |

A host port that is already taken makes `docker compose up` fail. The file does not choose another port.
