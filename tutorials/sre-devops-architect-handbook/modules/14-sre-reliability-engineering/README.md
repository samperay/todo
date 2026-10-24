# Module 14 — Sre Reliability Engineering

**Scope:** SLO and error budget.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Sre Reliability Engineering**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **SLO and error budget**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [14.01-service-level-indicators](lessons/14.01-service-level-indicators.md) | Service-level indicators | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.02-service-level-objectives](lessons/14.02-service-level-objectives.md) | Service-level objectives | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.03-error-budgets-and-burn-rates](lessons/14.03-error-budgets-and-burn-rates.md) | Error budgets and burn rates | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.04-availability-versus-correctness](lessons/14.04-availability-versus-correctness.md) | Availability versus correctness | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.05-latency-percentiles](lessons/14.05-latency-percentiles.md) | Latency percentiles | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.06-alerting-on-symptoms](lessons/14.06-alerting-on-symptoms.md) | Alerting on symptoms | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.07-incident-severity-and-response](lessons/14.07-incident-severity-and-response.md) | Incident severity and response | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.08-runbooks-and-escalation](lessons/14.08-runbooks-and-escalation.md) | Runbooks and escalation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.09-postmortems-and-action-items](lessons/14.09-postmortems-and-action-items.md) | Postmortems and action items | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.10-toil-reduction-and-automation](lessons/14.10-toil-reduction-and-automation.md) | Toil reduction and automation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |
| [14.11-capacity-planning-and-reliability-reviews](lessons/14.11-capacity-planning-and-reliability-reviews.md) | Capacity planning and reliability reviews | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
