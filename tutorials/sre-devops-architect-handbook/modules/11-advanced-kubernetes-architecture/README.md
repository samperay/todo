# Module 11 — Advanced Kubernetes Architecture

**Scope:** Advanced Kubernetes prerequisite check.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Advanced Kubernetes Architecture**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Advanced Kubernetes prerequisite check**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [11.01-ingress-and-gateway-api](lessons/11.01-ingress-and-gateway-api.md) | Ingress and Gateway API | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.02-service-discovery-and-traffic-flow](lessons/11.02-service-discovery-and-traffic-flow.md) | Service discovery and traffic flow | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.03-horizontal-pod-autoscaler](lessons/11.03-horizontal-pod-autoscaler.md) | Horizontal Pod Autoscaler | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.04-cluster-autoscaling-concepts](lessons/11.04-cluster-autoscaling-concepts.md) | Cluster autoscaling concepts | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.05-persistentvolumes-and-claims](lessons/11.05-persistentvolumes-and-claims.md) | PersistentVolumes and claims | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.06-storage-classes-and-failure-domains](lessons/11.06-storage-classes-and-failure-domains.md) | Storage classes and failure domains | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.07-helm-charts-and-values](lessons/11.07-helm-charts-and-values.md) | Helm charts and values | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.08-networkpolicies](lessons/11.08-networkpolicies.md) | NetworkPolicies | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.09-poddisruptionbudgets](lessons/11.09-poddisruptionbudgets.md) | PodDisruptionBudgets | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.10-affinity-and-topology-spread](lessons/11.10-affinity-and-topology-spread.md) | Affinity and topology spread | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.11-rbac-and-service-accounts](lessons/11.11-rbac-and-service-accounts.md) | RBAC and service accounts | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |
| [11.12-multi-tenant-operational-boundaries](lessons/11.12-multi-tenant-operational-boundaries.md) | Multi-tenant operational boundaries | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
