# Research: React and TypeScript Todo Frontend

Decisions for [spec.md](./spec.md). The backend contract is the existing one in [../001-todo-management/contracts/todos.openapi.yaml](../001-todo-management/contracts/todos.openapi.yaml), checked against `backend/src/todo_api/api/routes/`, `backend/src/todo_api/schemas/`, and `backend/src/todo_api/api/deps.py`. This feature does not add a route, a field, or a CORS grant.

## Framework and language

**Decision**: React with TypeScript, built by Vite, styled with one plain CSS file. No Next.js, no Redux or other state library, no component library, and no router.

**Rationale**: The spec names this stack. The screen is one page: account, list, filter, create, edit, complete, reopen, and delete. A router and a state library would add concepts the SRE learning goal does not need. TypeScript strict mode holds the API shapes at the client boundary. JSX text nodes render titles and descriptions as text, which is the safe-rendering rule.

**Alternatives considered**:

- Next.js. Rejected. It is a second application server and is out of scope.
- Vue, Svelte, or plain HTML without a component model. Rejected because the spec requires React.
- Redux, Zustand, or a component library. Rejected by the spec.

## HTTP client

**Decision**: The native Fetch API in one client module. The browser calls only relative `/api/v1/...` paths. Each request aborts after 10 seconds. That timer abort, HTTP 502, HTTP 504, any other HTTP 5xx, and a browser network failure are five different results. Each shows one fixed sentence. None of them shows the response body, a stack trace, SQL, or the bearer token. A timer abort is not the abort used when the account session changes.

**Rationale**: Fetch is required and adds no dependency. Relative paths keep the page and the API on one browser origin, so the existing API needs no CORS change. The 10-second limit stops a loading state that never ends. Nginx can return 502 or 504 when the API is down or slow, without a new backend route. A connection failure never receives a status. Tests need those cases separated so an operator can tell a client timeout from a proxy timeout. The sentences are fixed so a gateway HTML page or a token in a header cannot reach the screen.

**Alternatives considered**:

- Axios or a generated client. Rejected. Extra dependency, and the contract is seven calls.
- Calling `http://127.0.0.1:8000` from the page. Rejected. That is a cross-origin call, and the API does not send a cross-origin grant.
- One message for every transport failure. Rejected. It hides the difference between a client abort, a proxy error, and a connection failure.
- Showing the status text or the response body. Rejected. Those can contain internal details.

## Same-origin forwarding

**Decision**: Local Vite proxies `/api` to `API_PROXY_TARGET`, default `http://127.0.0.1:8000`. The container Nginx proxies `/api/v1/` to `API_UPSTREAM`, default `http://todo-api:8000`. The committed source file is `frontend/nginx.conf.template`. `frontend/docker-entrypoint.sh` substitutes `API_UPSTREAM` and runs `nginx -t` before Nginx starts. There is no committed `frontend/nginx.conf`. Neither upstream value is a `VITE_` variable, so Vite does not inline it into the browser bundle. The browser bundle contains the relative path only.

**Rationale**: `main.py` registers no CORS middleware. Adding one would change the backend. Compose DNS name `todo-api` is how Prometheus already reaches the API. `localhost` inside Nginx would be the frontend container, not the API. Keeping the upstream in the server process makes a wrong address an operator setting, which the handbook can break and restore on purpose.

**Alternatives considered**:

- FastAPI `CORSMiddleware` for `http://127.0.0.1:5173`. Rejected. It modifies backend authentication-adjacent browser policy and is forbidden by the spec.
- A public API gateway. Rejected by scope.

## Token storage

**Decision**: `localStorage` keys `todo.accountId` and `todo.token`. Logout removes those keys and does not call a revoke route, because none exists. Create-account shows the token once in component state and does not write it to the URL, logs, or `console`. Pasting a saved token writes the same keys. The design is documented as a local-learning limitation, not production authentication.

**Rationale**: The service returns the token only from `POST /api/v1/users` and stores only its hash. Memory-only storage loses the only credential on reload. An httpOnly cookie would require backend changes. `localStorage` survives reload in the same browser. Any script on this origin can read it. The application ships no third-party scripts, which reduces that exposure and does not remove it.

**Alternatives considered**:

- `sessionStorage`. Rejected. Closing the browser would strand the account the same way memory-only storage does.
- httpOnly cookie or a new sign-in system. Rejected. Both change backend authentication.

## Account switch and 401

**Decision**: The page keeps a session generation, a number that starts at 0. Logout, a newly created account, and a pasted token increment that number, abort every request started under the old number, and clear the stored todos, the open editor, and the failure notice in that same update. A `401` does the same clear. Each request remembers the generation that started it. A response is applied only when that generation is still current. A late response from an older generation is discarded even when it arrives after the new account's request has already completed. A `404`, `422`, 502, 504, other `5xx`, client timeout, or network failure for the current generation leaves a list that was already shown.

**Rationale**: Clearing the list at switch time is not enough. The previous list request can resolve later and write the previous account's rows back. Aborting the old fetch reduces that window. The generation check closes it, including when the abort does not stop the response. The spec still keeps the last good list for a failed action on the current account. Vitest holds the old response until the new one has been applied, then releases the old one, and asserts the old rows never return.

**Alternatives considered**:

- Keeping the previous list until the new list arrives. Rejected because a slow or failed switch would show the wrong person's todos.
- Clearing the list on every error. Rejected because the spec keeps the last good list for validation, not-found, server, and network failures.
- Aborting without a generation check. Rejected. A response can already be parsed when logout runs, and the abort would not discard it.
- Ignoring a late response only when it arrives before the new request finishes. Rejected. The required case is the late response that arrives after the new account's request has completed.

## Same-page edit lock

**Decision**: The page tracks the todo id whose editor is open and the todo id whose save is in flight. A second edit of that same id does not open and does not send. An edit of a different id may open. Complete, reopen, and delete are not editors. Each of those still refuses a duplicate submit while its own request is in flight. Another tab or client is outside this rule. No `If-Match`, version field, or backend change.

**Rationale**: The spec simplified overlapping edits to a single page. The service still applies the later successful patch when two clients race. The frontend does not pretend to detect that race.

**Alternatives considered**:

- Optimistic concurrency on `updated_at`. Rejected. It needs a backend precondition the API does not have.
- A cross-tab lock. Rejected. The spec treats another tab as another client.

## Validation messages

**Decision**: The client reads FastAPI's `422` body `detail[].msg` and shows one plain sentence when the text contains one of: "Title is required", "Title must be at most 200 characters", "Description must be at most 2000 characters", "Priority is invalid", or "At least one of title, description, or priority is required". Any other `422` still says the values were rejected and does not show the raw `detail` array.

**Rationale**: Those sentences are the `ValueError` texts in `backend/src/todo_api/schemas/todo.py`. Pydantic may prefix them. Matching the sentence avoids depending on the prefix. The domain `401` and `404` bodies are `{error:{code,message}}` from `backend/src/todo_api/api/errors.py`, not the `422` shape.

**Alternatives considered**:

- Displaying `detail` as JSON. Rejected. It leaks the framework shape and can include input the spec wants shown only as a plain rule.
- Re-implementing every limit only in the browser and ignoring `422`. Rejected. The service remains the authority. The screen still states the rule the service rejected.

## Playwright isolation

**Decision**: Playwright starts its own API and Vite processes through `frontend/scripts/playwright-servers.sh`. That shell script delegates process creation and process-group termination to Python 3. `reuseExistingServer` is false everywhere, so a process already listening is never reused. Python creates a new temporary directory and a new SQLite file inside it, then sets `DATABASE_URL` to that absolute path. It starts Uvicorn on `127.0.0.1:8001` and Vite on `127.0.0.1:5174` with `strictPort` and `API_PROXY_TARGET=http://127.0.0.1:8001`, each with `subprocess.Popen(..., start_new_session=True)`, so npm, Node, and Uvicorn children stay in that session. The `setsid` executable is not used. The runner records only those session ids. If either port is already taken, the runner prints which port and exits non-zero. It does not kill the process that already holds the port, and it does not pick another port. On success, failure, or signal, one guarded cleanup calls `os.killpg` with SIGTERM, then SIGKILL if needed, only for the recorded sessions, and deletes the temporary directory. EXIT after INT or TERM does not run that body twice. The same Python calls are used on macOS and on Linux. Chromium is the only browser. Ports `8000` and `5173`, and any `todo.db` the contributor already has, are not used.

**Rationale**: `Settings.database_url` defaults to `sqlite+aiosqlite:///./todo.db` in the process working directory. An explicit new file is the only way to avoid that default. A listener on `8001` might be an old crashed run or something the contributor started. Attaching to it would reuse unknown data. Killing whatever holds the port could stop a process this run did not start. Backend tests already use a temp SQLite file in `backend/tests/conftest.py`. Playwright follows that idea with a real Uvicorn process instead of the in-process HTTPX client. One browser is enough for the workflow and keeps CI smaller.

**Alternatives considered**:

- Reusing `127.0.0.1:8000` and the default `todo.db`. Rejected. It can read or write the contributor's data.
- `reuseExistingServer: true` on a developer machine. Rejected. It attaches to a backend the runner did not start.
- `pkill` for Uvicorn or Vite during cleanup. Rejected. It can stop the contributor's API on port `8000`.
- The `setsid` command and GNU `kill -- -$pgid`. Rejected. The command is not on a default macOS install, and `--` is not portable to BSD `kill`. The POSIX `setsid` system call and `os.killpg` work on macOS and on the Linux CI runner.
- Killing only the direct child PID. Rejected. `npm` and Uvicorn spawn further children that would survive.
- Choosing a free port when `8001` or `5174` is busy. Rejected. The failure must name the occupied port.
- Playwright against the Docker stack. Rejected for the default check. Compose SQLite lives in the API container and is not a disposable file the test can delete without `docker compose down`.
- Firefox and WebKit as well as Chromium. Rejected for this feature. The spec requires Playwright, not a three-browser matrix.

## Vulnerability check

**Decision**: `npm audit --audit-level=high` in the frontend directory, locally and in CI. High and critical findings fail the command. The command still prints moderate and low findings. No second scanner.

**Rationale**: The spec leaves the tool to planning and sets the fail line at high. npm is already the package manager, so audit adds no dependency. The advisory database changes over time, so a lockfile can fail later without a code change. That is the check working.

**Alternatives considered**:

- `npm audit` with the default level, which also fails on moderate. Rejected because the spec says moderate and low do not fail the default check.
- OSV-Scanner or Snyk. Rejected. Extra tool for the same gate.

## Container images

**Decision**: Multi-stage image. Build stage `node:22-alpine`. Runtime stage `nginx:1.28-alpine`, listening on container port 80, published as `127.0.0.1:8080:80`. Implementation confirms both tags still exist for the host architecture before the first commit and does not use `latest`. The existing API image and `prom/prometheus:v3.13.4` stay as they are.

**Rationale**: Node 22 is the LTS line that covers this plan's date. Nginx serves the built files and proxies `/api/v1/`. Alpine keeps the runtime small. Pinning avoids a moving `latest` tag. The API container continues to listen on `0.0.0.0:8000` inside the Compose network so Nginx and Prometheus can reach it, while the host publish stays loopback.

**Alternatives considered**:

- `nginx:latest` or an unpinned Node image. Rejected. Not reproducible.
- Caddy or a Node static server in production mode. Rejected. The spec requires Nginx.

## CI shape

**Decision**: Keep the four backend jobs in `.github/workflows/ci.yml` on the same pull-request and main-branch triggers, including `pytest --cov-fail-under=90`. Add four frontend jobs in that file: `frontend-static` (TypeScript and ESLint), `frontend-unit` (Vitest), `frontend-e2e` (Playwright plus a Python 3.12 API), and `frontend-audit` (`npm audit --audit-level=high`). Backend jobs do not install Node. Frontend jobs do not change the coverage gate.

**Rationale**: Separate jobs match the spec and keep a frontend failure from hiding a backend failure. The e2e job is the only one that needs both toolchains.

**Alternatives considered**:

- A second workflow file. Rejected. The spec asks for the same automation triggers, and one file keeps the backend jobs visibly intact.
- Folding Playwright into the backend pytest job. Rejected. It would mix runtimes and could weaken the coverage job's scope.

## Documentation timing

**Decision**: `frontend/README.md` and `frontend/ARCHITECTURE.md` ship with the implementation. They cover local development, build and test commands, Docker, the module map, and the token limitation. `tutorials/frontend-operations-handbook/` is written only after that code and the Compose file exist. This planning phase does not create the handbook. Chapter file names are chosen then. Each exercise uses a safe local or simulated failure and has symptoms, investigation, root cause, remediation, validation, and rollback.

**Rationale**: The spec requires the handbook examples to match the running application. Writing them now would invent commands and file paths.

**Alternatives considered**:

- Drafting the handbook during planning. Rejected by the spec.
- Putting the SRE exercises only in `frontend/README.md`. Rejected. The spec requires the dedicated handbook path.
