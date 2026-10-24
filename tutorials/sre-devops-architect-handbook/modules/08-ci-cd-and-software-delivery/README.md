# Module 08 — Ci Cd And Software Delivery (Handbook v3)

**Purpose:** Learn ci cd and software delivery through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-08.py`](../../labs/module-experiments/module-08.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [08.01 — CI versus CD](lessons/08.01-ci-versus-cd.md) | `python3 .../module-08.py --lesson 08.01` |
| [08.02 — git branching and protected main](lessons/08.02-git-branching-and-protected-main.md) | `python3 .../module-08.py --lesson 08.02` |
| [08.03 — ruff mypy and pytest jobs](lessons/08.03-ruff-mypy-and-pytest-jobs.md) | `python3 .../module-08.py --lesson 08.03` |
| [08.04 — frontend lint build test gates](lessons/08.04-frontend-lint-build-test-gates.md) | `python3 .../module-08.py --lesson 08.04` |
| [08.05 — dependency pinning and caching](lessons/08.05-dependency-pinning-and-caching.md) | `python3 .../module-08.py --lesson 08.05` |
| [08.06 — build artifacts and provenance](lessons/08.06-build-artifacts-and-provenance.md) | `python3 .../module-08.py --lesson 08.06` |
| [08.07 — container registry workflows](lessons/08.07-container-registry-workflows.md) | `python3 .../module-08.py --lesson 08.07` |
| [08.08 — release tags and semantic versioning](lessons/08.08-release-tags-and-semantic-versioning.md) | `python3 .../module-08.py --lesson 08.08` |
| [08.09 — deployment environments and approvals](lessons/08.09-deployment-environments-and-approvals.md) | `python3 .../module-08.py --lesson 08.09` |
| [08.10 — rolling blue green and canary strategies](lessons/08.10-rolling-blue-green-and-canary-strategies.md) | `python3 .../module-08.py --lesson 08.10` |
| [08.11 — rollback and verification](lessons/08.11-rollback-and-verification.md) | `python3 .../module-08.py --lesson 08.11` |
| [08.12 — pipeline threat modeling](lessons/08.12-pipeline-threat-modeling.md) | `python3 .../module-08.py --lesson 08.12` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
