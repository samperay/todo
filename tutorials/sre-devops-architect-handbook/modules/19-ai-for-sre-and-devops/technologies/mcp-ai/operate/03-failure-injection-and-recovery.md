# MCP and AI-assisted Todo — Operate 03: Failure injection and recovery

## Learning objective

Use disposable isolated labs; define failure and rollback before testing.

### Prerequisites and safety

Run commands from the **Todo repository root** unless stated otherwise. Check the active branch first. Docker commands require a running Docker engine. Commands involving containers create only isolated lab resources; never reuse production names or credentials. Expected outputs may vary by version and environment.

## Real-world analogy

In our restaurant, the manager first defines the change, then verifies service quality. Restaurant concierge can look up orders, but changing an order requires the customer’s permission.

### Mapping the analogy to Todo

```text
Customer → Waiter → Order board → Chef → Completed order

Todo user → React → FastAPI → Todo service → SQLite
Proposed read-only Todo tools first; no autonomous write access.
```

**Current vs proposed:** Proposed read-only Todo tools first; no autonomous write access. Check actual repository files before asserting a component exists.

## Explanation

This lesson addresses **failure injection and recovery**. Begin by identifying who initiates the action, which component owns the work, what data changes, and what happens when the dependency is unavailable. In Todo, always trace the authenticated request and preserve owner isolation. A green infrastructure check is not sufficient evidence of a successful user journey.

### Architecture reasoning

- **Correctness:** What state is authoritative? What invariants must never break?
- **Reliability:** How does the API behave during dependency failure or restart?
- **Security:** Which identities and trust boundaries are involved?
- **Operability:** Which observable signal would prove success or failure?
- **Complexity:** What operational cost is introduced versus retaining the current architecture?

## Guided exercise

### Step 1 — Run the demonstration

```bash
git status --short
docker compose ps
```

### Step 2 — Expected output

```text
<current state>
```

### Step 3 — What to Observe

**Code/command observation:** Never stop production services; inject failures only in approved disposable environments.

**Output observation:** Compare each printed value or response with the command that produced it. Placeholders in angle brackets denote environment-specific output, not guaranteed literal text. If a prerequisite is missing, record the error and do not claim the lesson passed.

**Todo observation:** Inspect `backend/src/todo_api/`, `compose.yaml`, and existing tests as relevant. Distinguish *verified implementation*, *standalone demonstration*, and *proposed architecture*.

## Intermediate — Todo integration thinking

1. Identify the exact Todo endpoint, service, or operational workflow affected by **failure injection and recovery**.
2. State one acceptance criterion that can be checked automatically and one user-visible failure symptom.
3. Decide whether a code change is justified now. If yes, first create a feature branch and SDD specification; do not edit the running application as part of this standalone lesson.

### Evidence to collect

Record the actual command, output, affected Todo component, and an explanation of why the output supports your conclusion. No `progress/` directory or file update is required.

## Architect — Failure and design challenge

A dependency is slow or unavailable while a user is attempting to list or complete Todos. Describe the failure boundary, timeout/fallback behavior, data consistency implications, observability, recovery procedure, and rollback. Compare **no new technology** with the proposed component and justify the added operational cost.

### Decision checklist

- Can authenticated users still access only their own Todos?
- Does the system recover without data loss or duplicate side effects?
- Can an operator distinguish application failure from dependency failure?
- Is there a documented cleanup/rollback path?

## Troubleshooting and cleanup

For a failed command, first check the current working directory, executable availability, and relevant service health. Do not execute destructive cleanup against an unknown container. Isolated containers used in this track can be removed **only after confirming they contain no needed data**; e.g., `docker rm -f todo-redis-lab` for the dedicated Redis lab.

## Knowledge check

1. Explain **failure injection and recovery** using the restaurant analogy and then Todo.
2. Which command/output provides evidence, and what does it *not* prove?
3. What failure mode would concern an SRE most, and how would you detect it?

## Completion gate

Explain the result in your own words, verify the real output, and answer the knowledge check before moving to the next lesson. The tutor should link this file rather than copy all commands into chat.
