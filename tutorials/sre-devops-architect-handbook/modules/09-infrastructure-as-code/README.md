# Module 09 — Infrastructure As Code

**Scope:** Infrastructure as code dry-run.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Infrastructure As Code**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Infrastructure as code dry-run**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [09.01-declarative-infrastructure](lessons/09.01-declarative-infrastructure.md) | Declarative infrastructure | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.02-terraform-providers-and-resources](lessons/09.02-terraform-providers-and-resources.md) | Terraform providers and resources | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.03-variables-outputs-locals](lessons/09.03-variables-outputs-locals.md) | Variables, outputs, locals | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.04-state-and-state-locking](lessons/09.04-state-and-state-locking.md) | State and state locking | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.05-plan-apply-destroy-lifecycle](lessons/09.05-plan-apply-destroy-lifecycle.md) | Plan/apply/destroy lifecycle | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.06-remote-state-and-encryption](lessons/09.06-remote-state-and-encryption.md) | Remote state and encryption | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.07-modules-and-composition](lessons/09.07-modules-and-composition.md) | Modules and composition | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.08-environment-separation](lessons/09.08-environment-separation.md) | Environment separation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.09-drift-detection](lessons/09.09-drift-detection.md) | Drift detection | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.10-least-privilege-for-automation](lessons/09.10-least-privilege-for-automation.md) | Least privilege for automation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |
| [09.11-policy-checks-and-cost-awareness](lessons/09.11-policy-checks-and-cost-awareness.md) | Policy checks and cost awareness | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
