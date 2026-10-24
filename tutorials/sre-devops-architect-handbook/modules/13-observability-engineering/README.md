# Module 13 — Observability Engineering (Handbook v5)

**Purpose:** Learn observability engineering through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-13.py`](../../labs/module-experiments/module-13.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [13.01 — three pillars and their limitations](lessons/13.01-three-pillars-and-their-limitations.md) | `python3 .../module-13.py --lesson 13.01` |
| [13.02 — existing metrics endpoint and exposition format](lessons/13.02-existing-metrics-endpoint-and-exposition-format.md) | `python3 .../module-13.py --lesson 13.02` |
| [13.03 — counters gauges histograms](lessons/13.03-counters-gauges-histograms.md) | `python3 .../module-13.py --lesson 13.03` |
| [13.04 — red and use methods](lessons/13.04-red-and-use-methods.md) | `python3 .../module-13.py --lesson 13.04` |
| [13.05 — label cardinality](lessons/13.05-label-cardinality.md) | `python3 .../module-13.py --lesson 13.05` |
| [13.06 — promql rates and quantiles](lessons/13.06-promql-rates-and-quantiles.md) | `python3 .../module-13.py --lesson 13.06` |
| [13.07 — grafana dashboards](lessons/13.07-grafana-dashboards.md) | `python3 .../module-13.py --lesson 13.07` |
| [13.08 — structured application logging](lessons/13.08-structured-application-logging.md) | `python3 .../module-13.py --lesson 13.08` |
| [13.09 — trace and span fundamentals](lessons/13.09-trace-and-span-fundamentals.md) | `python3 .../module-13.py --lesson 13.09` |
| [13.10 — opentelemetry instrumentation](lessons/13.10-opentelemetry-instrumentation.md) | `python3 .../module-13.py --lesson 13.10` |
| [13.11 — alerting and noise reduction](lessons/13.11-alerting-and-noise-reduction.md) | `python3 .../module-13.py --lesson 13.11` |
| [13.12 — operational runbooks](lessons/13.12-operational-runbooks.md) | `python3 .../module-13.py --lesson 13.12` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.
