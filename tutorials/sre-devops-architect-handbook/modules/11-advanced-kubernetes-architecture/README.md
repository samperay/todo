# Module 11 — Advanced Kubernetes Architecture (Handbook v5)

**Purpose:** Learn advanced kubernetes architecture through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-11.py`](../../labs/module-experiments/module-11.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [11.01 — ingress and gateway API](lessons/11.01-ingress-and-gateway-api.md) | `python3 .../module-11.py --lesson 11.01` |
| [11.02 — service discovery and traffic flow](lessons/11.02-service-discovery-and-traffic-flow.md) | `python3 .../module-11.py --lesson 11.02` |
| [11.03 — horizontal pod autoscaler](lessons/11.03-horizontal-pod-autoscaler.md) | `python3 .../module-11.py --lesson 11.03` |
| [11.04 — cluster autoscaling concepts](lessons/11.04-cluster-autoscaling-concepts.md) | `python3 .../module-11.py --lesson 11.04` |
| [11.05 — persistentvolumes and claims](lessons/11.05-persistentvolumes-and-claims.md) | `python3 .../module-11.py --lesson 11.05` |
| [11.06 — storage classes and failure domains](lessons/11.06-storage-classes-and-failure-domains.md) | `python3 .../module-11.py --lesson 11.06` |
| [11.07 — helm charts and values](lessons/11.07-helm-charts-and-values.md) | `python3 .../module-11.py --lesson 11.07` |
| [11.08 — networkpoliCIes](lessons/11.08-networkpolicies.md) | `python3 .../module-11.py --lesson 11.08` |
| [11.09 — poddisruptionbudgets](lessons/11.09-poddisruptionbudgets.md) | `python3 .../module-11.py --lesson 11.09` |
| [11.10 — affinity and topology spread](lessons/11.10-affinity-and-topology-spread.md) | `python3 .../module-11.py --lesson 11.10` |
| [11.11 — rbac and service accounts](lessons/11.11-rbac-and-service-accounts.md) | `python3 .../module-11.py --lesson 11.11` |
| [11.12 — multi tenant operational boundaries](lessons/11.12-multi-tenant-operational-boundaries.md) | `python3 .../module-11.py --lesson 11.12` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.
