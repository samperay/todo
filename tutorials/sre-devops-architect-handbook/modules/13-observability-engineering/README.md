# Module 13 — Observability Engineering

**Scope:** Prometheus metric semantics.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Observability Engineering**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Prometheus metric semantics**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [13.01-three-pillars-and-their-limitations](lessons/13.01-three-pillars-and-their-limitations.md) | Three pillars and their limitations | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.02-existing-metrics-endpoint-and-exposition-format](lessons/13.02-existing-metrics-endpoint-and-exposition-format.md) | Existing /metrics endpoint and exposition format | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.03-counters-gauges-histograms](lessons/13.03-counters-gauges-histograms.md) | Counters, gauges, histograms | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.04-red-and-use-methods](lessons/13.04-red-and-use-methods.md) | RED and USE methods | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.05-label-cardinality](lessons/13.05-label-cardinality.md) | Label cardinality | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.06-promql-rates-and-quantiles](lessons/13.06-promql-rates-and-quantiles.md) | PromQL rates and quantiles | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.07-grafana-dashboards](lessons/13.07-grafana-dashboards.md) | Grafana dashboards | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.08-structured-application-logging](lessons/13.08-structured-application-logging.md) | Structured application logging | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.09-trace-and-span-fundamentals](lessons/13.09-trace-and-span-fundamentals.md) | Trace and span fundamentals | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.10-opentelemetry-instrumentation](lessons/13.10-opentelemetry-instrumentation.md) | OpenTelemetry instrumentation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.11-alerting-and-noise-reduction](lessons/13.11-alerting-and-noise-reduction.md) | Alerting and noise reduction | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |
| [13.12-operational-runbooks](lessons/13.12-operational-runbooks.md) | Operational runbooks | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
