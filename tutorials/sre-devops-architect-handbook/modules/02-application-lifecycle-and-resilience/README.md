# Module 02 — Application Lifecycle And Resilience

**Scope:** Retry, backoff and circuit breaker.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Application Lifecycle And Resilience**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Retry, backoff and circuit breaker**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [02.01-react-state-and-re-rendering](lessons/02.01-react-state-and-re-rendering.md) | React state and re-rendering | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.02-browser-localstorage-versus-server-persistence](lessons/02.02-browser-localstorage-versus-server-persistence.md) | Browser localStorage versus server persistence | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.03-useeffect-and-cleanup](lessons/02.03-useeffect-and-cleanup.md) | useEffect and cleanup | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.04-useref-and-mutable-coordination](lessons/02.04-useref-and-mutable-coordination.md) | useRef and mutable coordination | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.05-abortcontroller-and-stale-requests](lessons/02.05-abortcontroller-and-stale-requests.md) | AbortController and stale requests | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.06-session-generations-and-race-prevention](lessons/02.06-session-generations-and-race-prevention.md) | Session generations and race prevention | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.07-timeout-budgets-and-http-failure-taxonomy](lessons/02.07-timeout-budgets-and-http-failure-taxonomy.md) | Timeout budgets and HTTP failure taxonomy | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.08-idempotency-and-safe-retry-decisions](lessons/02.08-idempotency-and-safe-retry-decisions.md) | Idempotency and safe retry decisions | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.09-exponential-backoff-and-jitter](lessons/02.09-exponential-backoff-and-jitter.md) | Exponential backoff and jitter | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.10-circuit-breaker-states](lessons/02.10-circuit-breaker-states.md) | Circuit breaker states | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |
| [02.11-graceful-degradation-and-incident-diagnosis](lessons/02.11-graceful-degradation-and-incident-diagnosis.md) | Graceful degradation and incident diagnosis | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
