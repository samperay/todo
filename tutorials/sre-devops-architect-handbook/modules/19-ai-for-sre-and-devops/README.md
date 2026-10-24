# Module 19 — Ai For Sre And Devops (Handbook v3)

**Purpose:** Learn ai for sre and devops through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-19.py`](../../labs/module-experiments/module-19.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [19.01 — llm capabilities and limitations](lessons/19.01-llm-capabilities-and-limitations.md) | `python3 .../module-19.py --lesson 19.01` |
| [19.02 — rag for runbooks and inCIdents](lessons/19.02-rag-for-runbooks-and-incidents.md) | `python3 .../module-19.py --lesson 19.02` |
| [19.03 — tool calling agents and permissions](lessons/19.03-tool-calling-agents-and-permissions.md) | `python3 .../module-19.py --lesson 19.03` |
| [19.04 — prompt and context design](lessons/19.04-prompt-and-context-design.md) | `python3 .../module-19.py --lesson 19.04` |
| [19.05 — human in the loop operations](lessons/19.05-human-in-the-loop-operations.md) | `python3 .../module-19.py --lesson 19.05` |
| [19.06 — read only diagnosis before write actions](lessons/19.06-read-only-diagnosis-before-write-actions.md) | `python3 .../module-19.py --lesson 19.06` |
| [19.07 — evaluation datasets and grounded answers](lessons/19.07-evaluation-datasets-and-grounded-answers.md) | `python3 .../module-19.py --lesson 19.07` |
| [19.08 — prompt injection and tool output trust](lessons/19.08-prompt-injection-and-tool-output-trust.md) | `python3 .../module-19.py --lesson 19.08` |
| [19.09 — auditability and rollback](lessons/19.09-auditability-and-rollback.md) | `python3 .../module-19.py --lesson 19.09` |
| [19.10 — ai assisted inCIdent summarization](lessons/19.10-ai-assisted-incident-summarization.md) | `python3 .../module-19.py --lesson 19.10` |
| [19.11 — cost and latency controls](lessons/19.11-cost-and-latency-controls.md) | `python3 .../module-19.py --lesson 19.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
