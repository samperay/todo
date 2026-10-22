# Contract: Local and Container Runtime

Existing services stay. The frontend is added. Host ports bind to `127.0.0.1` only.

## Addresses

| Mode | Browser | API the browser uses | Forward target | Prometheus |
|------|---------|----------------------|----------------|------------|
| Local dev | `http://127.0.0.1:5173` | Relative `/api/v1` on that origin | `API_PROXY_TARGET`, default `http://127.0.0.1:8000` | Unchanged, `http://127.0.0.1:9090` when Compose is up |
| Compose | `http://127.0.0.1:8080` | Relative `/api/v1` on that origin | `API_UPSTREAM`, default `http://todo-api:8000` | `http://127.0.0.1:9090` |
| Playwright | `http://127.0.0.1:5174` | Relative `/api/v1` on that origin | A new Uvicorn process on `http://127.0.0.1:8001` and a new SQLite file | Not used |

A busy `5173` or `8080` fails startup. Vite uses `strictPort`. Compose fails if `8080` is taken. Playwright uses `5174` and `8001` so it does not take the contributor's dev ports. If `5174` or `8001` is already taken, Playwright exits non-zero and names that port. It does not attach to the existing listener and does not kill it.

## Vite

- `server.host` is `127.0.0.1`.
- `server.port` is `5173`.
- `server.strictPort` is true.
- Proxy `/api` to `API_PROXY_TARGET`.
- `API_PROXY_TARGET` is read from the environment in the Vite config only. It is not a `VITE_` variable and is not referenced from React code.

The dev command does not start the API. The contributor starts Uvicorn or Compose separately. The API remains `uvicorn todo_api.main:app` from `backend/` on `127.0.0.1:8000`.

## Compose

Add service `frontend` to the existing root `compose.yaml`.

| Item | Value |
|------|--------|
| Build context | `frontend/` |
| Publish | `127.0.0.1:8080:80` |
| Upstream env | `API_UPSTREAM=http://todo-api:8000` |
| `todo-api` publish | `127.0.0.1:8000:8000`, unchanged |
| `prometheus` publish | `127.0.0.1:9090:9090`, unchanged |
| Prometheus file | `deploy/prometheus/prometheus.yml`, still scraping `todo-api:8000` `/metrics` |
| API database | Still the container-local SQLite file. No new volume. |
| Extra services | None |

Nginx:

- Serves the built files.
- `location /api/v1/` proxies to `API_UPSTREAM` and keeps the `/api/v1/` path.
- Does not proxy `/metrics`.
- Substitutes `API_UPSTREAM` at container start. A wrong value is an operator failure, not a committed secret.

The API process inside its container still listens on `0.0.0.0:8000` so the Compose network can reach it. That is the existing image command. This feature does not republish `8000` on every host interface.

## Playwright process rules

- `reuseExistingServer` is false. The runner does not use an API or Vite process it did not start.
- The SQLite file is created in a new temporary directory for that run. `DATABASE_URL` is its absolute path. It is not `backend/todo.db` and not the default `./todo.db`.
- `frontend/scripts/playwright-servers.sh` delegates process creation and termination to Python 3. Each of Uvicorn and Vite is started with `subprocess.Popen(..., start_new_session=True)`. The `setsid` executable is not used. The runner records those session ids. npm, Node, and Uvicorn children stay in the session. The same calls are used on macOS and on Linux.
- One cleanup function runs on exit, failure, and INT or TERM. A guard makes the body run once when a signal also triggers EXIT. Python signals only recorded sessions with `os.killpg`, then deletes the temporary directory.
- A process that already held `8001` or `5174` is not in that session list and is not signalled.

## Images

| Stage | Image |
|-------|--------|
| Build | `node:22-alpine` |
| Runtime | `nginx:1.28-alpine` |

Implementation verifies the tags exist for the machine architecture before they are committed. Do not use `latest`. The image build context is `frontend/` and does not install the Python package.
