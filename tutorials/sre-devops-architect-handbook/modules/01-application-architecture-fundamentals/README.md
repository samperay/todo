# Module 01 — Application Architecture Fundamentals

**Scope:** HTTP boundaries and dependency health.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Application Architecture Fundamentals**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **HTTP boundaries and dependency health**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [01.01-application-boundaries-and-responsibilities](lessons/01.01-application-boundaries-and-responsibilities.md) | Application boundaries and responsibilities | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.02-react-bootstrap-main-tsx](lessons/01.02-react-bootstrap-main-tsx.md) | React bootstrap: main.tsx | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.03-component-composition-app-tsx](lessons/01.03-component-composition-app-tsx.md) | Component composition: App.tsx | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.04-development-servers-and-ports](lessons/01.04-development-servers-and-ports.md) | Development servers and ports | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.05-tcp-listeners-and-process-trees](lessons/01.05-tcp-listeners-and-process-trees.md) | TCP listeners and process trees | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.06-http-status-codes-and-headers](lessons/01.06-http-status-codes-and-headers.md) | HTTP status codes and headers | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.07-vite-proxy-and-same-origin-routing](lessons/01.07-vite-proxy-and-same-origin-routing.md) | Vite proxy and same-origin routing | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.08-bearer-authentication-request-path](lessons/01.08-bearer-authentication-request-path.md) | Bearer authentication request path | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.09-dependency-failure-and-502-diagnosis](lessons/01.09-dependency-failure-and-502-diagnosis.md) | Dependency failure and 502 diagnosis | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |
| [01.10-architecture-diagrams-and-adrs](lessons/01.10-architecture-diagrams-and-adrs.md) | Architecture diagrams and ADRs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
