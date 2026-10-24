# Module 20 — Sre Devops Architect Capstone

**Scope:** Architecture review and decision records.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Sre Devops Architect Capstone**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Architecture review and decision records**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [20.01-business-and-nonfunctional-requirements](lessons/20.01-business-and-nonfunctional-requirements.md) | Business and nonfunctional requirements | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.02-current-state-and-target-state-architecture](lessons/20.02-current-state-and-target-state-architecture.md) | Current-state and target-state architecture | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.03-capacity-and-failure-assumptions](lessons/20.03-capacity-and-failure-assumptions.md) | Capacity and failure assumptions | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.04-security-and-threat-modeling](lessons/20.04-security-and-threat-modeling.md) | Security and threat modeling | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.05-cost-and-operational-complexity](lessons/20.05-cost-and-operational-complexity.md) | Cost and operational complexity | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.06-technology-selection-trade-offs](lessons/20.06-technology-selection-trade-offs.md) | Technology selection trade-offs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.07-architecture-decision-records](lessons/20.07-architecture-decision-records.md) | Architecture decision records | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.08-ci-cd-and-change-safety](lessons/20.08-ci-cd-and-change-safety.md) | CI/CD and change safety | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.09-slos-monitoring-and-incident-response](lessons/20.09-slos-monitoring-and-incident-response.md) | SLOs, monitoring and incident response | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.10-disaster-recovery-and-game-days](lessons/20.10-disaster-recovery-and-game-days.md) | Disaster recovery and game days | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.11-operational-readiness-review](lessons/20.11-operational-readiness-review.md) | Operational readiness review | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |
| [20.12-executive-communication-and-portfolio-presentation](lessons/20.12-executive-communication-and-portfolio-presentation.md) | Executive communication and portfolio presentation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
