# Module 18 — Disaster Recovery And Chaos Engineering (Handbook v5)

**Purpose:** Learn disaster recovery and chaos engineering through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-18.py`](../../labs/module-experiments/module-18.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [18.01 — backup versus replication](lessons/18.01-backup-versus-replication.md) | `python3 .../module-18.py --lesson 18.01` |
| [18.02 — RPO and RTO definitions](lessons/18.02-rpo-and-rto-definitions.md) | `python3 .../module-18.py --lesson 18.02` |
| [18.03 — SQLite consistent backup practices](lessons/18.03-sqlite-consistent-backup-practices.md) | `python3 .../module-18.py --lesson 18.03` |
| [18.04 — restore verification](lessons/18.04-restore-verification.md) | `python3 .../module-18.py --lesson 18.04` |
| [18.05 — failure modes and blast radius](lessons/18.05-failure-modes-and-blast-radius.md) | `python3 .../module-18.py --lesson 18.05` |
| [18.06 — dependency mapping](lessons/18.06-dependency-mapping.md) | `python3 .../module-18.py --lesson 18.06` |
| [18.07 — fault injection hypotheses](lessons/18.07-fault-injection-hypotheses.md) | `python3 .../module-18.py --lesson 18.07` |
| [18.08 — graceful shutdown and recovery](lessons/18.08-graceful-shutdown-and-recovery.md) | `python3 .../module-18.py --lesson 18.08` |
| [18.09 — disaster runbooks](lessons/18.09-disaster-runbooks.md) | `python3 .../module-18.py --lesson 18.09` |
| [18.10 — game days and inCIdent learning](lessons/18.10-game-days-and-incident-learning.md) | `python3 .../module-18.py --lesson 18.10` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.
