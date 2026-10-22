# Todo Frontend Operations & Architecture Handbook

**Repository:** `samperay/todo` · **Branch reviewed:** `feature/frontend-react-typescript` · **Baseline:** frontend Milestones 1–2 · **Audience:** SRE/DevOps Architect · **Edition:** 1.0 (2026-10-22)

> **Purpose:** A stable, reusable course. During future sessions, say **“Teach Handbook Lesson N, Section X”**. We will use this file as our syllabus, read the relevant code, execute the lab, discuss observations, and record progress. **Do not implement Milestone 3 until the chosen learning checkpoint is complete.**

## How to use this handbook

1. Read the **Concept** and **Code map** for one lesson. Do not memorize TypeScript syntax first.
2. Predict what you expect the lab to show; run the commands and record the actual result.
3. Compare the two. Investigate differences in DevTools, terminal output, and code.
4. Complete the **Checkpoint** only after the walkthrough. Questions are optional until the concepts are clear.
5. Mark the lesson complete in the tracker. Work on one lesson per session if needed.

**Safety:** Use disposable accounts and a temporary SQLite database for write tests. Never paste real bearer tokens, secrets, or browser storage contents into chat, issues, or screenshots. `localStorage` tokens are a local-learning design choice, not a recommended production security pattern.

## Course map and progress tracker

| # | Lesson | Key practical result | Status |
|---|---|---|---|
| 01 | Architecture & boot sequence | Identify processes, files, boundaries | In progress |
| 02 | React components & state | Trace `main` → `App` → child components | Not started |
| 03 | HTTP request lifecycle | Trace GET from UI through database and back | Not started |
| 04 | Authentication & session storage | Explain token flow and account isolation | Not started |
| 05 | Asynchrony, effects & race conditions | Reproduce canceled and stale requests | Not started |
| 06 | Vite proxy, origins & CORS | Diagnose routing and upstream errors | Not started |
| 07 | API contract, JSON & error handling | Explain 200/401/502, malformed responses | Not started |
| 08 | Browser troubleshooting & debugging | Use Network, Console, Storage, timings | Not started |
| 09 | Testing & quality gates | Run and interpret unit, type, lint, build checks | Not started |
| 10 | Docker, Nginx & deployment architecture | Understand planned production serving and proxying | Not yet implemented |
| 11 | CI/CD, dependency security & release | Map tests to release confidence | Partly planned |
| 12 | SRE reliability & incident drills | Build failure matrix, SLI/SLO and runbooks | Partly planned |

**Study rhythm:** Lessons 01–09 apply to Milestones 1–2. Lessons 10–12 include planned future architecture; clearly distinguish design from deployed code. After Lesson 09, decide whether to proceed with Milestone 3, then return to the handbook as new features arrive.

---

# Reference A — What actually exists

### Current application capabilities
- FastAPI backend with SQLite and bearer-token identity.
- React + TypeScript + Vite frontend with account creation, token paste, local logout, session restoration, and read-only Todo listing.
- `GET /api/v1/todos` uses the token and returns an array in backend order.
- UI states: idle, loading, ready (including empty), error.
- Frontend tests: user reported **16 passing tests across 5 files** after Milestone 2, plus successful typecheck, lint, and build. This is a reported checkpoint, not a fresh CI verification.
- Not yet present: frontend create/edit/complete/delete/filter; Nginx frontend deployment; later granular transport-error messages.

### Request architecture (development)

```text
Mac process: Vite dev server :5173 ──serves HTML/JS/CSS──> Browser
                                                      │
Browser runs React: main.tsx → App.tsx → useTodoSession │
                                                      │ fetch('/api/v1/todos')
                                                      ▼
                                              Vite proxy :5173
                                                      │ HTTP forwarding
                                                      ▼
                                               FastAPI :8000
                                                      │
                                                service/repository
                                                      │
                                                    SQLite
                                                      │
                                             JSON response → React
```

**Key distinction:** React executes in the browser. Vite is a local development server. FastAPI is the API server. SQLite is the database. Nginx is a *planned* frontend server for a later milestone, not part of this development path.

### Verified frontend code map (branch reviewed)

| File | Purpose | Read during |
|---|---|---|
| `frontend/src/main.tsx` | Finds `#root`; calls `createRoot(...).render(<StrictMode><App/></StrictMode>)` | 01–02 |
| `frontend/src/App.tsx` | Calls `useTodoSession()`; passes state/actions to `AccountPanel` and `TodoList` | 02 |
| `frontend/src/session/useTodoSession.ts` | Owns session, Todo array, loading/error status, request generation, cancellation | 02, 04–05 |
| `frontend/src/auth/tokenStore.ts` | Browser token persistence | 04 |
| `frontend/src/api/todos.ts` | `listTodos(...)`, validates Todo response shape | 03, 07 |
| `frontend/src/api/users.ts` | Account creation request | 04 |
| `frontend/src/api/client.ts` | `fetch`, bearer header, 10-second timeout, JSON parsing, stale-result checks | 03, 05, 07 |
| `frontend/src/components/TodoList.tsx` | Loading/empty/error/list rendering | 02, 07 |
| `frontend/src/components/TodoItem.tsx` | Renders individual Todo fields as React text | 02 |
| `frontend/vite.config.ts` | Proxies `/api` to `API_PROXY_TARGET` or `127.0.0.1:8000` | 06 |

**Useful navigation:** `git grep -n 'loadTodos\|listTodos\|fetch(' -- frontend/src`; `git grep -n 'api/v1/todos' -- backend`.

---

# Lesson 01 — Architecture & boot sequence

**Outcome:** Describe what runs where, how the page starts, and which process can fail independently.

## Concept
A web application is not one process. The browser runs JavaScript; Vite serves the development assets and forwards API requests; FastAPI implements business operations; SQLite persists records. **Serving the page** and **serving data** are separate availability conditions.

## Code walkthrough
1. Open `frontend/index.html` and locate the element with `id="root"`.
2. Open `frontend/src/main.tsx`: `document.getElementById('root')` finds the mount point. `createRoot(root).render(...)` starts rendering `App`.
3. Open `frontend/src/App.tsx`: `useTodoSession()` supplies data; `AccountPanel` and `TodoList` render it.
4. Open `frontend/vite.config.ts`: find `server.port: 5173` and the `/api` proxy target.

## Lab — start and observe
Terminal A (from `backend/`, using your Python environment):

```bash
uvicorn todo_api.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal B (from `frontend/`):

```bash
npm run dev
```

Terminal C:

```bash
lsof -nP -iTCP:5173 -sTCP:LISTEN
lsof -nP -iTCP:8000 -sTCP:LISTEN
curl -i http://127.0.0.1:8000/docs
```

Open `http://127.0.0.1:5173`. In DevTools → Network, reload and distinguish **document**, **JS/CSS assets**, and **Fetch/XHR**. A stored token is required for automatic Todo GET. Record which port served each request.

## Failure lab — backend down
Stop FastAPI only. Refresh browser. With a saved token, inspect `GET /api/v1/todos` and the UI. In the observed project, Vite returned **502 Bad Gateway** while `lsof :8000` showed no listener and `curl :8000` failed. The UI displayed **“The list could not be loaded.”** Restart FastAPI and refresh to verify 200. Do not confuse page availability with end-to-end health.

**Checkpoint:** Explain browser vs Vite vs FastAPI vs SQLite using one sentence each. Identify the failed component from a 502 plus connection refused. **Completion evidence:** screenshot of Network status (redact credentials) and terminal listener check.

---

# Lesson 02 — React components, props & state

**Outcome:** Explain how data gets from session logic to visible rows, without needing to write React code.

## Concept
A **component** is a function that describes UI. **Props** are inputs passed from a parent component. **State** is data React remembers across renders; updating it causes the UI to render again. A **hook** is a function using React features such as `useState` and `useEffect`.

## Code walkthrough

```tsx
// From App.tsx, simplified to the key relationship
const session = useTodoSession();
<TodoList todos={session.todos} listStatus={session.listStatus} notice={session.notice} />
```

`useTodoSession()` returns values such as `todos`, `listStatus`, and `notice`. `App` passes them to `TodoList`. `TodoList` chooses among loading, error, empty, and list. For a successful nonempty list, it maps each Todo to `TodoItem`. React safely renders `{todo.title}` as text, not executable HTML.

## Lab
Open `App.tsx`, `TodoList.tsx`, `TodoItem.tsx` side by side. Search for `todos.map`, `listStatus`, and `todo.title`. Draw arrows showing who **owns** `todos` and who merely **receives** it. Create no code. Use the browser to compare the empty state with a populated account.

**Checkpoint:** What is the difference between state and props? Which file decides whether to show “Loading todos.”? Which file actually renders a title?

---

# Lesson 03 — HTTP request lifecycle

**Outcome:** Trace one GET across every application boundary.

## Concept
The browser sends an HTTP request; the proxy forwards it; FastAPI authenticates, reads data, and responds; React parses and displays the result. A function call in React is **not** itself an HTTP request; the actual network boundary occurs at `fetch()`.

## Code walkthrough

```text
useTodoSession.loadTodos(token, generation)
   → api/todos.ts: listTodos(...)
   → api/client.ts: request(...)
   → fetch('/api/v1/todos', { method: 'GET', headers, signal })
   → Vite proxy /api → FastAPI :8000
   → backend route → service/repository → SQLite
   → HTTP 200 JSON array
   → client parses → todos.ts validates → hook setTodos(...)
   → App → TodoList → TodoItem
```

`listTodos` does **not** create another network stack: it calls the shared `request` function. The browser sees URL `:5173/api/v1/todos`, even though FastAPI listens on `:8000`.

## Lab
DevTools → Network → Fetch/XHR → click `GET /api/v1/todos`. Record method, URL, status, request headers, response body shape, timing. Confirm `Authorization` header **exists**, but do not copy its value. Compare response item order to UI order. Use `git grep` to locate the backend route and repository method.

**Checkpoint:** Which line actually initiates network I/O? Which process sends SQL? What changes when response is `[]` versus an error?

---

# Lesson 04 — Authentication & session storage

**Outcome:** Explain account creation, bearer token use, browser persistence, and logout limitations.

## Concept
`POST /api/v1/users` creates an anonymous account and returns an ID and token. The token is a credential. Subsequent GET requests use `Authorization: Bearer <token>`. The frontend stores token and account ID in `localStorage` for reload persistence. **This application does not use cookies for authentication.** A local logout clears browser storage; it does not revoke the backend token.

## Code walkthrough
Read `auth/tokenStore.ts`, `api/users.ts`, `useTodoSession.ts` functions `initialSession`, `createNewAccount`, `logout`, `pasteToken`. Follow `client.ts` setting the Authorization header. Pasting a token may not recover the account ID because the backend has no identity lookup endpoint.

## Lab
Use a disposable account. Observe Local Storage key **names** (not values); refresh and see that no new account is created; log out and verify the saved keys are cleared and Todo rows disappear. Compare network calls before and after logout. **Do not post token values.**

**Checkpoint:** What persists after reload? What does local logout *not* do? Why must the backend check token ownership on every Todo request?

---

# Lesson 05 — Asynchrony, StrictMode & race conditions

**Outcome:** Understand canceled requests and stale-response checks by reading the actual implementation.

## Concept
An `async` operation can finish later. If Account A's request finishes after switching to B, A's result is **stale**. Two separate defenses are useful: `AbortController` requests cancellation; a **generation counter** rejects results that no longer belong to the current session. Cancellation is not proof the server never processed the request.

## Code walkthrough
In `useTodoSession.ts` locate `generationRef`, `controllersRef`, `abortInFlight`, `bumpGeneration`, `isCurrent`, `loadTodos`. In `client.ts` locate `signal`, `fetch`, and `isCurrent` checks. Draw:

```text
A starts: generation 1 ───────────────┐
                                      │ late response → discard
Switch to B: bump generation to 2 ────┤
   ├─ abort previous requests         │
   ├─ clear previous Todos            │
   └─ B starts: generation 2 → accept ┘
```

Development StrictMode runs an extra effect setup/cleanup cycle. The observed Network trace of `(canceled)` followed by `200` is consistent with `useEffect` cleanup in `useTodoSession.ts`; it does not imply Vite independently duplicates requests.

## Lab
With an existing token, open DevTools → Network and refresh while Vite dev server runs. Inspect two requests, one canceled and one successful. Find the cleanup `return () => abortInFlight()` in the source. Do **not** disable StrictMode. For a deterministic race simulation, use existing unit tests or a test mock that resolves A after B; avoid modifying production code merely to create failures.

**Checkpoint:** Explain cancellation versus rejecting a stale response. Why is a canceled GET less risky than a duplicated account-creation POST?

---

# Lesson 06 — Proxy, origins & CORS

**Outcome:** Identify the hop returning an error and distinguish a proxy failure from browser CORS enforcement.

## Concept
An **origin** is scheme + hostname + port. `http://127.0.0.1:5173` differs from `http://127.0.0.1:8000`. With Vite proxy, the browser calls relative `/api/...` on its own origin, and Vite forwards server-side. This avoids requiring cross-origin browser API calls during development. CORS is a browser access-control mechanism, not a substitute for authentication.

## Code walkthrough
Read `frontend/src/config.ts`, `frontend/vite.config.ts`, `frontend/src/api/client.ts`. Confirm default proxy target and optional `API_PROXY_TARGET` override.

## Lab
While backend runs, inspect Request URL and Remote Address in Network. Stop backend and repeat; expect a gateway failure from `:5173`, not a direct browser request to `:8000`. Verify backend listener with `lsof`; do not diagnose every 502 as CORS. Restore backend and confirm 200.

**Checkpoint:** Why is the browser request URL on port 5173? Which process knows the upstream port? Why is 502 not a CORS error by itself?

---

# Lesson 07 — API contracts, JSON & error handling

**Outcome:** Distinguish HTTP failure, network failure, invalid JSON, invalid data shape, and empty success.

## Concept
`200` plus `[]` means successful empty data; `401` means authentication failure; `502` means proxy/upstream failure. A response may contain plain text rather than JSON. Valid HTTP status does not guarantee valid JSON or a valid Todo object.

## Code walkthrough
`api/todos.ts` validates an array of Todo-shaped objects. `api/client.ts` currently reads text and attempts `JSON.parse(text)` for non-204 responses. **Known limitation:** if Vite returns `502 text/plain`, parsing throws; the catch returns `status: 0`, losing the original 502. The generic UI error still appears. Track this as US8 improvement; do not silently change scope now.

## Lab
Observe three cases: 200 with rows; 200 with `[]`; 502 with backend stopped. For each, note response content-type, status, and UI. Optional: use a disposable mock test to simulate malformed JSON. Do not expose auth tokens.

**Checkpoint:** Why must empty success not be displayed on HTTP failure? Why should a client preserve the original 502 even if parsing fails?

---

# Lesson 08 — Browser diagnostics

**Outcome:** Investigate user-visible incidents using evidence rather than guesses.

## Tool map
- **Network:** method, URL, status, request/response headers, timings, initiator, cancellation.
- **Console:** JavaScript exceptions and browser warnings (a 502 line alone does not prove unhandled JS error).
- **Application → Local Storage:** storage key names and persistence; keep token values private.
- **Terminal:** `lsof`, `curl`, Vite output, FastAPI logs.
- **Sources:** breakpoints at `fetch`, `loadTodos`, and state transitions.

## Incident exercise
User reports “Page loads but list is unavailable.” Start with a **timeline**: page served? GET emitted? response status? proxy listener? backend listener? backend logs? UI state? Compare evidence to Lesson 01. Create a 5-line incident note: symptom, impact, observations, root cause, recovery validation.

**Checkpoint:** For a 502 with no port-8000 listener, what is the fastest confirming command? For a 200 with empty array, is the API necessarily broken?

---

# Lesson 09 — Testing & quality gates

**Outcome:** Know what each quality check protects and what it does not.

From `frontend/`:

```bash
npm run typecheck
npm run lint
npm test
npm run build
```

| Check | Protects against | Does not prove |
|---|---|---|
| Typecheck | Type-level mistakes | Correct runtime behavior |
| Lint | Suspicious patterns/style violations | Correct business behavior |
| Vitest | Behaviors encoded in tests | Real proxy/backend health unless integration is tested |
| Build | Frontend compiles/bundles | End-to-end availability |

Read `frontend/tests/components/TodoList.test.tsx` and `AccountPanel.test.tsx`. Identify test setup, action, assertion, and mocks. Explain why a mock success test cannot guarantee the real FastAPI process is running. **Baseline reported:** 16 passing tests after Milestone 2.

**Checkpoint:** Why can all unit tests pass while production users still see 502?

---

# Lesson 10 — Docker, Nginx & deployment (future milestone)

**Status:** Planned; do not treat as already implemented.

**Target architecture:** build React assets → Nginx serves static files → Nginx proxies `/api` to backend container → FastAPI → SQLite. Vite dev server is not the production serving layer. Learn container DNS, host vs container ports, upstream health, config templating, and 502/504 failure analysis.

**When implemented:** read `frontend/Dockerfile`, `frontend/nginx.conf.template`, `frontend/docker-entrypoint.sh`, and Compose config. Run `docker compose config`, inspect logs, verify Nginx config (`nginx -t` inside container), and trace an API request across container names. Do not assume the files or commands work until the feature exists.

**Checkpoint:** Why can't Nginx inside a container assume `localhost:8000` means the backend container?

---

# Lesson 11 — CI/CD, dependencies & release (future milestone)

**Status:** Partially planned. Once frontend CI exists, inspect GitHub Actions jobs for typecheck, lint, unit tests, browser E2E, and dependency audit. Compare local and CI Node versions; learn lockfiles, reproducible installs, test isolation, security severity gates, and artifact provenance.

**Exercise:** Take one failed check, identify whether it is a code issue, dependency issue, environment issue, or flaky test. Write a short remediation plan without weakening quality gates.

**Checkpoint:** Why are passing unit tests insufficient for a deployment decision?

---

# Lesson 12 — Reliability engineering & incident drills

**Status:** Concepts apply now; advanced infrastructure labs later.

## Failure matrix

| Failure | Browser page | API GET | User impact | Diagnostic |
|---|---|---|---|---|
| FastAPI stopped | Loads from Vite | 502 in observed setup | Todos unavailable | `lsof :8000`, proxy logs |
| Vite stopped | Cannot load dev page | Cannot reach same-origin API | Frontend unavailable | `lsof :5173` |
| Missing token | Loads | No authenticated list request | Account identification required | Storage key names, UI |
| Invalid token | Loads | 401 | Unauthorized | Network status, backend auth logs |
| Empty account | Loads | 200 `[]` | Valid empty list | Response body, empty state |
| Slow backend | Loads | Pending or timeout | Delay/error | Network timing, 10s client timeout |
| Malformed JSON | Loads | May return 200 with bad body | Parse failure | Content-type/body, client catch |

## Reliability vocabulary
- **SLI:** measured behavior (e.g., fraction of successful Todo list loads).
- **SLO:** target for the SLI over a window.
- **Availability:** ability to perform a meaningful user operation, not merely serve HTML.
- **Latency:** time from request initiation to usable result.
- **Timeout:** bound on waiting; not a guarantee server-side work stops.
- **Retry:** new attempt; must consider idempotency, backoff, and overload.

## Incident report template

```text
Incident ID / time:
User-visible symptom:
Scope / impact:
Evidence (status, timestamps, logs):
Affected boundary (browser / Vite / FastAPI / SQLite):
Root cause (confirmed vs suspected):
Recovery action:
Verification:
Follow-up prevention:
```

**Capstone:** Reproduce backend-down 502, collect evidence, recover, write incident report, and propose one measurable SLI for the user-facing Todo list.

---

# Reference B — Fast lookup glossary

| Term | Plain meaning |
|---|---|
| Component | React function describing a part of the UI |
| Prop | Input passed into a component |
| State | Data React remembers and uses to render |
| Hook | React function for state, effects, or reusable behavior |
| Effect | React synchronization logic, often used for fetching or subscriptions |
| Promise | Representation of an asynchronous result |
| Fetch | Browser API that starts HTTP requests |
| AbortController | Requests cancellation of an asynchronous operation |
| Race condition | Outcome depends on timing/order of overlapping operations |
| Generation counter | Version number used to reject results from an obsolete session |
| Proxy | Intermediary forwarding a request to another service |
| Upstream | Service a proxy calls on behalf of a client |
| Origin | Scheme + host + port |
| CORS | Browser-enforced cross-origin response access rules |
| Bearer token | Credential presented in an Authorization header |
| 401 | Unauthorized / credentials missing or rejected |
| 502 | Gateway/proxy unable to obtain a valid upstream response |
| Idempotency | Repeating an operation has the same intended effect as doing it once |
| SLI/SLO | Reliability measurement / reliability objective |

# Reference C — How to continue with ChatGPT

Use any of these prompts in future sessions:

- **“Use `frontend-operations-handbook.md`. Teach Lesson 01, section Code walkthrough. Explain each line from the GitHub branch and wait after each file.”**
- **“Continue Lesson 03, lab. I see HTTP 502; guide me through diagnosis one command at a time.”**
- **“Review my answers for Lesson 05 only after showing me the actual implementation of `bumpGeneration` and `loadTodos`.”**
- **“Update the handbook after Milestone 3, keeping completed lessons unchanged and marking newly implemented capabilities.”**

**Source-of-truth rule:** This handbook documents the Milestone 2 branch reviewed on 2026-10-22. If code changes, read the current GitHub branch before explaining exact behavior. The handbook is a learning guide, not a substitute for inspecting source code and observing the running system.
