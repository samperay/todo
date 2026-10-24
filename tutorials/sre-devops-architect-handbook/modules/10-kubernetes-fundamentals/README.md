# Module 10 — Kubernetes Fundamentals (Handbook v5)

**Purpose:** Learn kubernetes fundamentals through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-10.py`](../../labs/module-experiments/module-10.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [10.01 — control plane and worker nodes](lessons/10.01-control-plane-and-worker-nodes.md) | `python3 .../module-10.py --lesson 10.01` |
| [10.02 — pods and container lifecycle](lessons/10.02-pods-and-container-lifecycle.md) | `python3 .../module-10.py --lesson 10.02` |
| [10.03 — deployments and replicasets](lessons/10.03-deployments-and-replicasets.md) | `python3 .../module-10.py --lesson 10.03` |
| [10.04 — services and dns](lessons/10.04-services-and-dns.md) | `python3 .../module-10.py --lesson 10.04` |
| [10.05 — namespaces and labels](lessons/10.05-namespaces-and-labels.md) | `python3 .../module-10.py --lesson 10.05` |
| [10.06 — configmaps and secrets](lessons/10.06-configmaps-and-secrets.md) | `python3 .../module-10.py --lesson 10.06` |
| [10.07 — resource requests and limits](lessons/10.07-resource-requests-and-limits.md) | `python3 .../module-10.py --lesson 10.07` |
| [10.08 — liveness readiness startup probes](lessons/10.08-liveness-readiness-startup-probes.md) | `python3 .../module-10.py --lesson 10.08` |
| [10.09 — kubectl describe and logs](lessons/10.09-kubectl-describe-and-logs.md) | `python3 .../module-10.py --lesson 10.09` |
| [10.10 — rolling updates and rollback](lessons/10.10-rolling-updates-and-rollback.md) | `python3 .../module-10.py --lesson 10.10` |
| [10.11 — persistent storage introduction](lessons/10.11-persistent-storage-introduction.md) | `python3 .../module-10.py --lesson 10.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.

## Canonical roadmap technology tracks

- [Kubernetes workload operations — Learn → Integrate → Operate](technologies/kubernetes/README.md)

## Technology track: Kubernetes

Start with [Kubernetes — Learn → Integrate → Operate](technologies/kubernetes/README.md).
