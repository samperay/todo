# Module 20 — Sre Devops Architect Capstone (Handbook v3)

**Purpose:** Learn sre devops architect capstone through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-20.py`](../../labs/module-experiments/module-20.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [20.01 — business and nonfunctional requirements](lessons/20.01-business-and-nonfunctional-requirements.md) | `python3 .../module-20.py --lesson 20.01` |
| [20.02 — current state and target state architecture](lessons/20.02-current-state-and-target-state-architecture.md) | `python3 .../module-20.py --lesson 20.02` |
| [20.03 — capaCIty and failure assumptions](lessons/20.03-capacity-and-failure-assumptions.md) | `python3 .../module-20.py --lesson 20.03` |
| [20.04 — security and threat modeling](lessons/20.04-security-and-threat-modeling.md) | `python3 .../module-20.py --lesson 20.04` |
| [20.05 — cost and operational complexity](lessons/20.05-cost-and-operational-complexity.md) | `python3 .../module-20.py --lesson 20.05` |
| [20.06 — technology selection trade offs](lessons/20.06-technology-selection-trade-offs.md) | `python3 .../module-20.py --lesson 20.06` |
| [20.07 — architecture deCIsion records](lessons/20.07-architecture-decision-records.md) | `python3 .../module-20.py --lesson 20.07` |
| [20.08 — CI CD and change safety](lessons/20.08-ci-cd-and-change-safety.md) | `python3 .../module-20.py --lesson 20.08` |
| [20.09 — SLOs monitoring and inCIdent response](lessons/20.09-slos-monitoring-and-incident-response.md) | `python3 .../module-20.py --lesson 20.09` |
| [20.10 — disaster recovery and game days](lessons/20.10-disaster-recovery-and-game-days.md) | `python3 .../module-20.py --lesson 20.10` |
| [20.11 — operational readiness review](lessons/20.11-operational-readiness-review.md) | `python3 .../module-20.py --lesson 20.11` |
| [20.12 — executive communication and portfolio presentation](lessons/20.12-executive-communication-and-portfolio-presentation.md) | `python3 .../module-20.py --lesson 20.12` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
