# Module 15 — Performance And Scalability

**Scope:** Latency percentiles and load.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Performance And Scalability**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Latency percentiles and load**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [15.01-latency-versus-throughput](lessons/15.01-latency-versus-throughput.md) | Latency versus throughput | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.02-concurrency-and-queueing](lessons/15.02-concurrency-and-queueing.md) | Concurrency and queueing | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.03-baseline-and-reproducibility](lessons/15.03-baseline-and-reproducibility.md) | Baseline and reproducibility | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.04-load-generators-and-safe-limits](lessons/15.04-load-generators-and-safe-limits.md) | Load generators and safe limits | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.05-p50-p95-p99-latency](lessons/15.05-p50-p95-p99-latency.md) | p50/p95/p99 latency | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.06-python-profiling](lessons/15.06-python-profiling.md) | Python profiling | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.07-database-query-analysis](lessons/15.07-database-query-analysis.md) | Database query analysis | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.08-caching-and-invalidation](lessons/15.08-caching-and-invalidation.md) | Caching and invalidation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.09-rate-limiting-and-overload](lessons/15.09-rate-limiting-and-overload.md) | Rate limiting and overload | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.10-capacity-estimates](lessons/15.10-capacity-estimates.md) | Capacity estimates | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |
| [15.11-autoscaling-trade-offs](lessons/15.11-autoscaling-trade-offs.md) | Autoscaling trade-offs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
