# Spec Kit Tutorial — FastAPI Todo Project

> A practical, end-to-end guide for the existing `todo` repository, using Cursor IDE, FastAPI, SQLAlchemy, SQLite, and pytest. Updated October 2026.

## 1. Goal and mental model

Spec-driven development (SDD) means agreeing on **what** software must do before deciding **how** to build it. Treat specifications as living artifacts that must remain aligned with the code, rather than disposable prompts.

```text
Idea → Constitution → Specification → Clarification → Technical plan
     → Quality checklist → Tasks → Analysis → Implementation → Convergence
     → Tests/review → Commit
```

**Three questions to remember:**

- **Constitution:** What engineering rules must every feature follow?
- **Specification:** What must users be able to do, and what behavior counts as correct?
- **Plan:** How will we implement those requirements with our chosen architecture and tools?
- **Tasks:** What small, verifiable pieces of work deliver the plan?

Do not ask Cursor to code before the requirements and acceptance criteria are understood.

## 2. The actual Todo project

Your implementation already exists. Relevant structure (based on your shared `tree` output):

```text
todo/
├── README.md
├── backend/
│   ├── pyproject.toml
│   ├── src/todo_api/
│   │   ├── api/deps.py
│   │   ├── api/errors.py
│   │   ├── api/routes/{todos.py,users.py}
│   │   ├── core/{config.py,tokens.py}
│   │   ├── db/{models.py,schema.py,session.py}
│   │   ├── repositories/{protocols.py,todo_repository.py,user_repository.py}
│   │   ├── schemas/{todo.py,user.py,errors.py}
│   │   ├── services/{todo_service.py,errors.py}
│   │   └── main.py
│   └── tests/{api,integration,unit}/
└── specs/001-todo-management/
    ├── checklists/requirements.md
    ├── contracts/todos.openapi.yaml
    ├── data-model.md
    ├── plan.md
    ├── quickstart.md
    ├── research.md
    ├── spec.md
    └── tasks.md
```

Spec Kit typically also creates hidden `.specify/` and Cursor integration files; `tree .` does not show hidden directories unless you use `tree -a`. Check with `ls -la .specify .cursor` where applicable. The constitution is normally `.specify/memory/constitution.md`.

**Project choices we settled on:** FastAPI backend; Pydantic v2; SQLAlchemy 2.x; SQLite for local development; pytest; thin API handlers; service and repository layers; environment-backed settings. **No Alembic for the initial learning project**; `Base.metadata.create_all()` is acceptable for initializing a fresh development database. Existing-table schema changes are not automatically migrated by `create_all()`.

The generated specification also includes **Person/owner identity and bearer-token behavior**. Do not casually remove those requirements when making changes: the API includes `users.py`, `tokens.py`, and ownership tests.

## 3. Initial setup: commands and where to run them

### Terminal — installation and initialization

These are the setup commands discussed for your already-created `todo` repository. **Do not rerun `specify init` unless you intentionally want to repair or refresh the integration**; it may change generated configuration.

```bash
cd /path/to/todo
uv tool install specify-cli
specify version
# Initial setup only, after committing/stashing any existing changes:
specify init --here --force --integration cursor-agent
```

Check the CLI options installed on your machine with `specify init --help`. If `specify version` is unsupported in your installed release, use `specify --help` and the available version command. Use the exact Cursor integration/command names offered by your installed version.

**Terminal vs Cursor:** `uv`, `specify init`, `git`, and `pytest` run in a shell. `/speckit.*` commands run in the **Cursor agent chat**, not in your shell.

**Important command naming:** The commands used in this project discussion use `/speckit.constitution`, `/speckit.specify`, etc. Other integrations/releases may expose `/speckit-constitution` or another syntax. Choose the command actually installed in Cursor.

### Git checkpoint before agent changes

```bash
git status
git add .
git commit -m "chore: checkpoint before spec changes"
```

Only commit files you intend to track. Do not commit a local SQLite database containing sensitive data, `.env` secrets, virtual environments, caches, or generated `*.egg-info` unless your repository intentionally tracks them.

## 4. Writing the constitution in plain English

**Purpose:** Long-lived, testable engineering rules for the entire repository. Usually write once, then amend only when the team's principles change.

### Questions to answer before writing

1. What is the project's purpose and expected lifetime: tutorial, prototype, or production?
2. What architecture boundaries must remain stable?
3. What quality rules are non-negotiable (tests, typing, validation, error handling)?
4. How should secrets and configuration be handled?
5. What is explicitly out of scope, and why?
6. Which choices are permanent principles versus temporary technology choices?
7. Can an AI reviewer objectively check compliance with each MUST statement?

**Prefer:** “API routes MUST delegate business rules to services.”

**Avoid:** “Code should be clean, scalable, and amazing.” (Not testable.)

### Example constitution prompt — Cursor chat

```text
/speckit.constitution

Create or update the engineering constitution for this FastAPI Todo
learning project. Preserve any existing principles that do not conflict.

Non-negotiable rules:
1. Use typed Python and Pydantic v2 for request/response validation.
2. Keep HTTP concerns in API routes, business rules in services,
   and persistence in repositories.
3. Use SQLAlchemy 2.x; services must not depend on SQLite-specific SQL.
4. Use pytest with unit, integration, and API coverage for behavior changes.
5. Keep secrets out of source control; read settings from the environment.
6. Return consistent HTTP errors; enforce Todo ownership on reads/writes.
7. Use SQLite for local development and initialize a fresh schema with
   SQLAlchemy metadata.create_all(). Alembic/migrations are NOT required
   for the initial learning project.
8. Do not introduce unnecessary infrastructure or dependencies.

Explain any conflict with the existing constitution before changing it.
Do not modify application code.
```

**Expected artifact:** `.specify/memory/constitution.md`. Read it after generation. Check for contradictory statements such as “Alembic MUST be used” and “migrations are out of scope.”

**When to change the constitution:** When an enduring engineering rule changes, such as requiring type checking or introducing mandatory migration governance. A one-feature UI/API change does **not** normally require a constitution change. SQLite is also a technical choice that belongs primarily in the plan; mentioning it in this learning project's constitution is an explicit scoped exception, not a universal rule.

## 5. Writing the feature specification in plain English

**Purpose:** Explain WHAT users need, WHY it matters, observable behavior, error cases, boundaries, and acceptance criteria. Avoid describing Python modules, database tables, or SQLAlchemy methods here.

### Before writing a spec, decide

- **Actors:** Who performs the action? In this repo, how is the Person/user identified?
- **Goal:** What outcome does that person need?
- **Scope:** What is included? What is explicitly excluded?
- **Inputs and rules:** Required/optional fields, length limits, valid values.
- **Ownership/security:** Who can read, edit, or delete each Todo?
- **Errors:** What happens for missing, invalid, unauthorized, or conflicting requests?
- **State changes:** What changes and what remains unchanged?
- **Defaults:** What happens when an optional value is omitted?
- **Acceptance criteria:** Can a test prove each requirement?
- **Nonfunctional needs:** Expected list size, persistence across restarts, response behavior.

### Example original feature prompt — Cursor chat

```text
/speckit.specify

Build a personal Todo management backend.

A person can create, list, view, partially update, complete, reopen,
and permanently delete their own Todos.

Each Todo has an ID, title, optional description, completed state,
created timestamp, and updated timestamp.

Rules:
- Title is required, nonblank, and at most 200 characters.
- Description is optional and at most 2000 characters.
- New Todos are incomplete.
- IDs are assigned by the system.
- A person can only access their own Todos.
- Different Todos may share the same title; ID is their identity.
- Listing returns newest first and an empty list when no Todos exist.
- Partial updates change only supplied fields.
- Repeating a no-op completion change must not change updated_at.
- Missing or other-owned Todos must not reveal another owner's data.

Describe behavior, user stories, acceptance scenarios, and edge cases.
Do not prescribe frameworks, databases, or source-file names.
```

**Expected artifact:** `specs/001-todo-management/spec.md` and typically `checklists/requirements.md`.

### How to write good requirements

Weak: “Support updates.”

Strong: “When an owner sends a partial update containing only `title`, the Todo's stored `description` and `completed` values MUST remain unchanged.”

Weak: “Handle security.”

Strong: “A caller MUST NOT retrieve or modify a Todo owned by another person; the response MUST NOT disclose its contents.”

Weak: “Be fast.”

Strong: “Listing 100 Todos must meet the explicitly agreed performance threshold under the defined local test conditions.” (Do not invent a latency target without agreeing on one.)

### User story and acceptance example

```markdown
### User story: Complete my Todo
As a Todo owner, I want to mark a Todo completed so I can track progress.

Acceptance scenarios:
1. Given an incomplete Todo I own, when I mark it complete,
   then completed becomes true and the Todo remains listable.
2. Given an already completed Todo, when I complete it again,
   then its stored values and updated_at remain unchanged.
3. Given a Todo owned by another person, when I attempt to complete it,
   then I cannot change or inspect it.
```

## 6. Clarification: resolve ambiguity before design

Run in Cursor:

```text
/speckit.clarify
```

Ask yourself: Is delete permanent? Does an empty description clear it? Can a completed Todo be reopened? Do two identical titles conflict? What does a bearer token identify? What happens when two requests update the same Todo? Clarify and record the answers rather than allowing the agent to guess.

For overlapping updates, this project analysis highlighted an important rule: **only fields included in a later successful request overwrite their stored values; omitted fields retain their previous values**. A later request wins for the fields it sends, not automatically for the whole record.

## 7. Write the technical plan: HOW to build it

**Purpose:** Choose stack, architecture, dependencies, persistence approach, API contracts, data model, error mapping, and test strategy. Unlike the spec, this is the right place to mention FastAPI, SQLite, and file layout.

### Before writing the plan

- Which existing modules should be reused?
- Which data entities, relationships, and indexes are required?
- Which request/response schemas and HTTP status codes are needed?
- Where are validation, ownership checks, and error translation performed?
- How is the DB session created and cleaned up?
- What tests are unit vs integration vs API?
- How will the SQLite file be configured and persisted?
- Will an existing SQLite DB require a migration or an intentional reset?
- Which decisions are risky enough to document in `research.md`?

### Example plan prompt — Cursor chat

```text
/speckit.plan

Implement the existing Todo specification with Python 3.12+,
FastAPI, Pydantic v2, SQLAlchemy 2.x, SQLite, and pytest.

Use this layering:
HTTP routes → services → repository interfaces/implementations
→ SQLAlchemy → SQLite.

Keep route handlers thin. Use dependency injection. Keep SQLAlchemy
models separate from Pydantic API schemas. Enforce Todo ownership
in the application logic and scoped persistence operations.
Use environment-backed configuration and consistent REST errors.
Initialize a fresh local development schema with metadata.create_all().
Do not introduce Alembic in this learning project.

Align the design with the current backend/src/todo_api structure.
Generate/reconcile data-model.md, research.md, quickstart.md,
and contracts/todos.openapi.yaml as needed.
Do not implement code yet.
```

### What each generated design file does

| File | Responsibility | Review question |
|---|---|---|
| `plan.md` | Architecture, stack, design decisions, project tree | Does the design obey the constitution and match existing code? |
| `data-model.md` | Entities, fields, relationships, invariants | Are defaults, nullability, ownership, and state transitions correct? |
| `contracts/todos.openapi.yaml` | HTTP paths, request/response schemas, errors | Can clients rely on the documented contract? |
| `research.md` | Alternatives and decisions | Are important tradeoffs and assumptions explained? |
| `quickstart.md` | Setup and verification instructions | Can a new developer run the project? |

## 8. Requirements-quality checklist (optional)

```text
/speckit.checklist Focus on Todo ownership, partial updates, input
validation, error responses, and acceptance criteria.
```

Review the checklist manually. A checked requirement-quality item means the requirement was reviewed, **not** that implementation is complete. Do not mark unreviewed items as done merely to allow implementation.

## 9. Write/review tasks in plain English

**Purpose:** Translate each requirement and design choice into small, ordered, verifiable units of work. Normally **`/speckit.tasks` generates `tasks.md`**; you supply constraints and review the result rather than writing all tasks by hand.

### Before generating tasks

- Does every functional requirement have an implementation/test task?
- Are tasks small enough to complete and verify independently?
- Are dependencies explicit (schema before repository; service before API)?
- Can independent tasks run in parallel safely?
- Are tests included for success, failure, ownership, and edge cases?
- Are tasks mapped to user stories/requirements?
- Does each task name an outcome rather than a vague activity?
- Are out-of-scope tools (e.g., Alembic) absent?
- Will tasks preserve existing behavior and tests?

### Example task-generation prompt — Cursor chat

```text
/speckit.tasks

Generate dependency-ordered tasks from the approved spec and plan.
Use the existing backend/src/todo_api layout. Include unit,
integration, and API tests for every behavioral requirement.
Keep tasks scoped and testable, identify safe parallel work,
and make story dependencies explicit. Do not include Alembic.
Do not implement any code in this step.
```

### Example of useful tasks

```markdown
- [ ] T001 Configure SQLite engine and session lifecycle.
- [ ] T002 Define Todo and Person persistence models.
- [ ] T003 Implement owner-scoped Todo repository methods.
- [ ] T004 Implement create-Todo service validation and defaults.
- [ ] T005 Expose POST /todos with request/response validation.
- [ ] T006 Test blank-title rejection and duplicate-title allowance.
- [ ] T007 Test that other owners cannot read or change a Todo.
```

A poor task says “Finish backend.” A good task says “Add an API test proving PATCH title-only preserves description.”

## 10. Analyze before implementing

In Cursor:

```text
/speckit.analyze
```

This is a **read-only report**; it does not automatically fix the artifacts. Your earlier report found:

| Finding | Meaning | Proper fix |
|---|---|---|
| I1 | Partial update and overlapping-write rules needed clearer wording | Clarify `spec.md`, then align tasks/tests |
| U1 | `user_repository.py` was in tasks but missing from the plan tree | Update `plan.md` |
| G1 | Duplicate titles allowed, but no dedicated test task | Add task/test coverage |
| O1 | A user story depended on a method created by another story | Correct dependencies in `tasks.md` |
| C1 | `Person` domain term vs `users` HTTP term | Explain naming in spec/design |
| D1 | Similar validation requirements | Keep if independently testable |

The initial analysis had **32 functional requirements, 62 tasks, 97% task coverage, and no critical issues**. Those figures describe that analysis run, not necessarily the current post-implementation state.

### Remediation prompt for Cursor

```text
Review the latest /speckit.analyze findings. Fix each issue in the
artifact that owns it: spec for behavioral ambiguity, plan/design for
technical mismatch, tasks for missing coverage or dependencies.
Preserve unrelated decisions and all existing application behavior.
Do not change code. Summarize the file-by-file changes and rerun analysis.
```

Repeat analysis until critical issues are zero, medium issues are addressed or explicitly accepted, and all meaningful requirements have task/test coverage. “100% mapped” does not itself prove correct code.

## 11. Implement, test, converge

In Cursor:

```text
/speckit.implement
```

For a larger feature, scope implementation to one task group or story, review the diff and run tests, then continue. The agent should implement from `tasks.md`, not invent extra functionality.

**Terminal verification (from `todo/`):**

```bash
cd backend
python -m pip install -e .
python -m pytest
```

Check `backend/pyproject.toml` and `quickstart.md` for the project's actual dependency groups and test instructions; pytest may need installation separately, e.g. `python -m pip install pytest`, depending on the declared dependencies. Use your chosen virtual environment. To run the API if `todo_api.main` exports `app`:

```bash
python -m uvicorn todo_api.main:app --reload
```

Check the application's actual entry point and config first; these are conventional examples, not verified executions against your local repository.

Then in Cursor:

```text
/speckit.converge
```

Convergence checks implementation against the artifacts. If it appends missing work to `tasks.md`, rerun `/speckit.implement` and `/speckit.converge` until converged. Also review the code and tests independently: an agent's “converged” result is not a substitute for test execution and human review.

```bash
cd ..
git diff --check
git status
git diff --stat
```

## 12. Your real-world change: PostgreSQL → SQLite; remove Alembic

This happened while preparing the Todo project. It was a **technical decision**, not a change in the Todo user's behavior.

- **Constitution:** Remove any mandatory Alembic/PostgreSQL rule; retain layering and testing principles. The project may explicitly allow SQLite and `create_all()` during learning.
- **`spec.md`:** Usually unchanged, unless it incorrectly contains database implementation requirements.
- **`plan.md`:** Replace PostgreSQL/Alembic with SQLite/SQLAlchemy schema initialization.
- **`tasks.md`:** Remove migration setup; ensure tasks configure SQLite and test persistence.
- **Analyze:** Check that no stale PostgreSQL or Alembic instructions remain.

Suggested Cursor sequence:

```text
/speckit.constitution
/speckit.plan
/speckit.tasks
/speckit.analyze
```

Do **not** use `/speckit.specify` to start a new feature solely because the database implementation changed.

**Caution:** `metadata.create_all()` creates missing tables but does not automatically add columns to existing tables. If you later change an existing SQLite schema, either intentionally reset disposable development data, write a controlled one-off migration, or adopt a migration tool. Never silently delete a database that contains data you need.

## 13. After implementation: modify an existing feature (add priority)

Your current implementation is complete. Imagine adding priority with values `low`, `medium`, `high` and default `medium`.

### Step A — checkpoint and scope

```bash
git status
git switch -c feat/todo-priority
```

Commit or stash unrelated work first. Check that the active feature is `001-todo-management` before running commands that infer the current feature from Git branch or environment; Spec Kit's feature detection varies by setup.

### Step B — amend the existing specification first

**For a small change to an existing capability, you do not need to create `002-*`.** You may edit `specs/001-todo-management/spec.md` in Cursor or ask the agent to update that exact file. `/speckit.specify` can create or update specs, but do not invoke it blindly if your setup would create a new numbered feature.

```text
Update ONLY specs/001-todo-management/spec.md for the existing
Todo Management feature. Do not create another numbered feature.

New requirements:
- Priority is one of low, medium, high.
- Creating a Todo without priority defaults to medium.
- The owner may change priority with a partial update.
- Invalid priority values are rejected.
- Todo responses include priority.
- Existing Todos must have a defined behavior when priority is added.
- Existing ownership, completion, and other CRUD rules remain unchanged.

Add user stories, acceptance scenarios, and requirement IDs.
Do not modify design files or application code yet.
```

**Decision to make explicitly:** What happens to already-stored SQLite Todos? Since no migrations are used, choose between a disposable DB reset and a safe schema/data upgrade. Document the chosen behavior; do not let Cursor decide to delete data implicitly.

### Step C — update downstream design artifacts

You do **not** have to hand-edit every file. Ask Cursor to reconcile affected files, then review the diff.

```text
Read the amended specs/001-todo-management/spec.md and reconcile
ONLY the affected design artifacts: plan.md, data-model.md,
contracts/todos.openapi.yaml, research.md, and quickstart.md
where changes are actually necessary.

Represent priority as low/medium/high, default medium. Define create,
PATCH, response, and invalid-value behavior. Preserve unrelated API
contracts. Address existing SQLite database compatibility explicitly.
Do not change application code or tests yet.
```

Expected changes:

```text
spec.md                   → priority behavior and acceptance criteria
data-model.md             → Todo.priority and default/invariants
todos.openapi.yaml        → create/PATCH/response enum and errors
plan.md                   → storage/validation/compatibility decisions
tasks.md                  → implementation and tests (next step)
```

A contract snippet (illustrative; adapt to your real OpenAPI structure):

```yaml
priority:
  type: string
  enum: [low, medium, high]
  default: medium
```

For PATCH, omission means “leave priority unchanged”; a response should include the effective priority. Decide separately whether explicit `null` is rejected.

### Step D — tasks, analyze, implement

In Cursor:

```text
/speckit.tasks
/speckit.analyze
```

Review for tasks covering model/schema, create default, explicit priority, PATCH, invalid values, response, existing-data strategy, and regression tests. **Protect completed tasks:** if the command regenerates `tasks.md`, review the diff and preserve the historical completion state or add a clearly scoped enhancement section rather than blindly overwriting completed work.

After resolving analysis findings:

```text
/speckit.implement
/speckit.converge
```

Verify locally:

```bash
cd backend
python -m pytest
cd ..
git diff --check
git diff --stat
git status
```

Commit after review:

```bash
git add specs backend
git commit -m "feat: add todo priority through spec-driven workflow"
```

### When to use `/speckit.specify` again

- **New cohesive capability** (e.g., Todo sharing or reminders): run `/speckit.specify` to create a new numbered feature, then clarify → plan → checklist → tasks → analyze → implement → converge.
- **Existing Todo behavior enhancement** (e.g., priority): amend `001-todo-management/spec.md` directly, or invoke the installed specify workflow only when it is explicitly configured to update that feature without creating another one.
- **Implementation-only change** (e.g., SQLite instead of PostgreSQL): change technical artifacts and any constitution rule, not the product spec unless behavior changes.
- **Pure bug fix:** reproduce and document expected vs actual behavior; if the spec is already correct, fix code/tests against it. A full new feature spec is not mandatory for every bug.

## 14. New feature example: share Todos

A separate capability deserves its own spec:

```text
/speckit.specify

Allow Todo owners to share a Todo with another registered person.
Owners may grant and revoke read access and see current recipients.
Recipients may view shared Todos but cannot edit, complete, or delete
them. Sharing never transfers ownership. Define behavior for revoked
access, invalid recipients, duplicate shares, and deleted Todos.
Do not choose storage or API implementation details yet.
```

This may create `specs/002-todo-sharing/`. Review the generated directory/branch and follow with:

```text
/speckit.clarify
/speckit.plan
/speckit.checklist
/speckit.tasks
/speckit.analyze
/speckit.implement
/speckit.converge
```

For planning, explicitly instruct the agent to reuse the existing Person/Todo identity model, SQLAlchemy repository interfaces, SQLite development database, and established FastAPI error conventions.

## 15. Prompt-writing template for any future feature

Copy this into Cursor and fill in the brackets:

```text
Context:
This is the existing FastAPI Todo backend. Preserve current behavior.

Problem:
[What is difficult or missing today?]

Actor and goal:
As a [person/role], I want [capability] so that [outcome].

Required behavior:
1. [Observable requirement]
2. [Observable requirement]
3. [Observable requirement]

Validation and edge cases:
- [Required fields, defaults, bounds]
- [Missing/invalid input behavior]
- [Ownership/permission behavior]
- [Concurrent update or retry behavior]

Out of scope:
- [What we deliberately will not build]

Acceptance criteria:
- Given [initial state], when [action], then [observable result].
- Given [error state], when [action], then [safe error/result].

Constraints:
- Respect the current constitution and existing public contracts.
- Do not invent infrastructure or change unrelated code.

This phase only:
[Specification / Plan / Tasks / Implementation]
Do not proceed to the next phase until I review the output.
```

### Vocabulary for clear requirements

- **MUST:** Mandatory and verifiable.
- **SHOULD:** Recommended; exceptions need a reason.
- **MAY:** Optional.
- **Given / When / Then:** A testable acceptance scenario.
- **Out of scope:** An explicit boundary that prevents accidental feature growth.
- **Invariant:** A condition that must remain true (e.g., ownership never changes on PATCH).
- **Idempotent/no-op:** Repeating an action does not create an additional state change when already satisfied.

Avoid combining several independent requirements into a vague sentence. Give each behavior its own acceptance criteria.

## 16. Practical review checklist before each stage

| Gate | Questions |
|---|---|
| Constitution | Are rules durable, unambiguous, and verifiable? Any conflicting MUSTs? |
| Specification | Are actors, success, failure, defaults, security, and boundaries clear? |
| Clarification | Are important unanswered decisions resolved and recorded? |
| Plan | Does the architecture reuse existing code and honor the constitution? |
| Data model | Are types, ownership, nullability, defaults, and transitions defined? |
| OpenAPI | Do requests, responses, errors, and partial updates match the spec? |
| Tasks | Does every requirement have implementation and verification work? |
| Analysis | Are inconsistencies and uncovered requirements resolved? |
| Implementation | Did the agent change only intended code and add appropriate tests? |
| Convergence | Are remaining spec-to-code gaps closed? |
| Git review | Are secrets, databases, caches, and accidental changes excluded? |

## 17. Common mistakes and how to avoid them

1. **Putting frameworks in `spec.md`.** Put user behavior in the spec and technology choices in `plan.md`.
2. **Regenerating everything for one small change.** Update only affected artifacts and review diffs.
3. **Running `/speckit.specify` without selecting the existing feature.** You may accidentally create another `002-*` directory.
4. **Assuming `/speckit.analyze` fixes files.** It reports; you or the agent must make the edits.
5. **Assuming `create_all()` migrates SQLite.** It does not alter existing columns automatically.
6. **Treating generated tests as proof without running them.** Execute tests and review assertions.
7. **Losing completed-task history.** Diff `tasks.md` before accepting regenerated tasks.
8. **Using vague acceptance criteria.** Specify inputs, expected outputs, and errors.
9. **Letting AI silently choose defaults.** Make defaults, null behavior, and security boundaries explicit.
10. **Overengineering the tutorial.** Introduce migrations, queues, caching, or deployment only when the learning objective calls for them.

## 18. One-page command reference

| Action | Where | Command or action |
|---|---|---|
| Install Spec Kit | Terminal | `uv tool install specify-cli` |
| Initialize existing repo (once) | Terminal | `specify init --here --force --integration cursor-agent` |
| Set engineering principles | Cursor | `/speckit.constitution` |
| Define new feature behavior | Cursor | `/speckit.specify` |
| Resolve ambiguity | Cursor | `/speckit.clarify` |
| Design implementation | Cursor | `/speckit.plan` |
| Review requirements quality | Cursor | `/speckit.checklist` |
| Generate implementation tasks | Cursor | `/speckit.tasks` |
| Check consistency | Cursor | `/speckit.analyze` |
| Execute approved tasks | Cursor | `/speckit.implement` |
| Verify implementation completeness | Cursor | `/speckit.converge` |
| Run tests | Terminal, from `backend/` | `python -m pytest` |
| Review changes | Terminal | `git diff --check && git status` |

**Recommended repeatable sequence:**

```text
New feature:
  specify → clarify → plan → checklist → tasks → analyze
  → implement → test → converge → review/commit

Existing feature enhancement:
  amend existing spec → reconcile design/contract → update tasks
  → analyze → implement → test → converge → review/commit

Technical-only change:
  update constitution if needed → revise plan/design/tasks
  → analyze → implement/test → review/commit
```

## 19. References

Official sources (URLs are included in this Markdown file for use inside your repository):

- Spec Kit project: https://github.com/github/spec-kit
- Official documentation: https://github.github.com/spec-kit/
- Agentic SDD command reference: https://github.github.com/spec-kit/reference/agentic-sdd.html
- Existing-project guide: https://github.com/github/spec-kit/blob/main/docs/guides/existing-projects.md
- Installation/upgrade guidance: https://github.com/github/spec-kit/tree/main/docs

**Final principle:** Make the specification the source of truth for behavior, the plan the source of truth for technical design, the tasks the execution checklist, and the tests/code the evidence. Update the appropriate source first whenever requirements change.
