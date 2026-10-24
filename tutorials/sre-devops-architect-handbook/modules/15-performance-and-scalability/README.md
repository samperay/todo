# Module 15 — Performance And Scalability (Handbook v3)

**Purpose:** Learn performance and scalability through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-15.py`](../../labs/module-experiments/module-15.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [15.01 — latency versus throughput](lessons/15.01-latency-versus-throughput.md) | `python3 .../module-15.py --lesson 15.01` |
| [15.02 — concurrency and queueing](lessons/15.02-concurrency-and-queueing.md) | `python3 .../module-15.py --lesson 15.02` |
| [15.03 — baseline and reproduCIbility](lessons/15.03-baseline-and-reproducibility.md) | `python3 .../module-15.py --lesson 15.03` |
| [15.04 — load generators and safe limits](lessons/15.04-load-generators-and-safe-limits.md) | `python3 .../module-15.py --lesson 15.04` |
| [15.05 — p50 p95 p99 latency](lessons/15.05-p50-p95-p99-latency.md) | `python3 .../module-15.py --lesson 15.05` |
| [15.06 — python profiling](lessons/15.06-python-profiling.md) | `python3 .../module-15.py --lesson 15.06` |
| [15.07 — database query analysis](lessons/15.07-database-query-analysis.md) | `python3 .../module-15.py --lesson 15.07` |
| [15.08 — caching and invalidation](lessons/15.08-caching-and-invalidation.md) | `python3 .../module-15.py --lesson 15.08` |
| [15.09 — rate limiting and overload](lessons/15.09-rate-limiting-and-overload.md) | `python3 .../module-15.py --lesson 15.09` |
| [15.10 — capaCIty estimates](lessons/15.10-capacity-estimates.md) | `python3 .../module-15.py --lesson 15.10` |
| [15.11 — autoscaling trade offs](lessons/15.11-autoscaling-trade-offs.md) | `python3 .../module-15.py --lesson 15.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
