# Module 10 — Kubernetes Fundamentals

**Scope:** Kubernetes read-only discovery.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Kubernetes Fundamentals**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Kubernetes read-only discovery**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [10.01-control-plane-and-worker-nodes](lessons/10.01-control-plane-and-worker-nodes.md) | Control plane and worker nodes | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.02-pods-and-container-lifecycle](lessons/10.02-pods-and-container-lifecycle.md) | Pods and container lifecycle | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.03-deployments-and-replicasets](lessons/10.03-deployments-and-replicasets.md) | Deployments and ReplicaSets | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.04-services-and-dns](lessons/10.04-services-and-dns.md) | Services and DNS | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.05-namespaces-and-labels](lessons/10.05-namespaces-and-labels.md) | Namespaces and labels | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.06-configmaps-and-secrets](lessons/10.06-configmaps-and-secrets.md) | ConfigMaps and Secrets | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.07-resource-requests-and-limits](lessons/10.07-resource-requests-and-limits.md) | Resource requests and limits | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.08-liveness-readiness-startup-probes](lessons/10.08-liveness-readiness-startup-probes.md) | Liveness, readiness, startup probes | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.09-kubectl-describe-and-logs](lessons/10.09-kubectl-describe-and-logs.md) | kubectl describe and logs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.10-rolling-updates-and-rollback](lessons/10.10-rolling-updates-and-rollback.md) | Rolling updates and rollback | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |
| [10.11-persistent-storage-introduction](lessons/10.11-persistent-storage-introduction.md) | Persistent storage introduction | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
