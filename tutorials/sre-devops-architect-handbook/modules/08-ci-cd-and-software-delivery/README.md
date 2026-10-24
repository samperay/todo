# Module 08 — Ci Cd And Software Delivery

**Scope:** Local CI quality gates.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Ci Cd And Software Delivery**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Local CI quality gates**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [08.01-ci-versus-cd](lessons/08.01-ci-versus-cd.md) | CI versus CD | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.02-git-branching-and-protected-main](lessons/08.02-git-branching-and-protected-main.md) | Git branching and protected main | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.03-ruff-mypy-and-pytest-jobs](lessons/08.03-ruff-mypy-and-pytest-jobs.md) | Ruff, mypy and pytest jobs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.04-frontend-lint-build-test-gates](lessons/08.04-frontend-lint-build-test-gates.md) | Frontend lint/build/test gates | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.05-dependency-pinning-and-caching](lessons/08.05-dependency-pinning-and-caching.md) | Dependency pinning and caching | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.06-build-artifacts-and-provenance](lessons/08.06-build-artifacts-and-provenance.md) | Build artifacts and provenance | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.07-container-registry-workflows](lessons/08.07-container-registry-workflows.md) | Container registry workflows | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.08-release-tags-and-semantic-versioning](lessons/08.08-release-tags-and-semantic-versioning.md) | Release tags and semantic versioning | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.09-deployment-environments-and-approvals](lessons/08.09-deployment-environments-and-approvals.md) | Deployment environments and approvals | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.10-rolling-blue-green-and-canary-strategies](lessons/08.10-rolling-blue-green-and-canary-strategies.md) | Rolling, blue-green and canary strategies | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.11-rollback-and-verification](lessons/08.11-rollback-and-verification.md) | Rollback and verification | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |
| [08.12-pipeline-threat-modeling](lessons/08.12-pipeline-threat-modeling.md) | Pipeline threat modeling | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
