# Module 14 — Sre Reliability Engineering (Handbook v5)

**Purpose:** Learn sre reliability engineering through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-14.py`](../../labs/module-experiments/module-14.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [14.01 — service level indicators](lessons/14.01-service-level-indicators.md) | `python3 .../module-14.py --lesson 14.01` |
| [14.02 — service level objectives](lessons/14.02-service-level-objectives.md) | `python3 .../module-14.py --lesson 14.02` |
| [14.03 — error budgets and burn rates](lessons/14.03-error-budgets-and-burn-rates.md) | `python3 .../module-14.py --lesson 14.03` |
| [14.04 — availability versus correctness](lessons/14.04-availability-versus-correctness.md) | `python3 .../module-14.py --lesson 14.04` |
| [14.05 — latency percentiles](lessons/14.05-latency-percentiles.md) | `python3 .../module-14.py --lesson 14.05` |
| [14.06 — alerting on symptoms](lessons/14.06-alerting-on-symptoms.md) | `python3 .../module-14.py --lesson 14.06` |
| [14.07 — inCIdent severity and response](lessons/14.07-incident-severity-and-response.md) | `python3 .../module-14.py --lesson 14.07` |
| [14.08 — runbooks and escalation](lessons/14.08-runbooks-and-escalation.md) | `python3 .../module-14.py --lesson 14.08` |
| [14.09 — postmortems and action items](lessons/14.09-postmortems-and-action-items.md) | `python3 .../module-14.py --lesson 14.09` |
| [14.10 — toil reduction and automation](lessons/14.10-toil-reduction-and-automation.md) | `python3 .../module-14.py --lesson 14.10` |
| [14.11 — capaCIty planning and reliability reviews](lessons/14.11-capacity-planning-and-reliability-reviews.md) | `python3 .../module-14.py --lesson 14.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.
