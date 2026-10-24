# Feature Specification: React and TypeScript Todo Frontend

**Feature Branch**: `004-react-todo-frontend`

**Created**: 2026-10-22

**Status**: Draft

**Input**: User description: "Add an independent React and TypeScript frontend for the existing Todo application. The frontend lets a person create an account, keep the bearer token the API already issues, and create, view, edit, complete, reopen, delete, and filter that person's todos. It shows loading and API errors, builds and runs on its own, talks only to the existing FastAPI contract, and can be developed locally or deployed with Docker and Nginx. Do not replace the backend or add unrelated infrastructure."

## Clarifications

### Session 2026-10-22

- Q: Is persistent browser storage of the bearer token production-ready? → A: No. It is an accepted limitation for this local learning application. Backend authentication stays as it is.
- Q: What happens when two edits of one todo overlap? → A: One page allows only one edit of that todo at a time. Updates from another page or client are outside the frontend's concurrency guarantee. No version field and no optimistic concurrency control.
- Q: When is the operations handbook written? → A: After the frontend implementation, so its examples match the running application.
- Q: Are a client timeout, HTTP 502, HTTP 504, any other HTTP 5xx, and a browser network failure one unexpected-failure message? → A: No. Each produces its own safe message. Cancelling a request because the account session changed does not show the timeout message. No message includes a raw response body, credential, database text, or stack trace.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create an account and stay identified (Priority: P1)

A person opens the browser application and creates an account. The existing service does not ask for a name, email, or password. It returns an account identifier and a bearer token, and it shows that token only in this response. The person can see the token once, keep using the application after a reload, leave the account, and later resume by presenting the same saved token.

**Why this priority**: Every todo action requires the bearer token the service already issues. There is no separate sign-in.

**Independent Test**: Create an account and confirm the screen shows an identifier and a token with no name, email, or password collected. Reload and confirm the same account's todo list is still available. Leave the account and confirm this page no longer sends the token. Present that same token again and confirm the service still accepts it. Present an unknown token and confirm the screen says the person must be identified. Confirm the token is absent from the page address and from application logs.

**Acceptance Scenarios**:

1. **Given** a person has no account in this browser, **When** they create an account, **Then** the application accepts the action with no name, email, or password, and shows the new account identifier and the bearer token once.
2. **Given** the account was just created, **When** the person reloads the application, **Then** they remain identified and can open their own todo list without creating another account.
3. **Given** the person is identified, **When** they leave the account, **Then** this browser removes the stored token and later todo actions on this page tell them they must be identified. The service still accepts that same token. Leaving the account does not revoke the backend credential, delete the account, or delete that account's todos.
4. **Given** the person left the account, or opened a browser that does not have the token, **When** they present the token they saved, **Then** they see the todos that belong to that same account.
5. **Given** the person presents a token the service does not recognize, or presents no token, **When** they try to view or change todos, **Then** no todo is shown or changed and the screen says they must be identified.
6. **Given** any of these steps, **When** the page address, application logs, an error message, or recorded diagnostic output is inspected, **Then** the token is absent from the path, query, fragment, logs, error text, and diagnostic output. The only places the token is shown are the one-time display at account creation and the field where the person deliberately enters a saved token.
7. **Given** the published description of this application, **When** a contributor reads how identification works, **Then** it states that persistent browser storage of the token is an accepted limitation for this local learning application, that a script running in this page's origin can read the stored token, and that this authentication design is not production-ready. Backend authentication is unchanged.
8. **Given** this browser has no stored token, **When** the person looks for a way to recover the account, **Then** the screen says the service cannot replace a lost token. The application does not ask for a password or an email address, and it does not ask the service to issue a replacement token.

---

### User Story 2 - See my todos (Priority: P1)

An identified person sees every todo they own, including completed ones, newest first. The screen shows a loading state while the list is still arriving, and an empty state when the account owns nothing.

**Why this priority**: A saved account is useful only when the person can see the work that belongs to them.

**Independent Test**: With a known set of todos on one account, open the list and confirm each of that account's todos appears once, in newest-created order, with its title, description, completion, priority, and times. Confirm another account's todos are absent. With an account that owns none, confirm an empty state. Delay the list response and confirm a loading state appears before either items or the empty state.

**Acceptance Scenarios**:

1. **Given** an identified person owns one or more todos, **When** the list finishes loading, **Then** every todo they own appears once, newest created time first, showing title, description when one exists, whether it is completed, priority, created time, and updated time.
2. **Given** two todos were created at different times, **When** the list is shown, **Then** the newer one appears before the older one, and the screen does not rearrange items that share the same created time.
3. **Given** an identified person owns no todos, **When** the list finishes loading, **Then** the screen shows an empty state. That empty state is not an error.
4. **Given** the list request has not finished, **When** the person is looking at the list, **Then** a loading state is visible and the screen does not present an empty collection as a successful result.
5. **Given** person A and person B each own todos, **When** person A views the list, **Then** person B's todos are absent.
6. **Given** the person is not identified, **When** they open the list, **Then** no todos are shown and the screen says they must be identified.
7. **Given** a todo title or description contains markup or script-like text, **When** the list shows that todo, **Then** those characters are visible as text and do not run.

---

### User Story 3 - Add a todo (Priority: P1)

An identified person adds a todo with a title and, when they have more detail, a description and a priority of low, medium, or high. A new todo starts incomplete. When priority is left unset, it is medium.

**Why this priority**: Adding work is the first action that makes the list the person's own.

**Independent Test**: Add a todo with only a title and confirm it appears as incomplete, priority medium, with no description. Add another with a description and a chosen priority. Attempt a blank title, a title over 200 characters, and a description over 2,000 characters, and confirm nothing new appears.

**Acceptance Scenarios**:

1. **Given** an identified person is adding a todo, **When** they provide a title and a description and choose low, medium, or high, **Then** the new incomplete todo appears in the list with that title, description, and priority, without a manual reload.
2. **Given** an identified person is adding a todo, **When** they provide only a title, **Then** the todo appears as incomplete, with priority medium and no description.
3. **Given** an identified person is adding a todo, **When** the title is missing or only whitespace, **Then** nothing is added and the screen says a title is required.
4. **Given** an identified person is adding a todo, **When** the title is longer than 200 characters or the description is longer than 2,000 characters, **Then** nothing is added and the screen says which limit was exceeded.
5. **Given** an identified person is adding a todo, **When** they enter a title and description that have leading or trailing whitespace, **Then** the stored title and description shown afterward do not include that surrounding whitespace. A description that is only whitespace is stored as no description.
6. **Given** the person already has a todo with the same title, **When** they add another todo with that title, **Then** both todos appear as separate items.
7. **Given** a create request is still in progress, **When** the person tries to submit it again, **Then** a second create is not sent until the first one finishes.

---

### User Story 4 - Complete a todo and make it pending again (Priority: P1)

An identified person marks one of their todos completed, and later marks that completed todo pending again. The todo stays in the collection either way. Completing an already completed todo, or reopening an already pending todo, leaves it unchanged.

**Why this priority**: Recording that work is done, and correcting that mark, is the outcome the list exists to support.

**Independent Test**: Create an incomplete todo, mark it completed, and confirm the list shows it completed with the same title, description, priority, and created time. Mark it pending and confirm it shows incomplete with those same fields. Repeat each action once and confirm nothing changes the second time.

**Acceptance Scenarios**:

1. **Given** an incomplete todo is in the list, **When** the person marks it completed, **Then** it shows completed, stays in the list, and keeps the same title, description, priority, identifier, and created time. The updated time becomes the time of completion.
2. **Given** a todo is already completed, **When** the person marks it completed again, **Then** it stays completed and no field changes, including the updated time.
3. **Given** a completed todo is in the list, **When** the person marks it pending, **Then** it shows incomplete and keeps the same title, description, priority, identifier, and created time. The updated time becomes the time of that change.
4. **Given** a todo is already pending, **When** the person marks it pending again, **Then** no field changes.
5. **Given** the identifier is unknown or belongs to someone else, **When** the person marks it completed or pending, **Then** the screen says the todo does not exist, nothing changes, and the screen does not reveal that another person owns that identifier.
6. **Given** the person is not identified, **When** they mark a todo completed or pending, **Then** nothing changes and the screen says they must be identified.

---

### User Story 5 - Edit a todo (Priority: P2)

An identified person changes the title, the description, the priority, or any combination of those. Editing does not change whether the todo is completed and does not change its identifier.

**Why this priority**: The list is already usable with the original wording. Correction matters after create, complete, and reopen work.

**Independent Test**: Create a todo, change its title and description, and confirm the list shows the new text, the same completion and created time, and a later updated time. Clear the description and confirm the todo has none. Save without changing anything and confirm no update is sent. Open an edit for one todo and confirm a second edit of that same todo does not start until the first edit is saved or cancelled.

**Acceptance Scenarios**:

1. **Given** a todo is in the list, **When** the person changes its title and description, **Then** the list shows the new text, completion and created time stay the same, and the updated time becomes the time of the change.
2. **Given** a todo is in the list, **When** the person changes only the title, **Then** the description and priority stay as they were.
3. **Given** a todo has a description, **When** the person clears it, **Then** the todo shows no description and the title stays as it was.
4. **Given** a todo is in the list, **When** the person sets priority to low, medium, or high and changes nothing else, **Then** the list shows that priority and the title and description stay as they were.
5. **Given** a todo is in the list, **When** the person saves without changing title, description, or priority, **Then** no update is sent and the todo is unchanged.
6. **Given** a todo is in the list, **When** the person sets a blank title, a title longer than 200 characters, or a description longer than 2,000 characters, **Then** the todo stays as it was and the screen says which rule failed.
7. **Given** the identifier is unknown or belongs to someone else, **When** the person edits it, **Then** the screen says the todo does not exist and nothing is changed.
8. **Given** an edit of a todo is open, or its save is still in progress, in this page, **When** the person tries to start another edit of that same todo, **Then** the second edit does not open and a second update is not sent. An edit of a different todo can still start.
9. **Given** another browser tab, another browser, or another client changes the same todo while this page also changes it, **When** those updates overlap, **Then** this application does not detect, merge, or warn about that overlap. Simultaneous updates from different clients are outside this frontend's concurrency guarantee.

---

### User Story 6 - Delete a todo (Priority: P2)

An identified person permanently removes one of their todos after confirming the deletion. Canceling leaves the todo in place.

**Why this priority**: Cleanup matters after the person can add and finish work. Deletion is permanent, so it follows the everyday actions.

**Independent Test**: Create two todos, delete one after confirming, and confirm it is gone while the other remains. Start a delete, cancel it, and confirm the todo remains. Delete an identifier that is already gone and confirm the screen says it does not exist.

**Acceptance Scenarios**:

1. **Given** a todo is in the list, **When** the person asks to delete it and confirms, **Then** it disappears from the list and does not return on a later visit.
2. **Given** a todo is in the list, **When** the person asks to delete it and then cancels, **Then** the todo remains unchanged.
3. **Given** several todos are in the list, **When** the person deletes one, **Then** the others remain.
4. **Given** the identifier is unknown, already deleted, or belongs to someone else, **When** the person deletes it, **Then** the screen says the todo does not exist and no other todo changes.
5. **Given** the person is not identified, **When** they delete a todo, **Then** nothing changes and the screen says they must be identified.

---

### User Story 7 - Filter pending and completed todos (Priority: P2)

An identified person narrows the list to pending todos, completed todos, or all todos. Pending means not completed. The service returns the full list, so the filter only changes what the screen shows.

**Why this priority**: The full list is already useful. Filtering makes a longer list easier to scan.

**Independent Test**: With a known mix of pending and completed todos, choose each filter and confirm only the matching todos appear, still in newest-created order. Choose a filter that matches nothing and confirm a distinct empty filter state. Add, complete, reopen, edit, and delete a todo and confirm the selected filter still applies to the updated list.

**Acceptance Scenarios**:

1. **Given** the list has loaded, **When** the person has not chosen a filter, **Then** all of their todos are shown, pending and completed together.
2. **Given** the list contains both pending and completed todos, **When** the person chooses pending, **Then** only todos that are not completed are shown, newest created first among those shown.
3. **Given** the same list, **When** the person chooses completed, **Then** only completed todos are shown, newest created first among those shown.
4. **Given** a filter matches nothing, **When** the person selects it, **Then** the screen shows an empty filter state. That state is distinct from a failed load and from the empty state of an account that owns no todos.
5. **Given** a filter is selected, **When** the person adds, edits, completes, reopens, or deletes a todo successfully, **Then** the same filter still applies to the updated items.
6. **Given** the person changes filters, **When** the list was already loaded, **Then** the change does not require another wait, because the application is hiding and showing items it already retrieved.

---

### User Story 8 - Understand loading and failures (Priority: P1)

When something goes wrong, the person can tell whether they must identify themselves, the todo is missing, the entered values were rejected, the client timed out, the proxy returned HTTP 502 or HTTP 504, the service returned another HTTP 5xx, or the browser could not reach the service. The screen stays on the last successful list when a later action fails. Messages do not include the token, raw response bodies, stack traces, database text, or other internal details.

**Why this priority**: A list the person cannot trust during a failure is not yet usable. This story can be demonstrated with account creation and the list alone.

**Independent Test**: Force an unknown token, a rejected title, a missing todo, a client timeout, HTTP 502, HTTP 504, another HTTP 5xx, and a browser network failure. Confirm each shows a different message, the token never appears in the message, and a failed action after a successful list leaves the previous items on screen. Confirm a cancellation caused by an account change does not show the timeout message.

**Acceptance Scenarios**:

1. **Given** the person is not identified or the token is unknown, **When** a todo action is attempted, **Then** the screen says they must be identified and offers account creation or entry of a saved token.
2. **Given** the service rejects a title, description, or priority, **When** the person reads the message, **Then** it states the failed rule in plain language. The stored todos stay as they were.
3. **Given** the service reports that a todo does not exist, **When** the person reads the message, **Then** it says the todo was not found and does not say whether another account owns that identifier.
4. **Given** the current account session's request reaches its 10-second limit, **When** the person reads the message, **Then** it says the request timed out. That message is not used when the request was cancelled because the account session changed.
5. **Given** the proxy returns HTTP 502, **When** the person reads the message, **Then** it says the proxy could not get a valid response from the service.
6. **Given** the proxy returns HTTP 504, **When** the person reads the message, **Then** it says the proxy timed out waiting for the service. That message is distinct from the client timeout.
7. **Given** the service returns another HTTP 5xx or a response the application cannot read, **When** the person reads the message, **Then** it says the action could not be completed.
8. **Given** the browser cannot reach the service, **When** the person attempts an action, **Then** the screen says the service could not be reached. That message is distinct from the client timeout, HTTP 502, HTTP 504, and other HTTP 5xx.
9. **Given** any client-timeout, HTTP 502, HTTP 504, other HTTP 5xx, or browser-network message, **When** the person reads it, **Then** it contains no stack trace, database text, credential, token, or raw response body.
10. **Given** the list was already shown, **When** a later action fails, **Then** the last successful items remain visible along with the error. The screen does not replace them with an empty success state.
11. **Given** the first list load fails, **When** the person is waiting, **Then** loading ends, an error is shown, and an empty success state is not shown.
12. **Given** any failure message or diagnostic record produced by the check, **When** it is inspected, **Then** the bearer token is absent.
13. **Given** account creation, create, edit, complete, reopen, or delete is still in progress, **When** the person looks at that action, **Then** a loading state is visible for it.

---

### User Story 9 - Run the frontend locally and in the local container stack (Priority: P2)

A contributor starts the browser application on its own for local development, and starts it with the existing API and Prometheus stack for a containerized run. In both supported setups the browser talks to one local address, and that address forwards todo and account requests to the existing API. The API and Prometheus stay on their current loopback addresses.

**Why this priority**: The todo flows above can be demonstrated against a running API before the container packaging is in place. Packaging is what makes the same flows repeatable for the next contributor.

**Independent Test**: From a clean checkout, follow only the local development steps and complete account creation and one todo at the documented dev address. Follow only the container steps and complete the same flow at the documented container address. Confirm the API is still at `http://127.0.0.1:8000`, Prometheus is still at `http://127.0.0.1:9090`, and both published frontend ports bind to `127.0.0.1`.

**Acceptance Scenarios**:

1. **Given** the documented local prerequisites, **When** a contributor follows the local development steps, **Then** the browser application is reachable at `http://127.0.0.1:5173` and account and todo requests from that page reach the existing API at `http://127.0.0.1:8000`.
2. **Given** the documented container prerequisites, **When** a contributor starts the existing stack with the frontend included, **Then** the browser application is reachable at `http://127.0.0.1:8080`, the API remains reachable at `http://127.0.0.1:8000`, and Prometheus remains reachable at `http://127.0.0.1:9090`.
3. **Given** either supported setup, **When** the page loads, **Then** the browser uses the frontend address for both the screen and `/api/v1` requests. The published frontend port binds to `127.0.0.1`.
4. **Given** the API container is recreated, **When** the contributor looks for todo rows saved only inside that container, **Then** this feature still does not keep those rows. The documented limitation stays as it is today.
5. **Given** the documented frontend port is already in use, **When** the contributor starts that mode, **Then** startup fails with a visible error instead of attaching to an unrelated process.
6. **Given** the frontend is built for the container, **When** the build runs, **Then** it completes from the frontend directory without installing the backend package.
7. **Given** the container stack is running, **When** the contributor inspects Prometheus targets, **Then** the existing API metrics endpoint is still the scrape target and the frontend is not a scrape target.
8. **Given** the container stack is running, **When** the contributor lists its services, **Then** they are the frontend, the existing API, and Prometheus.

---

### User Story 10 - Check the frontend and troubleshoot it (Priority: P2)

A contributor can run TypeScript type checking, ESLint, Vitest, React Testing Library, Playwright, and a frontend dependency vulnerability check. Playwright uses an isolated local environment and disposable test data. The existing backend pytest checks still pass at the current coverage gate. After the application exists, a dedicated operations handbook explains how to investigate frontend failures with safe local exercises.

**Why this priority**: The screen can be tried by hand before the checks and the handbook exist. Those checks, and a handbook written against the finished application, are what make the result repeatable and supportable.

**Independent Test**: Run the documented frontend checks and confirm type checking, lint, component checks, and the vulnerability check pass. Run Playwright against a disposable local dataset and confirm it creates an account and completes the todo workflow, then confirm that data is discarded and the contributor's existing todo database was not used. Run the existing backend pytest checks and confirm they still pass. After implementation, open `tutorials/frontend-operations-handbook/` and complete one documented exercise, including rollback to the starting state.

**Acceptance Scenarios**:

1. **Given** the documented frontend check commands, **When** a contributor runs them, **Then** TypeScript type checking and ESLint pass, and the Vitest and React Testing Library checks pass without a live API. Those component checks cover rendering, service communication through a substitute, user interactions, authentication failure, HTTP errors, and network failure.
2. **Given** the documented Playwright command, **When** a contributor runs it, **Then** it uses an isolated local environment and disposable test data. It creates an account and completes create, edit, complete, reopen, delete, and filter, and it covers an authentication failure and an HTTP error. The contributor's existing todo database is not used. The disposable data is discarded at the end. The check does not add a fault endpoint to the API.
3. **Given** a pull request or a push to the main branch, **When** the existing automation runs, **Then** the current backend lint, format, type-check, and coverage-gated pytest jobs still run and pass. The frontend automation also runs TypeScript type checking, ESLint, Vitest, React Testing Library, Playwright, and the dependency vulnerability check. The backend coverage gate is unchanged.
4. **Given** the contributor setup documents, **When** a new contributor looks up this feature, **Then** they can find local development steps, build and test commands, and container deployment steps.
5. **Given** the frontend implementation is complete, **When** a contributor opens `tutorials/frontend-operations-handbook/`, **Then** the handbook covers frontend architecture, a React and TypeScript overview, the browser-to-FastAPI request lifecycle, browser developer tools, authentication troubleshooting, CORS troubleshooting, the Nginx reverse proxy, Docker networking, CI/CD troubleshooting, and API latency and availability troubleshooting. Its examples match the running application.
6. **Given** one handbook exercise, **When** a contributor follows it, **Then** it uses a safe local or simulated failure and records symptoms, investigation steps, root cause, remediation, validation, and rollback. Completing the rollback returns the local environment to its starting state.
7. **Given** the frontend dependency manifest, **When** a contributor reviews it, **Then** the application is React and TypeScript, built with Vite, checked with TypeScript, ESLint, Vitest, React Testing Library, and Playwright, and styled with HTML and CSS. Service calls use the native Fetch API. The manifest does not include a state-management library or a user-interface framework, and the application does not load third-party scripts.
8. **Given** the frontend source and the container definition, **When** a contributor inspects them, **Then** screen presentation and service communication are separate, the contract types name only fields the existing service accepts or returns, and no committed file contains a token, a password, or todo contents.
9. **Given** the documented dependency vulnerability check, **When** a contributor runs it as part of the frontend development workflow, **Then** it reports known vulnerabilities in frontend dependencies. A high or critical finding fails the check. The backend checks are unchanged.

---

### Edge Cases

- Account creation collects no name, email, or password. The only credential is the bearer token returned once by the existing account action. Backend authentication is unchanged.
- Persistent browser storage of that token is an accepted limitation for this local learning application. It is not a production-ready authentication design. A script that runs in the page origin can read the stored token. This is the XSS exposure accepted for this application.
- The application does not write the token to logs, error messages, diagnostic output, the URL path, the query, or the fragment. The one-time display and the field where the person enters a saved token are the exceptions.
- The application does not load third-party scripts. Its scripts ship with the application.
- Title, description, and any other user-provided text are shown as text. Markup or script-like characters in that text are visible and do not run.
- Closing and reopening the browser keeps the person identified until they leave the account or clear this site's stored data. Reloading the page does the same.
- Leaving the account removes the token from this browser only. It does not revoke the backend credential, delete the account, or delete that account's todos. The same token works when presented again.
- A person who loses the token and clears site data cannot recover that account from the service. The screen says the service cannot replace a lost token. Todos for that account remain stored and stay unreachable until the same token is presented again.
- A wrong token, a missing token, and a cleared token all end in the same identified-person message. The screen does not say which of those cases the service saw, beyond that the person must be identified.
- The one-time token display is the only place the application reveals a token on its own. Entering a saved token is a field the person fills in. Copying the token is the person's action.
- Title and description limits match the service: a title must contain non-whitespace text and be at most 200 characters; a description, when present, must be at most 2,000 characters. Surrounding whitespace is removed. A whitespace-only description means no description.
- Priority on the screen offers only low, medium, and high. Leaving it unset on create shows medium after the todo is saved. Leaving it unset on edit keeps the stored priority.
- Two todos may share a title. The identifier is the identity the person does not choose and cannot edit.
- Marking a completed todo completed again, or a pending todo pending again, keeps every field the same and is not shown as a failure.
- Delete asks for confirmation. Cancel leaves the todo. Confirm removes it permanently. The same identifier is not reused, and the item cannot be restored from the screen.
- The list filter never asks the service for a subset. The service has no filter on the list action. Pending shows items that are not completed. Completed shows items that are completed. All shows both.
- An empty account and a filter that matches nothing are different empty screens. A failed load is different from both.
- A slow list shows loading until it succeeds or fails. A second submit is not sent while create, edit, complete, reopen, or delete is still in progress.
- After the list has succeeded once, a failed later action leaves those items on screen and shows the error. A failed first load shows the error and does not look like an empty account.
- Validation failure, not-found, and unauthenticated each have their own message. A client timeout, HTTP 502, HTTP 504, any other HTTP 5xx, and a browser network failure also have distinct messages. A session-change cancellation is not shown as a timeout. Not-found does not reveal that another person owns the identifier. None of these messages includes a raw response body, credential, database text, or stack trace.
- One page allows only one open or in-progress edit of a given todo. A second edit of that same todo does not start. An edit of a different todo can start. Complete, reopen, and delete stay separate actions and are still sent one at a time.
- Another tab, browser, or client can still update the same todo at the same time. This frontend does not detect or merge that overlap, and it does not add a version field or optimistic concurrency control. The existing service behavior remains the authority for that case.
- The page and the API share one browser origin in both supported setups. Pointing the page at the API's separate address is unsupported. The API does not currently grant cross-origin browser access, and this feature does not add that grant.
- A wrong forwarded address, a stopped API, a frontend build failure, a busy published port, and a container that cannot reach the API service are operational failures. The troubleshooting guide distinguishes them. They do not change todo data by themselves.
- Recreating the API container can discard todo rows stored only in that container. This feature does not change that.
- Automated network and HTTP failure checks are simulated from the frontend. They do not add an error, delay, or corruption endpoint to the API.
- Playwright runs in an isolated local environment. Its accounts and todos are disposable and are discarded when the run ends. The contributor's existing todo database is left untouched.
- The frontend dependency vulnerability check fails on a high or critical finding. Lower findings are reported and do not fail the check by default.
- The detailed operations handbook is written after the frontend implementation, at `tutorials/frontend-operations-handbook/`. Its exercises use safe local or simulated failures. Each exercise includes symptoms, investigation steps, root cause, remediation, validation, and rollback. This specification does not contain that handbook.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The application MUST let a person create an account through the existing account action, without collecting a name, email, or password.
- **FR-002**: After account creation, the application MUST show the account identifier and the bearer token once. The service returns that token only in that response.
- **FR-003**: The application MUST keep that token in the browser's persistent storage for this site so a reload or a new visit in the same browser stays identified, until the person leaves the account or clears the site's stored data. Persistent storage is an accepted limitation for this local learning application, and this authentication design MUST be documented as not production-ready. A script running in the page origin can read the stored token. That exposure MUST be documented. Backend authentication MUST remain unchanged.
- **FR-004**: The application MUST let a person leave the account. Logout MUST remove the locally stored token. Logout MUST NOT revoke, expire, or delete the backend credential, and MUST NOT delete the account or its todos. The same token MUST still be accepted when the person presents it again.
- **FR-005**: The application MUST let a person present a token they saved earlier and then use that account's todos. When no token is stored, the application MUST say that the service cannot replace a lost token. It MUST NOT collect a password or an email address, and it MUST NOT ask the service to issue a replacement token.
- **FR-006**: Todo actions MUST send the token as the bearer credential the existing todo actions already require.
- **FR-007**: A missing or unrecognized credential MUST stop the todo action, leave todos unchanged, and tell the person they must be identified.
- **FR-008**: The token value MUST NOT appear in the URL path, query, or fragment, in application logs, in error messages, in diagnostic output, in committed files, or in built images. The only on-screen exceptions are the one-time display after account creation and the field where the person enters a saved token.
- **FR-009**: An identified person MUST be able to see every todo they own, including completed ones, newest created time first. Items that share a created time MUST keep the order the service returned.
- **FR-010**: Each listed todo MUST show its title, its description when it has one, whether it is completed, its priority, its created time, and its updated time.
- **FR-011**: The list MUST exclude every todo owned by another person.
- **FR-012**: An identified person who owns no todos MUST see an empty state after a successful load. That empty state MUST NOT be presented while the load is still running or after the load failed.
- **FR-013**: The application MUST show a loading state while the list request, account creation, create, edit, complete, reopen, or delete request is in progress.
- **FR-014**: While one of those requests is in progress, the application MUST NOT send a duplicate of that same submission.
- **FR-015**: An identified person MUST be able to add a todo with a title, an optional description, and an optional priority of low, medium, or high. The new todo MUST appear in the list without a manual reload, start incomplete, and show priority medium when priority was left unset.
- **FR-016**: The application MUST reject a missing or whitespace-only title, a title longer than 200 characters, and a description longer than 2,000 characters, leave stored todos unchanged, and say which rule failed.
- **FR-017**: The application MUST show the title and description as stored after surrounding whitespace is removed. A whitespace-only description MUST result in no description.
- **FR-018**: The application MUST allow two todos with the same title to appear as separate items.
- **FR-019**: An identified person MUST be able to mark their own incomplete todo completed. It MUST remain in the list, show completed, and keep the same title, description, priority, identifier, and created time, with the updated time set to the time of completion.
- **FR-020**: Marking an already completed todo completed again MUST leave every field unchanged and MUST NOT be shown as a failure.
- **FR-021**: An identified person MUST be able to mark their own completed todo pending. It MUST show incomplete and keep the same title, description, priority, identifier, and created time, with the updated time set to the time of that change.
- **FR-022**: Marking an already pending todo pending again MUST leave every field unchanged and MUST NOT be shown as a failure.
- **FR-023**: An identified person MUST be able to change the title, the description, the priority, or any combination of those on their own todo, without changing its completed state or its identifier.
- **FR-024**: An edit MUST change only the title, description, or priority the person actually changes. Clearing the description MUST leave the todo with no description.
- **FR-025**: Saving an edit that changes neither title, description, nor priority MUST NOT send an update.
- **FR-026**: The priority control MUST offer only low, medium, and high.
- **FR-027**: Within one page, the application MUST prevent a second overlapping edit of the same todo. While an edit of a todo is open or its save is in progress, another edit of that same todo MUST NOT start and MUST NOT be sent. An edit of a different todo MAY start. The application MUST NOT add optimistic concurrency control, a version field, or a backend change for this rule. Simultaneous updates from different clients, including another browser tab, are outside the frontend's concurrency guarantees.
- **FR-028**: An identified person MUST confirm before a todo is deleted. Confirming MUST permanently remove it from the list. Canceling MUST leave it unchanged.
- **FR-029**: Deleting one todo MUST leave that person's other todos unchanged.
- **FR-030**: Edit, complete, reopen, and delete of an unknown identifier, or of an identifier owned by someone else, MUST say the todo does not exist, change nothing, and MUST NOT reveal that another person owns it.
- **FR-031**: The person MUST be able to show all todos, only pending todos, or only completed todos. The initial view MUST be all todos. Pending means not completed.
- **FR-032**: Filtering MUST be applied to the list the service already returned. The application MUST NOT send a filter, search, or paging parameter the list action does not provide.
- **FR-033**: The selected filter MUST remain in effect after a successful add, edit, complete, reopen, or delete. Items that share a created time MUST keep their returned order inside the filter.
- **FR-034**: A filter that matches nothing MUST show an empty filter state that is distinct from a failed load and from the empty state of an account that owns no todos. Changing the filter on an already loaded list MUST NOT require a new wait.
- **FR-035**: The application MUST distinguish these outcomes in plain language: the person must be identified, the entered values were rejected, the todo was not found, a client timeout, HTTP 502, HTTP 504, any other HTTP 5xx, and a browser network failure. The five transport outcomes MUST use different messages. A cancellation caused by an account-session change MUST NOT use the client-timeout message.
- **FR-036**: HTTP 5xx responses other than 502 and 504, and responses the application cannot read, MUST produce one general failure message. Client timeout, HTTP 502, HTTP 504, and a browser network failure MUST NOT reuse that message. None of these messages MUST include a stack trace, database text, credential, token, or raw response body.
- **FR-037**: After a list has loaded successfully, a later failed action MUST leave the last successful items visible and show the error. A failed first load MUST show the error and MUST NOT look like an empty account.
- **FR-038**: The frontend MUST live in a new `frontend/` directory and MUST build without installing the backend package.
- **FR-039**: The frontend MUST be a React and TypeScript application built with Vite, styled with HTML and CSS, and MUST call the service with the native Fetch API. It MUST NOT add a state-management library or a user-interface framework.
- **FR-040**: TypeScript interfaces MUST describe the existing account and todo contracts, and MUST use only fields and actions present in the repository. Screen presentation and service communication MUST be separate, so a visible label can change without rewriting the contract types.
- **FR-041**: The service address the frontend uses MUST come from environment configuration. Supported local and container setups MUST make the browser use one origin for the screen and for `/api/v1` requests, by forwarding those requests to the existing API. This feature MUST NOT add a cross-origin grant to the API.
- **FR-042**: Local development MUST serve the application at `http://127.0.0.1:5173` and forward `/api/v1` to the existing API at `http://127.0.0.1:8000`. The published dev address MUST bind to `127.0.0.1`.
- **FR-043**: The container stack MUST add a frontend service without removing the existing API or Prometheus services. Nginx MUST serve the built frontend and forward `/api/v1` to the existing API service. The frontend MUST be published at `http://127.0.0.1:8080`. The API MUST remain at `http://127.0.0.1:8000` and Prometheus at `http://127.0.0.1:9090`. Published ports MUST bind to `127.0.0.1`.
- **FR-044**: A busy documented frontend port MUST fail startup visibly.
- **FR-045**: Existing account and todo behavior, status outcomes, error shapes, ownership rules, backend tests, and the current backend lint, format, type-check, and coverage-gated test jobs MUST stay as they are. This feature MUST NOT add a backend fault-injection endpoint.
- **FR-046**: Prometheus MUST keep scraping the existing API metrics endpoint. The frontend MUST NOT become that scrape target.
- **FR-047**: The frontend development workflow MUST include TypeScript type checking, ESLint, Vitest, and React Testing Library. The Vitest and React Testing Library checks MUST run without a live API and MUST cover rendering, service communication, user interactions, authentication failure, HTTP errors, and network failure.
- **FR-048**: Playwright integration tests MUST use an isolated local environment with disposable test data. They MUST cover account creation, create, edit, complete, reopen, delete, filter, an authentication failure, and an HTTP error. They MUST discard that test data at the end and MUST NOT read or write the contributor's existing todo database. They MUST NOT add a fault endpoint to the API.
- **FR-049**: The same pull request and main-branch automation that runs the backend jobs MUST also run the frontend checks: TypeScript type checking, ESLint, Vitest, React Testing Library, Playwright, and the dependency vulnerability check. The current backend lint, format, type-check, and coverage-gated pytest jobs MUST remain, and the backend coverage gate MUST NOT be lowered.
- **FR-050**: Contributor setup documentation MUST explain local development, build and test commands, and container deployment. A dedicated SRE-focused frontend operations handbook MUST be created at `tutorials/frontend-operations-handbook/` after the frontend implementation, so its examples match the running application. This specification does not author that handbook. The handbook MUST cover frontend architecture, a React and TypeScript overview, the browser-to-FastAPI request lifecycle, browser developer tools, authentication troubleshooting, CORS troubleshooting, the Nginx reverse proxy, Docker networking, CI/CD troubleshooting, and API latency and availability troubleshooting. It MUST include practical failure-injection exercises that use safe local or simulated failures. Each exercise MUST document symptoms, investigation steps, root cause, remediation, validation, and rollback, and MUST restore the local environment. Exercises MUST NOT add a fault-injection endpoint to the API. The authentication chapter MUST record the accepted token-storage limitation, the XSS exposure of persistent browser storage, the ban on token logging and tokens in URLs, safe rendering of user-provided content, the ban on third-party scripts, and the fact that logout removes only the local token.
- **FR-051**: Committed configuration and images MUST NOT contain tokens, passwords, or todo contents. Local defaults MAY exist only when they are not secrets.
- **FR-052**: This feature MUST NOT add PostgreSQL, Redis, Kubernetes, an API gateway, a second identity system, or any other service beyond the frontend and the existing API and Prometheus stack.
- **FR-053**: The application MUST render title, description, and any other user-provided text as text. Markup or script-like content in those fields MUST remain visible as characters and MUST NOT execute.
- **FR-054**: The application MUST NOT load third-party scripts. Scripts MUST ship with the application itself.
- **FR-055**: The frontend development workflow MUST include a dependency vulnerability check for frontend dependencies. A high or critical finding MUST fail the check. Lower findings MUST be reported and MUST NOT fail the check by default. This check MUST NOT change the backend test jobs or the backend coverage gate.

### Key Entities *(include if feature involves data)*

- **Person**: An account created by the existing service. The browser learns an identifier and a one-time bearer token. The account has no name, email, or password in this feature. The same token sees the same todos until the person deletes them.
- **Access credential**: The bearer token the service issues once. The browser stores it for this site until the person leaves the account or clears site data. Logout removes that local copy and leaves the backend credential valid. The person can present a saved token again. The service does not replace a lost token. Persistent storage is an accepted local-learning limitation, not a production-ready design.
- **Todo**: One piece of work owned by exactly one person. The screen shows the identifier, title, description, completed flag, priority, created time, and updated time that the service already returns. Ownership is not a displayed field. Priority is low, medium, or high.
- **List view**: All, pending, or completed. It is a view over the person's already retrieved todos. It is not a separate collection and it is not a service filter.
- **Failure notice**: The plain-language result of a rejected credential, rejected values, a missing todo, a client timeout, HTTP 502, HTTP 504, any other HTTP 5xx, or a browser network failure. It is distinct from loading and from an empty list. It contains no raw response body, credential, database text, or stack trace.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A person with no account in the browser can create an account, see the token once, add a todo using only a title, and see that todo in the list, in one pass, in under 2 minutes.
- **SC-002**: In a check with two accounts, 100% of each account's own todos appear once, newest created time first, and 0% of the other account's todos appear.
- **SC-003**: In 100% of successful attempts, edit, complete, reopen, and confirmed delete leave the list matching the stored todo. In 100% of rejected title, description, and priority attempts, the stored todo is unchanged and the screen states the failed rule.
- **SC-004**: On a list of 50 todos with a known mix of pending and completed items, all, pending, and completed each show exactly the matching items, with no item in the wrong group.
- **SC-005**: A list response that has not finished shows a loading state first. A failed first load shows an error and does not show an empty success state. After a successful load, a failed later action keeps the last successful items visible in 100% of checks.
- **SC-006**: Unauthenticated, rejected values, and not-found each produce their own message. A client timeout, HTTP 502, HTTP 504, any other HTTP 5xx, and a browser network failure produce five further messages that differ from each other and from a session-change cancellation. The token value appears in 0 of those messages and in 0 of the diagnostic records from the check. No message includes a raw response body, credential, database text, or stack trace.
- **SC-007**: Leaving the account removes the token from the browser, and presenting that same saved token shows the same todos again, in 100% of checks. The backend credential remains valid after logout. An unrecognized token shows that the person must be identified and shows none of those todos, in 100% of checks.
- **SC-008**: TypeScript type checking, ESLint, Vitest, and React Testing Library pass, including rendering, service communication, interactions, authentication failure, HTTP errors, and network failure. Playwright passes against disposable local data and covers the create, edit, complete, reopen, delete, and filter workflow. The dependency vulnerability check passes when frontend dependencies have no high or critical finding. The existing backend pytest checks pass at the current coverage gate.
- **SC-009**: A contributor who already has the documented prerequisites finishes the local account-and-todo flow at `http://127.0.0.1:5173` within 15 minutes, and finishes the same flow from the container stack at `http://127.0.0.1:8080` within 15 minutes. The API stays at `http://127.0.0.1:8000` and Prometheus stays at `http://127.0.0.1:9090`.
- **SC-010**: After implementation, `tutorials/frontend-operations-handbook/` covers all ten required topics: frontend architecture, React and TypeScript, the browser-to-FastAPI request lifecycle, browser developer tools, authentication troubleshooting, CORS troubleshooting, the Nginx reverse proxy, Docker networking, CI/CD troubleshooting, and API latency and availability troubleshooting. Every failure-injection exercise records symptoms, investigation steps, root cause, remediation, validation, and rollback.
- **SC-011**: A contributor completes one documented handbook exercise using a safe local or simulated failure and returns the local environment to its starting state within 30 minutes. In a separate check, a title containing markup is displayed as text and executes in 0% of cases. In one page, a second overlapping edit of the same todo is sent in 0% of attempts.

## Assumptions

- The audience is the person managing their own todos, and the contributor who runs, checks, and troubleshoots the frontend. People do not share todos, and there is no role that can see another person's list.
- Any edit that still touches the backend remains governed by the project constitution: layered architecture, typed contracts, backend tests, the REST error policy, environment-only secrets, and SQLite as the default local database. The supported same-origin setup does not require a backend change. This feature does not amend the constitution.
- The existing service contract was verified in this repository before this specification was written. Account creation is `POST /api/v1/users` with no request body and a `201` response containing `id` and `token`. Todo actions are bearer-protected: `GET` and `POST /api/v1/todos`, `GET` and `PATCH` and `DELETE /api/v1/todos/{id}`, `POST /api/v1/todos/{id}/complete`, and `POST /api/v1/todos/{id}/incomplete`. A todo contains `id`, `title`, `description`, `completed`, `priority`, `created_at`, and `updated_at`. Priority is `low`, `medium`, or `high`, and an omitted create priority is stored as medium. The list is newest `created_at` first. Delete succeeds with an empty `204`. Unauthenticated responses use `401` and `{error:{code,message}}` with the message that the person must be identified. A missing or unowned todo uses `404` and `{error:{code,message}}` with the not-found message. Rejected values use the framework's `422` validation body. There is no sign-in, password, token refresh, token revoke, server-side filter, or paging action.
- A separate screen for opening one todo by identifier is not required. The list already returns the fields the person needs. The single-todo action remains available on the service and is unchanged.
- Token handling was evaluated against that contract. Keeping the token only in page memory would drop it on reload, and the service cannot issue it again. An httpOnly cookie would require the service to change how identification works, so it is out of scope. Persistent site storage, a one-time on-screen display, and a way to present a saved token are the chosen behavior for this local learning application. That choice is an accepted limitation and is not production-ready. A script that runs in the page origin can read the stored token. The application does not load third-party scripts, does not write the token into logs, URLs, messages, diagnostics, source, or images, and renders user-provided todo text as text. Logout removes only the browser copy.
- One page keeps a single edit open for a given todo. The rule does not cover another tab or another client. Those overlapping updates stay on the existing service behavior. The frontend does not add a version, a precondition, or a merge step. Complete, reopen, and delete are not a second edit form. Each of those actions is still sent once while its own request is in progress.
- The vulnerability check's failing threshold is high or critical. Moderate and low findings are reported and do not fail the default check. The tool itself is chosen during planning, provided it checks frontend dependencies and uses that threshold.
- Playwright's launch mechanism is chosen during planning. The required outcome is an isolated local run whose accounts and todos are created for the run and discarded afterward, without using the contributor's existing todo database.
- The operations handbook is a feature deliverable written after the application exists. Chapter file names inside `tutorials/frontend-operations-handbook/` are chosen then, provided every required topic and every exercise section is present. Setup documents for local development, build, test, and container deployment can be written with the implementation. They do not replace the handbook.
- The initial list view is all todos, so completing an item does not make it disappear until the person chooses the pending filter.
- Delete asks for confirmation because the service removes the todo permanently.
- Saving an edit with no changed title, description, or priority does not send a request. The service would reject an empty update.
- Both supported deployments keep the browser on the frontend origin and forward `/api/v1` to the API. Local development forwards to `127.0.0.1:8000`. The container stack forwards to the existing `todo-api` service on the stack network. The API process is not given a new cross-origin policy. Calling the API's separate origin directly from the page is an unsupported configuration described in troubleshooting.
- The forwarded service address is environment configuration. No secret is required for the local or container default. A missing or wrong address is an operational failure, not a todo-data failure.
- Local development uses `http://127.0.0.1:5173`. The containerized frontend uses `http://127.0.0.1:8080`. Both bind to loopback. A port that is already taken fails startup visibly.
- The existing root container stack remains the deployment definition. This feature adds the frontend service to it. API SQLite data inside the API container still disappears when that container is recreated. Prometheus samples remain on their existing volume. This feature does not add a database volume.
- Frontend component and interaction checks do not need a live API. Playwright integration tests use the existing API in an isolated local environment with disposable data, not a second backend and not the contributor's normal database. Network and HTTP failures in the component checks are simulated in the frontend test. Handbook exercises use safe local or simulated failures. Neither adds failure endpoints to the API.
- The existing GitHub Actions workflow keeps its backend lint, format, type-check, and coverage-gated pytest jobs, and gains the frontend checks on the same pull request and main-branch triggers. The frontend checks are TypeScript type checking, ESLint, Vitest, React Testing Library, Playwright, and the dependency vulnerability check. The backend coverage gate stays where it is.
- Display formatting of timestamps may be local to the browser as long as two times can be compared and the stored order stays newest created first.
- No git branch is created by this specification. The feature directory is `specs/004-react-todo-frontend`.

## Out of Scope

- Replacing, rewriting, or redesigning the existing API, its SQLite persistence, its bearer-token rules, or its Prometheus scrape. Backend authentication is not modified.
- Treating this authentication design as production-ready. Sign-in, passwords, email, display names, token refresh, token revocation, httpOnly cookies, shared lists, roles, and account recovery beyond presenting the original token are out of scope.
- Optimistic concurrency control, version fields, and frontend guarantees about simultaneous updates from different clients.
- A dedicated single-todo page, search, paging, due dates, tags, subtasks, bulk edits, and server-side filtering.
- PostgreSQL, Redis, Kubernetes, an API gateway, a second identity provider, a user-interface framework, and a frontend state-management library.
- Changing the API to grant cross-origin browser access.
- Making API container SQLite data survive container recreation.
- Artificial backend endpoints for errors, latency, or data corruption. Handbook exercises and automated failure checks stay on safe local or simulated failures.
- Writing the detailed operations handbook before the frontend implementation exists.
- Lowering or removing the existing backend pytest coverage gate, or replacing those backend jobs with frontend checks.
