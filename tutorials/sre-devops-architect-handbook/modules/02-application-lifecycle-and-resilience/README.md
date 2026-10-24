# Module 02 — Application Lifecycle And Resilience (Handbook v3)

**Purpose:** Learn application lifecycle and resilience through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-02.py`](../../labs/module-experiments/module-02.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [02.01 — react state and re rendering](lessons/02.01-react-state-and-re-rendering.md) | `python3 .../module-02.py --lesson 02.01` |
| [02.02 — browser localstorage versus server persistence](lessons/02.02-browser-localstorage-versus-server-persistence.md) | `python3 .../module-02.py --lesson 02.02` |
| [02.03 — useeffect and cleanup](lessons/02.03-useeffect-and-cleanup.md) | `python3 .../module-02.py --lesson 02.03` |
| [02.04 — useref and mutable coordination](lessons/02.04-useref-and-mutable-coordination.md) | `python3 .../module-02.py --lesson 02.04` |
| [02.05 — abortcontroller and stale requests](lessons/02.05-abortcontroller-and-stale-requests.md) | `python3 .../module-02.py --lesson 02.05` |
| [02.06 — session generations and race prevention](lessons/02.06-session-generations-and-race-prevention.md) | `python3 .../module-02.py --lesson 02.06` |
| [02.07 — timeout budgets and HTTP failure taxonomy](lessons/02.07-timeout-budgets-and-http-failure-taxonomy.md) | `python3 .../module-02.py --lesson 02.07` |
| [02.08 — idempotency and safe retry deCIsions](lessons/02.08-idempotency-and-safe-retry-decisions.md) | `python3 .../module-02.py --lesson 02.08` |
| [02.09 — exponential backoff and jitter](lessons/02.09-exponential-backoff-and-jitter.md) | `python3 .../module-02.py --lesson 02.09` |
| [02.10 — CIrcuit breaker states](lessons/02.10-circuit-breaker-states.md) | `python3 .../module-02.py --lesson 02.10` |
| [02.11 — graceful degradation and inCIdent diagnosis](lessons/02.11-graceful-degradation-and-incident-diagnosis.md) | `python3 .../module-02.py --lesson 02.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
